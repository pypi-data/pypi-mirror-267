use super::{
    cursor::{Cursor, InnerCursor},
    transaction_options::{IsolationLevel, ReadVariant},
};
use crate::{
    common::rustdriver_future,
    exceptions::rust_errors::{RustPSQLDriverError, RustPSQLDriverPyResult},
    query_result::{PSQLDriverPyQueryResult, PSQLDriverSinglePyQueryResult},
    value_converter::{convert_parameters, postgres_to_py, PythonDTO},
};
use futures_util::future;
use pyo3::{
    pyclass, pymethods,
    types::{PyList, PyString, PyTuple},
    Py, PyAny, PyErr, PyObject, PyRef, PyRefMut, Python,
};
use std::{collections::HashSet, sync::Arc, vec};
use tokio::sync::RwLock;
use tokio_postgres::Row;

use super::connection::RustConnection;

/// Transaction for internal use only.
///
/// It is not exposed to python.
#[allow(clippy::module_name_repetitions)]
pub struct RustTransaction {
    connection: Arc<RustConnection>,
    is_started: bool,
    is_done: bool,
    rollback_savepoint: Arc<tokio::sync::RwLock<HashSet<String>>>,

    isolation_level: Option<IsolationLevel>,
    read_variant: Option<ReadVariant>,
    deferable: Option<bool>,
}

