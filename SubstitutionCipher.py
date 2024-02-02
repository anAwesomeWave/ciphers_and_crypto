import helpers as hps


class SubstitutionCipher:
    def __init__(self, key=None):
        """ create a pair of keys. The key can be provided. """

        if key is None:
            self.key = hps.Permutation(hps.ALPHABET_LEN)
        else:
            self.key = hps.Permutation(key)
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
    text = 'I LOV U'
    print(f'INITIAL TEXT: {text}')
    sc = SubstitutionCipher()
    ciphertext = sc.encrypt(text)
    print(f'CIPHERTEXT: {ciphertext}')
    print(f'TEXT AFTER DECRYPTION: {sc.decrypt(ciphertext)}')
