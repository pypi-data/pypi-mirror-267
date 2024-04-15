use pyo3::prelude::*;
use std::env;

#[pyfunction]
fn version() -> PyResult<String> {
    let version = env!("CARGO_PKG_VERSION");
    Ok((version).to_string())
}

#[pyclass]
struct Core {}

#[pymethods]
impl Core {

    #[new]
    fn new() -> Self {
        Core {}
    }

    #[staticmethod]
    pub fn extract_page() -> PyResult<&'static str> {
        Ok("foi")
    }
}

#[pymodule]
fn pylazypdfcore(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_class::<Core>()?;

    Ok(())
}
