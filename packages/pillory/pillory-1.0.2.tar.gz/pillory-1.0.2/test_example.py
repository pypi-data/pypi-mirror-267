import doctest
import os
import pathlib
import subprocess
import tempfile
from inspect import cleandoc


def doctest_pillory():
    """
    >>> doctest_pillory()
    ... # doctest: +ELLIPSIS +REPORT_UDIFF
    F.
    ======================================================================
    FAIL: test_hey1 (__main__.UseTestCase)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: 1 != 2
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...
    <BLANKLINE>
    FAILED (failures=1)
    <BLANKLINE>
    .../test_use.py... PM101 ...
    .../test_use.py... PM102 ...
    .../test_use.py... PM103 ...
    """
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp:
        tmp_path = pathlib.Path(tmp)
        def_path = tmp_path / "definition.py"
        def_path.write_text(
            cleandoc(
                """
                class Hey:
                    def yo(self):
                        return 1
                """
            )
        )
        use_path = tmp_path / "use.py"
        use_path.write_text(
            cleandoc(
                f"""
                from {tmp_path.name}.definition import Hey

                def do_something():
                    value = Hey().yo()
                    print(value)
                    return value
                """
            )
        )
        test_path = tmp_path / "test_use.py"
        test_path.write_text(
            cleandoc(
                f"""
                import unittest
                import unittest.mock

                from {tmp_path.name} import use

                @unittest.mock.patch("builtins.print")
                class UseTestCase(unittest.TestCase):
                    @unittest.mock.patch("{tmp_path.name}.definition.Hey")
                    def test_hey1(self, hey, print):
                        hey.return_value.yo.return_value = 2
                        self.assertEqual(use.do_something(), 2)

                    @unittest.mock.patch("{tmp_path.name}.definition.Hey.yo")
                    def test_hey2(self, yo, print):
                        yo.return_value = 3
                        self.assertEqual(use.do_something(), 3)

                if __name__ == "__main__":
                    unittest.main()
                """
            )
        )
        (tmp_path / "__init__.py").touch()
        unit_proc = subprocess.run(
            ["python", "-m", f"{tmp_path.name}.test_use"],
            capture_output=True,
            text=True,
        )
        print(unit_proc.stderr)
        pillory_proc = subprocess.run(
            ["python", "-m", "pillory", str(tmp_path.relative_to(os.getcwd()))],
            capture_output=True,
            text=True,
        )
        print(pillory_proc.stdout)


if __name__ == "__main__":
    fail_count, test_count = doctest.testmod()
    if fail_count > 0:
        raise SystemExit(1)
    if test_count == 0:
        raise SystemExit("no doctests found")
