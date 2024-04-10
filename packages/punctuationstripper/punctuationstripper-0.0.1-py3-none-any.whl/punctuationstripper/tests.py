import unittest
from punctuationstripper.punctuation_stripper import stripper

class TestPunctuationStripper(unittest.TestCase):

    def test_strip_all_punctuation(self):
        text = "This is a test, of the: punctuation stripper."
        expected = "This is a test of the punctuation stripper"
        actual = stripper(text)
        self.assertEqual(actual, expected)

    def test_strip_specific_punctuation(self):
        text = "This is a test, of the: punctuation stripper."
        expected = "This is a test, of the punctuation stripper."
        actual = stripper(text, punct=",.")
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
