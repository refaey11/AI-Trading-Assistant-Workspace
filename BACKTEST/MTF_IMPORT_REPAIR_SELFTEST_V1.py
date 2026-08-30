import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('acquire', Path(__file__).with_name('CIRCLECI_ACQUIRE_GOVERNED_SOURCES.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.pd is not None
print('MTF_IMPORT_REPAIR_SELFTEST=PASS')
