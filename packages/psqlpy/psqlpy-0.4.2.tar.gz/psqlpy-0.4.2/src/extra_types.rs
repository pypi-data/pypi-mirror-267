use std::str::FromStr;

use macaddr::{MacAddr6, MacAddr8};
use pyo3::{pyclass, pymethods, types::PyModule, PyAny, PyResult, Python};
use serde_json::Value;
use uuid::Uuid;

use crate::{exceptions::rust_errors::RustPSQLDriverPyResult, value_converter::build_serde_value};

macro_rules! build_python_type {
    ($st_name:ident, $rust_type:ty) => {
        #[pyclass]
        #[derive(Clone)]
        pub struct $st_name {
            inner_value: $rust_type,
        }

        impl $st_name {
            #[must_use]
            pub fn retrieve_value(&self) -> $rust_type {
                self.inner_value
            }
        }

        #[pymethods]
        impl $st_name {
            #[new]
            #[must_use]
            pub fn new_class(inner_value: $rust_type) -> Self {
                Self { inner_value }
            }

            #[must_use]
            pub fn __str__(&self) -> String {
                format!("{}, {}", stringify!($st_name), self.inner_value)
            }
        }
    };
}

build_python_type!(SmallInt, i16);
build_python_type!(Integer, i32);
build_python_type!(BigInt, i64);

#[pyclass]
#[derive(Clone)]
pub struct PyUUID {
    inner: Uuid,
}

impl PyUUID {
    #[must_use]
    pub fn inner(&self) -> Uuid {
        self.inner
    }
}

#[pymethods]
impl PyUUID {
    /// Create new uuid from Python str.
    ///
    /// # Errors
    /// May return Err Result if cannot convert python string
    /// into rust Uuid.
    #[new]
    #[allow(clippy::missing_errors_doc)]
    pub fn new_uuid(uuid_value: &str) -> RustPSQLDriverPyResult<Self> {
        Ok(Self {
            inner: Uuid::from_str(uuid_value)?,
        })
    }
}

#[pyclass]
#[derive(Clone)]
pub struct PyJSON {
    inner: Value,
}

impl PyJSON {
    #[must_use]
    pub fn inner(&self) -> &Value {
        &self.inner
    }
}

#[pymethods]
impl PyJSON {
    #[new]
    #[allow(clippy::missing_errors_doc)]
    pub fn new_json(value: &PyAny) -> RustPSQLDriverPyResult<Self> {
        Ok(Self {
            inner: build_serde_value(value)?,
        })
    }
}

macro_rules! build_macaddr_type {
    ($st_name:ident, $rust_type:ty) => {
        #[pyclass]
        #[derive(Clone)]
        pub struct $st_name {
            inner: $rust_type,
        }

        impl $st_name {
            #[must_use]
            pub fn inner(self) -> $rust_type {
                self.inner
            }
        }

        #[pymethods]
        impl $st_name {
            #[new]
            #[allow(clippy::missing_errors_doc)]
            pub fn new_class(value: &str) -> RustPSQLDriverPyResult<Self> {
                Ok(Self {
                    inner: <$rust_type>::from_str(value)?,
                })
            }
        }
    };
}

build_macaddr_type!(PyMacAddr6, MacAddr6);
build_macaddr_type!(PyMacAddr8, MacAddr8);

// #[pyclass]
// #[derive(Clone)]
// pub struct PyMacAddr6 {
//     inner: MacAddr6,
// }

// impl PyMacAddr6 {
//     #[must_use]
//     pub fn inner(self) -> MacAddr6 {
//         self.inner
//     }
// }

// #[pymethods]
// impl PyMacAddr6 {
//     #[new]
//     #[allow(clippy::missing_errors_doc)]
//     pub fn new_macaddr6(value: &str) -> RustPSQLDriverPyResult<Self> {
//         Ok(Self {
//             inner: MacAddr6::from_str(value)?,
//         })
//     }
// }

// #[pyclass]
// #[derive(Clone)]
// pub struct PyMacAddr8 {
//     inner: MacAddr8,
// }

// impl PyMacAddr8 {
//     #[must_use]
//     pub fn inner(self) -> MacAddr8 {
//         self.inner
//     }
// }

// #[pymethods]
// impl PyMacAddr8 {
//     #[new]
//     #[allow(clippy::missing_errors_doc)]
//     pub fn new_macaddr8(value: &str) -> RustPSQLDriverPyResult<Self> {}
// }

#[allow(clippy::module_name_repetitions)]
#[allow(clippy::missing_errors_doc)]
pub fn extra_types_module(_py: Python<'_>, pymod: &PyModule) -> PyResult<()> {
    pymod.add_class::<SmallInt>()?;
    pymod.add_class::<Integer>()?;
    pymod.add_class::<BigInt>()?;
    pymod.add_class::<PyUUID>()?;
    pymod.add_class::<PyJSON>()?;
    pymod.add_class::<PyMacAddr6>()?;
    pymod.add_class::<PyMacAddr8>()?;
    Ok(())
}
