from bookworm import __main__ as main
# pyright: reportWildcardImportFromLibrary=false
from hamcrest import *

def test_should_run_main():
    assert_that(main.main(), equal_to(0))

