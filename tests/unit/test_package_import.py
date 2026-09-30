import unittest


class TestPackageFoundation(unittest.TestCase):
    def test_app_package_imports(self) -> None:
        import app

        self.assertEqual(app.__name__, "app")


if __name__ == "__main__":
    unittest.main()
