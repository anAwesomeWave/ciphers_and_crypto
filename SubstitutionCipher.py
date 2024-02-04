import helpers as hps


class SubstitutionCipher:
    def __init__(self, key=None):
        """ create a pair of keys. The key can be provided. """

        if key is None:
            self.key = hps.Permutation(hps.ALPHABET_LEN)
        else:
            self.key = hps.Permutation(permutation_list=key)
        self.decryption_key = self.key.inverse_permutation()

    def encrypt(self, text):
        # Transform text to vector of indices
        # Multiply it by key
        # Transform this vector to ciphertext
        # 1. transform text to array
        arr = hps.Permutation(permutation_list=hps.str_to_array(text))  # 2. transform array to Permutation instance
        return hps.arr_to_str(arr * self.key)  # 3. return ciphertext

    def decrypt(self, ciphertext):
        return hps.arr_to_str(hps.Permutation(
            permutation_list=hps.str_to_array(ciphertext)) * self.decryption_key
        )


if __name__ == '__main__':
    text = 'anagram'
    print(f'INITIAL TEXT: {text}')
    sc = SubstitutionCipher([6, 2, 1, 7, 15, 3, 5, 4, 23, 9, 13, 8, 12, 25, 16, 11, 17, 19, 22, 14, 18, 21, 0, 10, 20, 24])
    print(f"KEY: {sc.key}")
    ciphertext = sc.encrypt(text)
    print(f'CIPHERTEXT: {ciphertext}')
    print(f'DECRYPTION KEY: {sc.decryption_key}')
    print(f'TEXT AFTER DECRYPTION: {sc.decrypt(ciphertext)}')
