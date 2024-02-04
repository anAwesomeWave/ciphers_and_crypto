from random import randint, choice
from collections import deque

import helpers as hps

MOD = hps.ALPHABET_LEN


class AffineCipher:
    def __init__(self, key_a=None, key_b=None):
        self.key_a = key_a
        self.key_b = key_b

        if self.key_a is None:
            self.key_a = choice([x for x in range(2, MOD) if hps.gcd(MOD, x) == 1])
        if self.key_b is None:
            self.key_b = randint(0, MOD - 1)  # random num from [0, MOD)
        self.decryption_key_a = self.__get_decryption_key__(self.key_a)

    def __get_decryption_key__(self, key):
        """ initialize decryption key based on self.key_a and MOD"""

        '''
            decryption: gcd(key_a, MOD) = 1 -> по т. Безу 
                key_a * x + MOD * y = 1 https://e-maxx.ru/algo/reverse_element
                но % MOD, key_a * x = 1 (mod MOD)
                x - обратное к key_a 
        '''

        inv1 = [0]
        inv2 = [0]
        if hps.gcd_extended(key, MOD, inv1, inv2) != 1:
            raise ValueError

        return inv1[0] % MOD

    def encrypt(self, text):
        arr = hps.str_to_array(text)
        ans = []
        for i in arr:
            ans.append((i * self.key_a + self.key_b) % MOD)
        return hps.arr_to_str(ans)

    def decrypt(self, ciphertext):
        arr = hps.str_to_array(ciphertext)
        ans = []
        for i in arr:
            ans.append((self.decryption_key_a * (i - self.key_b)) % MOD)
        return hps.arr_to_str(ans)


class AffineRecCipher(AffineCipher):
    def __init__(self, key_a1=None, key_b1=None, key_a2=None, key_b2=None):
        super().__init__(key_a1, key_b1)
        # initialize second pair of keys
        self.key_a2 = key_a2
        self.key_b2 = key_b2
        if self.key_a2 is None:
            self.key_a2 = choice([x for x in range(2, MOD) if hps.gcd(MOD, x) == 1])
        if self.key_b2 is None:
            self.key_b2 = randint(0, MOD - 1)  # random num from [0, MOD)

    def encrypt(self, plaintext):
        arr = hps.str_to_array(plaintext)
        ans = []
        prev_keys = deque()
        for ind, char in enumerate(arr):
            if ind == 0:
                ans.append((char * self.key_a + self.key_b) % MOD)
                prev_keys.append((self.key_a, self.key_b))
            elif ind == 1:
                ans.append((char * self.key_a2 + self.key_b2) % MOD)
                prev_keys.append((self.key_a2, self.key_b2))
            else:
                old_keys = prev_keys.popleft()
                new_keys = ((old_keys[0] * prev_keys[-1][0]) % MOD, (old_keys[1] + prev_keys[-1][1]) % MOD)
                ans.append((char * new_keys[0] + new_keys[1]) % MOD)
                prev_keys.append(new_keys)
            print(prev_keys)
        return hps.arr_to_str(ans)

    def decrypt(self, ciphertext):
        arr = hps.str_to_array(ciphertext)
        ans = []
        prev_keys = deque()
        for ind, char in enumerate(arr):
            print(prev_keys)
            if ind == 0:
                decryption_key = self.__get_decryption_key__(self.key_a)
                prev_keys.append((decryption_key, self.key_b))
                ans.append(((char - self.key_b) * decryption_key) % MOD)
            elif ind == 1:
                decryption_key = self.__get_decryption_key__(self.key_a2)
                prev_keys.append((decryption_key, self.key_b2))
                ans.append(((char - self.key_b2) * decryption_key) % MOD)
            else:
                old_keys = prev_keys.popleft()
                new_keys = ((old_keys[0] * prev_keys[-1][0]) % MOD, (old_keys[1] + prev_keys[-1][1]) % MOD)
                ans.append(((char - new_keys[1]) * new_keys[0]) % MOD)
                prev_keys.append(new_keys)
        print(ans)
        return hps.arr_to_str(ans)


if __name__ == '__main__':
    # ac = AffineCipher()
    # print(ac.key_a)
    # print(ac.key_b)
    # print(ac.decryption_key_a)
    # s = 'iloveuа'
    # cs = ac.encrypt(s)
    # print(cs)
    # print(ac.decrypt(cs))
    # print('---------')
    # arc = AffineRecCipher()
    # print(arc.key_a)
    # print(arc.key_a2)
    # print(arc.key_b)
    # print(arc.key_b2)
    #
    # cs = arc.encrypt(s)
    # print(cs)
    #
    # print(arc.decrypt(cs))
    ac = AffineRecCipher(1, 2, 3, 1)
    text = "palindrome"
    ct =ac.encrypt(text)
    print(ct)
    print(ac.decrypt(ct))
    # print(ac.key_a)
    # print(ac.decryption_key_a)