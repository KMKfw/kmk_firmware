import os

from tests.mocks import init_circuit_python_modules_mocks

init_circuit_python_modules_mocks()


def load_tests(loader, standard_tests, pattern):
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern='test*.py')
    standard_tests.addTests(package_tests)
    return standard_tests
