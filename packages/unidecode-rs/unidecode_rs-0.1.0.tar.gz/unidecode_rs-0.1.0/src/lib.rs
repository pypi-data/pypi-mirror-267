use pyo3::prelude::*;
use deunicode::deunicode;


#[pyfunction]
fn decode(_py: Python, input: &str) -> PyResult<String> {
    let decoded = deunicode(input);
    Ok(decoded)
}

#[pymodule]
fn unidecode_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    Ok(())
}