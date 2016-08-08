import unittest
import mellt


class TestMellt(unittest.TestCase):

    def test_char_set_single_number(self):
        m = mellt.Mellt()
        password = '1'
        self.assertEqual(set('0123456789'), set(m._get_char_set(password)))

    def test_char_set_single_letter(self):
        m = mellt.Mellt()
        password = 'a'
        self.assertEqual(set('abcdefghijklmnopqrstuvwxyz'), set(m._get_char_set(password)))

    def test_char_set_single_funny_character(self):
        m = mellt.Mellt()
        password = '$'
        self.assertEqual(set("!@#$%^&*()-=_+"), set(m._get_char_set(password)))

    def test_char_set_single_extra_funny_character(self):
        m = mellt.Mellt()
        password = '['
        self.assertEqual(set(" []\"{}|;':,./<>?`~"), set(m._get_char_set(password)))

    def test_char_set_multiple_numbers(self):
        m = mellt.Mellt()
        password = '1234567890'
        self.assertEqual(set('0123456789'), set(m._get_char_set(password)))

    def test_char_set_alphanum_numbers(self):
        m = mellt.Mellt()
        password = 'abc123'
        self.assertEqual(set('abcdefghijklmnopqrstuvwxyz0123456789'), set(m._get_char_set(password)))

    def test_char_set_multiple_funny_characters(self):
        m = mellt.Mellt()
        password = 'asdva98dfv79au******&^*&^&^$##%$#@*&'
        self.assertEqual(set("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=_+"), set(m._get_char_set(password)))

    def test_char_set_multiple_extra_funny_characters(self):
        m = mellt.Mellt()
        password = 'abc123[][][\][ap[sdfp][pasd]f[a9sdf7989*&^*&^%&'
        self.assertEqual(set("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=_+ []\"{}|;':,./<>?`~"), set(m._get_char_set(password)))

    def test_first_common(self):
        m = mellt.Mellt()
        password = 'password'
        self.assertTrue(m._check_common(password))

    def test_last_common(self):
        m = mellt.Mellt()
        password = 'eyphed'
        self.assertTrue(m._check_common(password))

    def test_not_common(self):
        m = mellt.Mellt()
        password = 'pass123$'
        self.assertFalse(m._check_common(password))

    def test_short_brute_force(self):
        m = mellt.Mellt()
        password = 'pass123$'
        self.assertEquals(4, m._brute_force_days(password))

    def test_max_brute_force_common(self):
        m = mellt.Mellt()
        password = 'this-password-is-really-really-long'
        self.assertEquals(1000000000, m._brute_force_days(password))

    def test_check_empty_password(self):
        m = mellt.Mellt()
        password = ''
        self.assertEquals(-1, m.check_password(password))

    def test_check_common_password(self):
        m = mellt.Mellt()
        password = 'password'
        self.assertEquals(-1, m.check_password(password))

    def test_four_day_password(self):
        m = mellt.Mellt()
        password = 'pass123$'
        self.assertEquals(4, m.check_password(password))

    def test_113_days_password(self):
        m = mellt.Mellt()
        password = 'passwD2$'
        self.assertEquals(113, m.check_password(password))

    def test_long_crack_password(self):
        m = mellt.Mellt()
        password = 'correcthorsebatterystaple'  # https://xkcd.com/936/
        self.assertEquals(1000000000, m.check_password(password))

if __name__ == '__main__':
    unittest.main()
