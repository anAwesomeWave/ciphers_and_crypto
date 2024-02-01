import helpers as hps


class SubstitutionCipher:
    def __init__(self, key=None):
        """ create a pair of keys. The key can be provided. """

        self.key = key
        if key is None:
            self.key = hps.Permutation(hps.LEN_OF_ENG_ALPHABET)
        self.decryption_key = self.key.inversed_permutation()

    def encrypt(self, text):
        # Transform text to vector of indices
        # Multiply it by key
        # Transform this vector to ciphertext
        arr = hps.str_to_array(text)  # transform text to array
        arr = hps.Permutation(len(arr), arr)  # transform array to Permutation instance
        return hps.arr_to_str(arr * self.key)  # return ciphertext

    def decrypt(self, ciphertext):
        arr = hps.str_to_array(ciphertext)
        return hps.arr_to_str(hps.Permutation(len(arr), arr) * self.decryption_key)


if __name__ == '__main__':
    text = 'abacaba'
    print(f'INITIAL TEXT: {text}')
    sc = SubstitutionCipher()
    ciphertext = sc.encrypt(text)
    print(f'CIPHERTEXT: {ciphertext}')
    print(f'TEXT AFTER DECRYPTION: {sc.decrypt(ciphertext)}')
