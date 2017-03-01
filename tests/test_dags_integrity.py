"""Test integrity of dags."""

import importlib
import os

import pytest
from airflow import models as af_models

DAG_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'dags'
)

DAG_FILES = [f for f in os.listdir(DAG_PATH) if f.endswith('.py')]

# Run this integrity check for each python file, sample_good.py, sample_bad.py, sample_nodag.py
@pytest.mark.parametrize('dag_file', DAG_FILES)
def test_dag_integrity(dag_file):
    """Import dag files and check for DAG."""
    # Get the name of the file, without the extension
    module_name, _ = os.path.splitext(dag_file)
    
    # Get the path to the dag file
    module_path = os.path.join(DAG_PATH, dag_file)
    
    # Extract the specification of the module
    # ModuleSpec(name='sample_nodag', loader=<_frozen_importlib_external.SourceFileLoader object at 0x1012b32e8>, origin='../dags/sample_nodag.py')
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    
    # Extract the module itself:
    # <module 'sample_nodag' from '../dags/sample_nodag.py'>
    module = importlib.util.module_from_spec(mod_spec)
    
    # Execute the module itself
    mod_spec.loader.exec_module(module)
    
    # Check if the DAG exists within the module
    assert any(
        isinstance(var, af_models.DAG)
        for var in vars(module).values())
