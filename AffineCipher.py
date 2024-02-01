from random import randint, choice

import helpers as hps

MOD = hps.ALPHABET_LEN


class AffineCipher:
    def __init__(self, key_a=None, key_b=None):
        self.key_a = key_a
        self.key_b = key_b

        '''
            decryption: gcd(key_a, MOD) = 1 -> по т. Безу 
                key_a * x + MOD * y = 1 https://e-maxx.ru/algo/reverse_element
                но % MOD, key_a * x = 1 (mod MOD)
                x - обратное к key_a 
        '''

        if self.key_a is None:
            self.key_a = choice([x for x in range(2, MOD) if hps.gcd(MOD, x) == 1])
        if self.key_b is None:
            self.key_b = randint(0, MOD - 1)  # random num from [0, MOD)

        inv1 = [0]
        inv2 = [0]
        if hps.gcd_extended(self.key_a, MOD, inv1, inv2) != 1:
            raise ValueError

        self.decryption_key_a = inv1[0] % MOD

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


if __name__ == '__main__':
    ac = AffineCipher()
    print(ac.key_a)
    print(ac.key_b)
    print(ac.decryption_key_a)
    s = 'abacaba'
    cs = ac.encrypt(s)
    print(cs)
    print(ac.decrypt(cs))
