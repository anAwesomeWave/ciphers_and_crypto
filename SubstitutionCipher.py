import helpers as hps


class SubstitutionCipher:
    def __init__(self, key=None):
        """ create a pair of keys. The key can be provided. """

        self.key = key
        if key is None:
            self.key = hps.Permutation(hps.LEN_OF_ENG_ALPHABET)
        self.decryption_key = self.key.inversed_permutation()

    def encrypt(self, text):
        pass

    def decrypt(self, ciphertext):
        pass


if __name__ == '__main__':
    s = 'abacaba'
    sc = SubstitutionCipher()
    print(hps.str_to_array(s))
