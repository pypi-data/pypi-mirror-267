import unittest
from inspect import cleandoc

import pillory


class PilloryTestCase(unittest.TestCase):
    def test_find_errors(self):
        self.assertEqual(
            list(
                pillory.find_errors(
                    cleandoc(
                        """
                        patch("builtins.open")
                        """
                    )
                )
            ),
            [("PM103", 1, 0, "builtins.open")],
        )


if __name__ == "__main__":
    unittest.main()