impl RustTransaction {
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        connection: Arc<RustConnection>,
        is_started: bool,
        is_done: bool,
        rollback_savepoint: Arc<tokio::sync::RwLock<HashSet<String>>>,
        isolation_level: Option<IsolationLevel>,
        read_variant: Option<ReadVariant>,
        deferable: Option<bool>,
    ) -> Self {
        Self {
            connection,
            is_started,
            is_done,
            rollback_savepoint,
            isolation_level,
            read_variant,
            deferable,
        }
    }

    fn check_is_transaction_ready(&self) -> RustPSQLDriverPyResult<()> {
        if !self.is_started {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "Transaction is not started, please call begin() on transaction".into(),
            ));
        }
        if self.is_done {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "Transaction is already committed or rolled back".into(),
            ));
        }

        Ok(())
    }

    /// Execute querystring with parameters.
    ///
    /// Method doesn't acquire lock on any structure fields.
    /// It prepares and caches querystring in the inner Object object.
    ///
    /// Then execute the query.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done already
    /// 3) Can not create/retrieve prepared statement
    /// 4) Can not execute statement
    pub async fn inner_execute(
        &self,
        querystring: String,
        parameters: Vec<PythonDTO>,
        prepared: bool,
    ) -> RustPSQLDriverPyResult<PSQLDriverPyQueryResult> {
        self.check_is_transaction_ready()?;
        self.connection
            .inner_execute(querystring, parameters, prepared)
            .await
    }

    /// Execute querystring with parameters.
    ///
    /// Method doesn't acquire lock on any structure fields.
    /// It prepares and caches querystring in the inner Object object.
    ///
    /// Then execute the query.
    ///
    /// It returns `Vec<Row>` instead of `PSQLDriverPyQueryResult`.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done already
    /// 3) Can not create/retrieve prepared statement
    /// 4) Can not execute statement
    pub async fn inner_execute_raw(
        &self,
        querystring: String,
        parameters: Vec<PythonDTO>,
        prepared: bool,
    ) -> RustPSQLDriverPyResult<Vec<Row>> {
        self.check_is_transaction_ready()?;
        self.connection
            .inner_execute_raw(querystring, parameters, prepared)
            .await
    }

    /// Execute querystring with many parameters.
    ///
    /// Method doesn't acquire lock on any structure fields.
    /// It prepares and caches querystring in the inner Object object.
    ///
    /// Then execute the query.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done already
    /// 3) Can not create/retrieve prepared statement
    /// 4) Can not execute statement
    pub async fn inner_execute_many(
        &self,
        querystring: String,
        parameters: Vec<Vec<PythonDTO>>,
        prepared: bool,
    ) -> RustPSQLDriverPyResult<()> {
        self.check_is_transaction_ready()?;
        if parameters.is_empty() {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "No parameters passed to execute_many".into(),
            ));
        }
        for single_parameters in parameters {
            self.connection
                .inner_execute(querystring.clone(), single_parameters, prepared)
                .await?;
        }

        Ok(())
    }

    /// Fetch exaclty single row from query.
    ///
    /// Method doesn't acquire lock on any structure fields.
    /// It prepares and caches querystring in the inner Object object.
    ///
    /// Then execute the query.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done already
    /// 3) Can not create/retrieve prepared statement
    /// 4) Can not execute statement
    /// 5) Query returns more than one row
    pub async fn inner_fetch_row(
        &self,
        querystring: String,
        parameters: Vec<PythonDTO>,
        prepared: bool,
    ) -> RustPSQLDriverPyResult<PSQLDriverSinglePyQueryResult> {
        self.check_is_transaction_ready()?;
        self.connection
            .inner_fetch_row(querystring, parameters, prepared)
            .await
    }

    /// Run many queries as pipeline.
    ///
    /// It can boost up querying speed.
    ///
    /// # Errors
    ///
    /// May return Err Result if can't join futures or cannot execute
    /// any of queries.
    pub async fn inner_pipeline(
        &self,
        queries: Vec<(String, Vec<PythonDTO>)>,
        prepared: bool,
    ) -> RustPSQLDriverPyResult<Vec<PSQLDriverPyQueryResult>> {
        let mut futures = vec![];
        for (querystring, params) in queries {
            let execute_future = self.inner_execute(querystring, params, prepared);
            futures.push(execute_future);
        }

        let b = future::try_join_all(futures).await?;
        Ok(b)
    }

    /// Start transaction
    /// Set up isolation level if specified
    /// Set up deferable if specified
    ///
    /// # Errors
    /// May return Err Result if cannot execute querystring.
    pub async fn start_transaction(&self) -> RustPSQLDriverPyResult<()> {
        let mut querystring = "START TRANSACTION".to_string();

        if let Some(level) = self.isolation_level {
            let level = &level.to_str_level();
            querystring.push_str(format!(" ISOLATION LEVEL {level}").as_str());
        };

        querystring.push_str(match self.read_variant {
            Some(ReadVariant::ReadOnly) => " READ ONLY",
            Some(ReadVariant::ReadWrite) => " READ WRITE",
            None => "",
        });

        querystring.push_str(match self.deferable {
            Some(true) => " DEFERRABLE",
            Some(false) => " NOT DEFERRABLE",
            None => "",
        });
        let db_client_guard = self.connection.db_client.read().await;
        db_client_guard.batch_execute(&querystring).await?;

        Ok(())
    }

    /// Start the transaction.
    ///
    /// Execute `BEGIN` commands and mark transaction as `started`.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Transaction is already started.
    /// 2) Transaction is done.
    /// 3) Cannot execute `BEGIN` command.
    pub async fn inner_begin(&mut self) -> RustPSQLDriverPyResult<()> {
        if self.is_started {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "Transaction is already started".into(),
            ));
        }

        if self.is_done {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "Transaction is already committed or rolled back".into(),
            ));
        }

        self.start_transaction().await?;
        self.is_started = true;

        Ok(())
    }

    /// Commit the transaction.
    ///
    /// Execute `COMMIT` command and mark transaction as `done`.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done
    /// 3) Cannot execute `COMMIT` command
    pub async fn inner_commit(&mut self) -> RustPSQLDriverPyResult<()> {
        self.check_is_transaction_ready()?;
        let db_client_guard = self.connection.db_client.read().await;
        db_client_guard.batch_execute("COMMIT;").await?;
        self.is_done = true;

        Ok(())
    }

    /// Create new SAVEPOINT.
    ///
    /// Execute SAVEPOINT <name of the savepoint> and
    /// add it to the transaction `rollback_savepoint` `HashSet`
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done
    /// 3) Specified savepoint name is exists
    /// 4) Can not execute SAVEPOINT command
    pub async fn inner_savepoint(&self, savepoint_name: String) -> RustPSQLDriverPyResult<()> {
        self.check_is_transaction_ready()?;

        let is_savepoint_name_exists = {
            let rollback_savepoint_read_guard = self.rollback_savepoint.read().await;
            rollback_savepoint_read_guard.contains(&savepoint_name)
        };

        if is_savepoint_name_exists {
            return Err(RustPSQLDriverError::DataBaseTransactionError(format!(
                "SAVEPOINT name {savepoint_name} is already taken by this transaction",
            )));
        }
        let db_client_guard = self.connection.db_client.read().await;
        db_client_guard
            .batch_execute(format!("SAVEPOINT {savepoint_name}").as_str())
            .await?;
        let mut rollback_savepoint_guard = self.rollback_savepoint.write().await;
        rollback_savepoint_guard.insert(savepoint_name);
        Ok(())
    }

    /// Execute ROLLBACK command.
    ///
    /// Run ROLLBACK command and mark the transaction as done.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done
    /// 3) Can not execute ROLLBACK command
    pub async fn inner_rollback(&mut self) -> RustPSQLDriverPyResult<()> {
        self.check_is_transaction_ready()?;
        let db_client_guard = self.connection.db_client.read().await;
        db_client_guard.batch_execute("ROLLBACK").await?;
        self.is_done = true;
        Ok(())
    }

    /// ROLLBACK to the specified savepoint
    ///
    /// Execute ROLLBACK TO SAVEPOINT <name of the savepoint>.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done
    /// 3) Specified savepoint name doesn't exist
    /// 4) Can not execute ROLLBACK TO SAVEPOINT command
    pub async fn inner_rollback_to(&self, rollback_name: String) -> RustPSQLDriverPyResult<()> {
        self.check_is_transaction_ready()?;

        let rollback_savepoint_arc = self.rollback_savepoint.clone();
        let is_rollback_exists = {
            let rollback_savepoint_guard = rollback_savepoint_arc.read().await;
            rollback_savepoint_guard.contains(&rollback_name)
        };
        if !is_rollback_exists {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "Don't have rollback with this name".into(),
            ));
        }
        let db_client_guard = self.connection.db_client.read().await;
        db_client_guard
            .batch_execute(format!("ROLLBACK TO SAVEPOINT {rollback_name}").as_str())
            .await?;

        Ok(())
    }

    /// Execute RELEASE SAVEPOINT.
    ///
    /// Run RELEASE SAVEPOINT command.
    ///
    /// # Errors
    /// May return Err Result if:
    /// 1) Transaction is not started
    /// 2) Transaction is done
    /// 3) Specified savepoint name doesn't exists
    /// 4) Can not execute RELEASE SAVEPOINT command
    pub async fn inner_release_savepoint(
        &self,
        rollback_name: String,
    ) -> RustPSQLDriverPyResult<()> {
        self.check_is_transaction_ready()?;

        let mut rollback_savepoint_guard = self.rollback_savepoint.write().await;
        let is_rollback_exists = rollback_savepoint_guard.remove(&rollback_name);

        if !is_rollback_exists {
            return Err(RustPSQLDriverError::DataBaseTransactionError(
                "Don't have rollback with this name".into(),
            ));
        }
        let db_client_guard = self.connection.db_client.read().await;
        db_client_guard
            .batch_execute(format!("RELEASE SAVEPOINT {rollback_name}").as_str())
            .await?;

        Ok(())
    }
}

