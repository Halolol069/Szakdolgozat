import unittest
import os
import importlib

class TestPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin_folder = "Controller/plugins"

    def test_plugin_foldes_exists(self):
        self.assertTrue(os.path.exists(self.plugin_folder), "Plugin mappa nem található!")

    def test_plugin_have_register_method(self):
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]

                module = importlib.import_module(f"Controller.plugins.{module_name}")

                self.assertTrue(
                    hasattr(module, "register"),
                    f"Hiba: A(z) '{module_name}' plugin nem tartalmazza a 'register' nevű függvényt!"
                )
if __name__ == "__main__":
    unittest.main()