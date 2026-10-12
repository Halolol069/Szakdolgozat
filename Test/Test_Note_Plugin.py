import os
import unittest

from Controller.plugins.note_plugin import write_note_file, read_notes_file


class TestNotePlugin(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_temp_note.txt"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_and_read_note(self):
        test_text = "Ez egy automatizált teszt jegyzet. Második sor."

        write_note_file(test_text, filepath=self.test_file)

        self.assertTrue(os.path.exists(self.test_file))

        read_text = read_notes_file(filepath=self.test_file)
        self.assertEqual(test_text,read_text)

    def test_read_none_exist_file(self):
        content = read_notes_file(filepath="none.txt")
        self.assertEqual(content, "")

if __name__ == "__main__":
    unittest.main()