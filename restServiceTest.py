import unittest

import rfIdReader


class RfIdReaderTest(unittest.TestCase):
    def test_format(self):
        to_format = ' 19272FA912,.!\r'
        formatted = rfIdReader.format_input(to_format)

        self.assertEqual(formatted, '19272FA912')


if __name__ == '__main__':
    unittest.main()