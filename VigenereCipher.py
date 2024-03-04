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

if __name__ == '__main__':
    text = 'attackatdawn'

    v_s = VigenerSlogan('ab')

    enc = v_s.encrypt(text)
    print(enc)
    print(v_s.decrypt(enc))


