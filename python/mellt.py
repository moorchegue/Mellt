# coding: utf-8

import os


class Mellt:

    # Originally these were character sets with increasing complexity.
    # However it may not be a good idea to rely on such logic, as hacker might
    # try different combinations of base sets.
    # In other words we should not assume that if user employed special
    # characters, he used numbers and letters as well, or if capitalized letters
    # were used, set of non-capitalized letters should be included.
    # Same with non-latin alphabets and other character sets potentially.
    character_sets = [
        "0123456789",
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "!@#$%^&*()-=_+",
        " []\"{}|;':,./<>?`~",
        'абвгдеёжзийклмнопрстуфхцчшщьыъэюя',
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ',
    ]

    def __init__(self, hashes_per_second=100000000):
        self._hashes_per_second = hashes_per_second

    def _get_char_set(self, password):
        if not password:
            return ''

        detected_sets = set()
        for character_set in self.character_sets:
            if set(password).intersection(set(character_set)):
                detected_sets.add(character_set)

        if detected_sets:
            return ''.join(sorted(detected_sets))
        else:
            # XXX: this might be a poor assumption.
            # E.g. Hebrew only includes 22 letters or Rotokas — 11.
            return ''.join(sorted(self.character_sets))

    def _check_common(self, password):
        password = password.lower()
        here = os.path.abspath(os.path.dirname(__file__))
        for line in open(os.path.join(here, 'common-passwords.txt'), 'r'):
            line = line.rstrip()
            if password == line:
                return True
        return False

    def _brute_force_days(self, password):
        base = self._get_char_set(password)
        pass_list = list(password)
        # Starting at the first character, figure out it's position in the
        # character set and how many attempts will take to get there. For
        # example, say your password was an integer (a bank card PIN number for
        # example): 0 (or 0000 if you prefer) would be the very first password
        # they attempted by the attacker.  9999 would be the last password they
        # attempted (assuming 4 characters).  Thus a password/PIN of 6529 would
        # take 6529 attempts until the attacker found the proper combination.
        # The same logic words for alphanumeric passwords, just with a larger
        # number of possibilities for each position in the password. The key
        # thing to note is the attacker doesn't need to test the entire range
        # (every possible combination of all characters) they just need to get
        # to the point in the list of possibilities that is your password. They
        # can (in this example) ignore anything between 6530 and 9999. Using
        # this logic, 'aaa' would be a worse password than 'zzz', because the
        # attacker would encounter 'aaa' first.
        attempts = 0
        characters_in_base = len(base)
        characters_in_password = len(password)
        position = 0
        for position in range(0, characters_in_password):
            # We power up to the reverse position in the string. For example, if
            # we're trying to hack the 4 character PING code in the example
            # above: First number * (number of characters possible in the
            # charset ^ length of password) ie: 6 * (10^4) = 6000 then add that
            # same equation for the second number: 5 * (10^3) = 500 then the
            # third numbers 2 * (10^2) = 20 and add on the last number 9 Totals:
            # 6000 + 500 + 20 + 9 = 6529 attempts before we encounter the
            # correct password.
            power_of = characters_in_password - position - 1
            # Character position within the base set. We add one on because
            # strpos is base 0, we want base 1.
            try:
                characters_at_position = base.index(pass_list[position]) + 1
            except ValueError:
                characters_at_position = len(base)

            # If we're at the last character, simply add it's position in the
            # character set this would be the "9" in the pin code example above.
            if power_of == 0:
                attempts = attempts + characters_at_position
            # Otherwise we need to iterate through all the other characters
            # positions to get here. For example, to find the 5 in 25 we can't
            # just guess 2 and then 5 (even though Hollywood seems to insist
            # this is possible), we need to try 0,1, 2,3...15,16,17...23,24,25
            # (got it).
            else:
                # This means we have to try every combination of values up to
                # this point for all previous characters. Which means we need to
                # iterate through the entire character set, X times, where X is
                # our position -1. Then we need to multiply that by this
                # character's position.  Multiplier is the (10^4) or (10^3), etc
                # in the pin code example above.
                multiplier = pow(characters_in_base, power_of)
                # New attempts is the number of attempts we're adding for this
                # position.
                new_attempts = characters_at_position * multiplier
                # Add that on to our existing number of attempts.
                attempts = attempts + new_attempts
        # We can (worst case) try a billion passwords a second. Calculate how
        # many days it will take us to get to the password.
        per_day = self._hashes_per_second * 60 * 60 * 24
        # This allows us to calculate a number of days to crack. We use days
        # because anything that can be cracked in less than a day is basically
        # useless, so there's no point in having a smaller granularity (hours
        # for example).
        days = attempts / per_day

        # If it's going to take more than a billion days to crack, just return a
        # billion. This helps when code outside this function isn't using
        # bcmath. Besides, if the password can survive 2.7 million years it's
        # probably ok for now.
        if days > 1000000000:
            return 1000000000

        return round(days)

    def check_password(self, password):
        if password is '':
            return -1
        if self._check_common(password):
            return -1
        return self._brute_force_days(password)