#[pyclass()]
pub struct Transaction {
    transaction: Arc<RwLock<RustTransaction>>,
    cursor_num: usize,
}

impl Transaction {
    #[must_use]
    pub fn new(transaction: Arc<RwLock<RustTransaction>>, cursor_num: usize) -> Self {
        Transaction {
            transaction,
            cursor_num,
        }
    }
}

#[pymethods]
impl Transaction {
    #[must_use]
    pub fn __aiter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    /// Return new instance of transaction.
    ///
    /// It's necessary because python requires it.
    ///
    /// # Errors
    /// May return Err Result if future returns error.
    pub fn __anext__(&self, py: Python<'_>) -> RustPSQLDriverPyResult<Option<PyObject>> {
        let transaction_clone = self.transaction.clone();
        let cursor_num = self.cursor_num;
        let future = rustdriver_future(py, async move {
            Ok(Transaction {
                transaction: transaction_clone,
                cursor_num,
            })
        });
        Ok(Some(future?.into()))
    }

    #[allow(clippy::missing_errors_doc)]
    #[allow(clippy::needless_pass_by_value)]
    pub fn __await__<'a>(
        slf: PyRefMut<'a, Self>,
        _py: Python,
    ) -> RustPSQLDriverPyResult<PyRefMut<'a, Self>> {
        Ok(slf)
    }

    #[allow(clippy::needless_pass_by_value)]
    fn __aenter__<'a>(
        slf: PyRefMut<'a, Self>,
        py: Python<'a>,
    ) -> RustPSQLDriverPyResult<&'a PyAny> {
        let transaction_arc = slf.transaction.clone();
        let transaction_arc2 = slf.transaction.clone();
        let cursor_num = slf.cursor_num;
        rustdriver_future(py, async move {
            transaction_arc.write().await.inner_begin().await?;
            Ok(Transaction {
                transaction: transaction_arc2,
                cursor_num,
            })
        })
    }

    #[allow(clippy::needless_pass_by_value)]
    fn __aexit__<'a>(
        slf: PyRefMut<'a, Self>,
        py: Python<'a>,
        _exception_type: Py<PyAny>,
        exception: &PyAny,
        _traceback: Py<PyAny>,
    ) -> RustPSQLDriverPyResult<&'a PyAny> {
        let transaction_arc = slf.transaction.clone();
        let transaction_arc2 = slf.transaction.clone();
        let is_no_exc = exception.is_none();
        let py_err = PyErr::from_value(exception);
        let cursor_num = slf.cursor_num;

        rustdriver_future(py, async move {
            let mut trasaction_guard = transaction_arc.write().await;
            if is_no_exc {
                trasaction_guard.inner_commit().await?;
                Ok(Transaction {
                    transaction: transaction_arc2,
                    cursor_num,
                })
            } else {
                trasaction_guard.inner_rollback().await?;
                Err(RustPSQLDriverError::PyError(py_err))
            }
        })
    }

    /// Execute querystring with parameters.
    ///
    /// It converts incoming parameters to rust readable
    /// and then execute the query with them.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Cannot convert python parameters
    /// 2) Cannot execute querystring.
    pub fn execute<'a>(
        &'a self,
        py: Python<'a>,
        querystring: String,
        parameters: Option<&'a PyAny>,
        prepared: Option<bool>,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();
        let mut params: Vec<PythonDTO> = vec![];
        if let Some(parameters) = parameters {
            params = convert_parameters(parameters)?;
        }

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_execute(querystring, params, prepared.unwrap_or(true))
                .await
        })
    }

    /// Execute querystring with parameters.
    ///
    /// It converts incoming parameters to rust readable
    /// and then execute the query with them.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Cannot convert python parameters
    /// 2) Cannot execute querystring.
    pub fn execute_many<'a>(
        &'a self,
        py: Python<'a>,
        querystring: String,
        parameters: Option<&'a PyList>,
        prepared: Option<bool>,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();
        let mut params: Vec<Vec<PythonDTO>> = vec![];
        if let Some(parameters) = parameters {
            for single_parameters in parameters {
                params.push(convert_parameters(single_parameters)?);
            }
        }

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_execute_many(querystring, params, prepared.unwrap_or(true))
                .await
        })
    }
    /// Execute querystring with parameters and return first row.
    ///
    /// It converts incoming parameters to rust readable,
    /// executes query with them and returns first row of response.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Cannot convert python parameters
    /// 2) Cannot execute querystring.
    /// 3) Query returns more than one row.
    pub fn fetch_row<'a>(
        &'a self,
        py: Python<'a>,
        querystring: String,
        parameters: Option<&'a PyList>,
        prepared: Option<bool>,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();
        let mut params: Vec<PythonDTO> = vec![];
        if let Some(parameters) = parameters {
            params = convert_parameters(parameters)?;
        }

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_fetch_row(querystring, params, prepared.unwrap_or(true))
                .await
        })
    }

    /// Execute querystring with parameters and return first value in the first row.
    ///
    /// It converts incoming parameters to rust readable,
    /// executes query with them and returns first row of response.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Cannot convert python parameters
    /// 2) Cannot execute querystring.
    /// 3) Query returns more than one row
    pub fn fetch_val<'a>(
        &'a self,
        py: Python<'a>,
        querystring: String,
        parameters: Option<&'a PyList>,
        prepared: Option<bool>,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();
        let mut params: Vec<PythonDTO> = vec![];
        if let Some(parameters) = parameters {
            params = convert_parameters(parameters)?;
        }

        rustdriver_future(py, async move {
            let first_row = transaction_arc
                .read()
                .await
                .inner_fetch_row(querystring, params, prepared.unwrap_or(true))
                .await?
                .get_inner();
            Python::with_gil(|py| match first_row.columns().first() {
                Some(first_column) => postgres_to_py(py, &first_row, first_column, 0),
                None => Ok(py.None()),
            })
        })
    }

    /// Execute querystrings with parameters and return all results.
    ///
    /// Create pipeline of queries.
    ///
    /// # Errors
    ///
    /// May return Err Result if:
    /// 1) Cannot convert python parameters
    /// 2) Cannot execute any of querystring.
    pub fn pipeline<'a>(
        &'a self,
        py: Python<'a>,
        queries: Option<&'a PyList>,
        prepared: Option<bool>,
    ) -> RustPSQLDriverPyResult<&'a PyAny> {
        let mut processed_queries: Vec<(String, Vec<PythonDTO>)> = vec![];
        if let Some(queries) = queries {
            for single_query in queries {
                let query_tuple = single_query.downcast::<PyTuple>().map_err(|err| {
                    RustPSQLDriverError::PyToRustValueConversionError(format!(
                        "Cannot cast to tuple: {err}",
                    ))
                })?;
                let querystring = query_tuple.get_item(0)?.extract::<String>()?;
                match query_tuple.get_item(1) {
                    Ok(params) => {
                        processed_queries.push((querystring, convert_parameters(params)?));
                    }
                    Err(_) => {
                        processed_queries.push((querystring, vec![]));
                    }
                }
            }
        }

        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_pipeline(processed_queries, prepared.unwrap_or(true))
                .await
        })
    }

    /// Start the transaction.
    ///
    /// # Errors
    /// May return Err Result if cannot execute command.
    pub fn begin<'a>(&'a self, py: Python<'a>) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc.write().await.inner_begin().await?;

            Ok(())
        })
    }

    /// Commit the transaction.
    ///
    /// # Errors
    /// May return Err Result if cannot execute command.
    pub fn commit<'a>(&'a self, py: Python<'a>) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc.write().await.inner_commit().await?;

            Ok(())
        })
    }

    /// Create new SAVEPOINT.
    ///
    /// # Errors
    /// May return Err Result if cannot extract string
    /// or `inner_savepoint` returns
    pub fn savepoint<'a>(
        &'a self,
        py: Python<'a>,
        savepoint_name: &'a PyAny,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let py_string = {
            if savepoint_name.is_instance_of::<PyString>() {
                savepoint_name.extract::<String>()?
            } else {
                return Err(RustPSQLDriverError::PyToRustValueConversionError(
                    "Can't convert your savepoint_name to String value".into(),
                ));
            }
        };

        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_savepoint(py_string)
                .await?;

            Ok(())
        })
    }

    /// Rollback the whole transaction.
    ///
    /// # Errors
    /// May return Err Result if `rollback` returns Error.
    pub fn rollback<'a>(&'a self, py: Python<'a>) -> RustPSQLDriverPyResult<&PyAny> {
        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc.write().await.inner_rollback().await?;

            Ok(())
        })
    }

    /// Rollback to the specified savepoint.
    ///
    /// # Errors
    /// May return Err Result if cannot extract string
    /// or`inner_rollback_to` returns Error.
    pub fn rollback_to<'a>(
        &'a self,
        py: Python<'a>,
        savepoint_name: &'a PyAny,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let py_string = {
            if savepoint_name.is_instance_of::<PyString>() {
                savepoint_name.extract::<String>()?
            } else {
                return Err(RustPSQLDriverError::PyToRustValueConversionError(
                    "Can't convert your savepoint_name to String value".into(),
                ));
            }
        };

        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_rollback_to(py_string)
                .await?;

            Ok(())
        })
    }

    /// Rollback to the specified savepoint.
    ///
    /// # Errors
    /// May return Err Result if cannot extract string
    /// or`inner_rollback_to` returns Error.
    pub fn release_savepoint<'a>(
        &'a self,
        py: Python<'a>,
        savepoint_name: &'a PyAny,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let py_string = {
            if savepoint_name.is_instance_of::<PyString>() {
                savepoint_name.extract::<String>()?
            } else {
                return Err(RustPSQLDriverError::PyToRustValueConversionError(
                    "Can't convert your savepoint_name to String value".into(),
                ));
            }
        };

        let transaction_arc = self.transaction.clone();

        rustdriver_future(py, async move {
            transaction_arc
                .read()
                .await
                .inner_release_savepoint(py_string)
                .await?;
            Ok(())
        })
    }

    /// Create new cursor.
    ///
    /// Call `inner_cursor` function.
    ///
    /// # Errors
    /// May return Err Result if can't convert incoming parameters
    /// or if `inner_cursor` returns error.
    pub fn cursor<'a>(
        &'a self,
        querystring: String,
        parameters: Option<&'a PyAny>,
        fetch_number: Option<usize>,
        scroll: Option<bool>,
        prepared: Option<bool>,
    ) -> RustPSQLDriverPyResult<Cursor> {
        let mut params: Vec<PythonDTO> = vec![];
        if let Some(parameters) = parameters {
            params = convert_parameters(parameters)?;
        }

        Ok(Cursor::new(InnerCursor::new(
            self.transaction.clone(),
            querystring,
            params,
            format!("cur{}", self.cursor_num),
            scroll,
            fetch_number.unwrap_or(10),
            prepared.unwrap_or(true),
        )))
    }
}
