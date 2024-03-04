class VigenereCipherBase:
    MOD = 29
    d = {chr(ord('a') + i): i for i in range(26)}
    d[' '] = 26
    d[','] = 27
    d['.'] = 28
    inv_d = {v: k for k, v in d.items()}

    def text_to_arr(self, text: str) -> list[int]:
        ans = []
        for c in text:
            # if c not in d:
            #     raise ValueError(f'Invalid character {c}. Must be in {list(d.keys())}')
            if c.lower() in self.d:
                ans.append(self.d[c])
        return ans

    def arr_to_text(self, arr: list[int]) -> str:
        ans = []
        for num in arr:
            if num not in self.inv_d:
                raise ValueError(f'{num} is not in {list(self.d.keys())}')
            ans.append(self.inv_d[num])
        return ''.join(ans)

    # def get_gamma(self, key: str, length) -> str:
    #


class VigenerSlogan(VigenereCipherBase):
    def __init__(self, key: str) -> None:
        self.key = self.text_to_arr(key)

    def encrypt(self, text: str) -> str:
        """Вместо того, чтобы делать лозунг нужной длины, я буду обращаться к его индексам по модулю его длины"""
        encrypted = []
        arr = self.text_to_arr(text)

        for i in range(len(arr)):
            encrypted.append(self.inv_d[(arr[i] + self.key[i % len(self.key)]) % self.MOD])  # шифрование

        return ''.join(encrypted)

    def decrypt(self, text: str) -> str:
        decrypted = []
        arr = self.text_to_arr(text)

        for i in range(len(arr)):
            decrypted.append(self.inv_d[(arr[i] - self.key[i % len(self.key)]) % self.MOD])

        return ''.join(decrypted)


class VigenereTextKey(VigenereCipherBase):
    def __init__(self, key_letter: str) -> None:
        self.key_letter = key_letter

    def get_key_for_text(self, arr: list[int]) -> list[int]:
        return [self.d[self.key_letter], *arr[:-1]]

    def encrypt(self, text: str) -> list[str]:
        """ Returns both ciphertext and generated key."""
        arr = self.text_to_arr(text)
        key = self.get_key_for_text(arr)
        encrypted = []
        print(arr)
        print(key)
        for i in range(len(arr)):
            encrypted.append(self.inv_d[(arr[i] + key[i]) % self.MOD])
        return [''.join(encrypted), self.arr_to_text(key)]

    def decrypt(self, key: str, ciphertext: str) -> str:
        arr = self.text_to_arr(ciphertext)
        key = self.text_to_arr(key)
        decrypted = []
        for i in range(len(arr)):
            decrypted.append(self.inv_d[(arr[i] - key[i]) % self.MOD])
        return ''.join(decrypted)


class VigenereCiphertextKey(VigenereCipherBase):
    def __init__(self, key_letter: str) -> None:
        self.key_letter = key_letter

    def encrypt(self, text: str) -> list[str]:
        """ Returns both ciphertext and generated key."""
        arr = self.text_to_arr(text)
        encrypted = []
        prev_key = self.d[self.key_letter]
        key = [self.key_letter, ]
        for i in range(len(arr)):
            new_char = (prev_key + arr[i]) % self.MOD
            encrypted.append(self.inv_d[new_char])
            key.append(self.inv_d[new_char])
            prev_key = new_char
        print(arr)
        print(self.text_to_arr(''.join(key)))
        print(self.text_to_arr(''.join(encrypted)))
        return [''.join(encrypted), ''.join(key)]

    def decrypt(self, key: str, ciphertext: str):
        arr = self.text_to_arr(ciphertext)
        key = self.text_to_arr(key)
        decrypted = []
        for i in range(len(arr)):
            decrypted.append(self.inv_d[(arr[i] - key[i]) % self.MOD])
        return ''.join(decrypted)


if __name__ == '__main__':
    text = 'attackatdawn'

    v_s = VigenerSlogan('ab')

    enc = v_s.encrypt(text)
    print(enc)
    print(v_s.decrypt(enc))

    v_t = VigenereTextKey('a')
    enc, key = v_t.encrypt('abacaba')
    print(enc)
    print(v_t.decrypt(key, enc))

    v_c = VigenereCiphertextKey('a')
    enc, key = v_c.encrypt('abacaba')

    print(enc)
    print(key)
    print(v_c.decrypt(key, enc))
