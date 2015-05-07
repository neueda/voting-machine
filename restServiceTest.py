import unittest

import restService


class RestServiceTest(unittest.TestCase):
    def test_valid_check_date(self):
        date_to_check = '2015-01-02'
        try:
            restService.check_date(date_to_check, 'valid date')
        except TypeError:
            self.fail('valid date raised exception')

    def test_valid_check_datetime(self):
        date_to_check = '2015-01-02 12:14:01'
        try:
            restService.check_date(date_to_check, 'valid datetime')
        except TypeError:
            self.fail('valid datetime raised exception')

    def test_invalid_check_date(self):
        date_to_check = '01-02'
        self.assertRaises(TypeError, restService.check_date, date_to_check, 'date')


if __name__ == '__main__':
    unittest.main()