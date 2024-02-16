import numpy as np
from helpers import gcd_extended
from typing import Optional


class HillCipher:
    MOD = 29
    d = {chr(ord('a') + i): i for i in range(26)}
    d[' '] = 26
    d[','] = 27
    d['.'] = 28
    inv_d = {v: k for k, v in d.items()}

    def __init__(self, key: Optional[np.ndarray] = None, chunk_len: int = 3) -> None:
        self.key = key
        self.chunk_len = chunk_len
        if self.key is None:
            self.key = self.get_random_matrix()

        self.inv_key = self.inv_matrix_mod_n(self.key)
        if self.inv_key is None:
            print('Ошибка, обратная матрицы не исчеслима')
            raise ValueError
        # print(self.key)
        # print(self.inv_key)

    def get_random_matrix(self) -> np.ndarray:
        arr = np.random.randint(10, size=(self.chunk_len, self.chunk_len))
        while int(round(np.linalg.det(arr))) % self.MOD == 0:
            arr = np.random.randint(10, size=(self.chunk_len, self.chunk_len))
        return arr

    def text_to_arr(self, text: str) -> list[int]:
        ans = []
        for c in text:
            # if c not in d:
            #     raise ValueError(f'Invalid character {c}. Must be in {list(d.keys())}')
            if c in self.d:
                ans.append(self.d[c])
        return ans

    def arr_to_text(self, arr: np.ndarray) -> str:
        ans = []
        for num in arr:
            if num not in self.inv_d:
                raise ValueError(f'{num} is not in {list(d.keys())}')
            ans.append(self.inv_d[num])
        return ''.join(ans)

    def split_arr(self, arr: list[int]) -> list[list[int]]:
        '''arr - array of indeces, chunk_len - size of portion'''
        ans = []
        for i in range(0, len(arr), self.chunk_len):
            # print(i, n, i + n)
            ans.append(arr[i:i + self.chunk_len])
        if len(ans[-1]) < self.chunk_len:
            ans[-1] += [-1 for _ in range(self.chunk_len - len(ans[-1]))]
        return ans

    def encrypt_chunk(self, x: list[int]) -> np.ndarray:
        return np.dot(self.key, x) % 29

    def encrypt(self, text: str) -> str:
        arr_from_text = self.text_to_arr(text)  # переводим text в массив
        arr_of_chunks = self.split_arr(
            arr_from_text
        )  # разделим его на куски равной длины, дополнив последний пустым символом
        ans = np.array([], dtype=int)
        for chunk in arr_of_chunks:
            ans = np.append(ans, self.encrypt_chunk(chunk))

        print(ans)
        return self.arr_to_text(ans)

    def matrix_minor(self, arr: np.ndarray, i: int, j: int) -> np.ndarray:
        return np.delete(np.delete(arr, i, axis=0), j, axis=1)

    # function for computing matrix inverse modulo n , input: matrix A and modulo m
    def inv_matrix_mod_n(self, matrix: np.ndarray) -> np.ndarray:
        n = len(matrix)

        # inverse = (1/detM) * adj(M) ,where adj(M) is adjugate of matrix M
        det = int(round(np.linalg.det(matrix)) % self.MOD)

        inverse_det = [0]
        inv2 = [0]
        if gcd_extended(det, self.MOD, inverse_det, inv2) != 1:
            print("БЕДА, из-за округления нод не равен 1", det, self.MOD, inverse_det, inv2, matrix)
            return None

        # calculate adjugate
        adj = np.zeros((n, n), dtype=int)
        for i in range(n):  # rows
            for j in range(n):  # columns
                # calculate cofactor of A(i,j)
                minor = self.matrix_minor(matrix, i, j)
                # use adj[j][i] - INV !!!
                adj[j][i] = int((round(
                    np.linalg.det(minor)) % self.MOD))  # определитель минора по модулю
                if (i + 1 + j + 1) % 2 == 1:
                    adj[j][i] = (-1 * adj[j][i]) % self.MOD  # алг. дополнение
        return (inverse_det * adj) % self.MOD

    def decrypt_chunk(self, y: list[int]) -> np.ndarray:
        return np.dot(self.inv_key, y) % 29

    def decrypt(self, ciphertext: str) -> str:
        arr_from_ciphertext = self.text_to_arr(ciphertext)
        arr_of_chunks = self.split_arr(arr_from_ciphertext)
        ans = np.array([], dtype=int)
        for chunk in arr_of_chunks:
            ans = np.append(ans, self.decrypt_chunk(chunk))

        print(ans)
        return self.arr_to_text(ans)


# print(y)
#
# encrypted_text = arr_to_text(y, inv_d)
# print(encrypted_text)
#
# inv_key = inv_matrix_mod_n(k, 29)
# print(inv_key)
# print('text to arr')
# print(text_to_arr(encrypted_text, d))
# encr_chunks = split_arr(text_to_arr(encrypted_text, d), 3)
#
# deciphered = np.array([], dtype=int)
# for chunk in encr_chunks:
#     deciphered = np.append(deciphered, decrypt(inv_key, chunk))
#
# print(deciphered)
#
# print(arr_to_text(deciphered, inv_d))
#
# print(text_to_arr('concurrency', d))
# chunks = split_arr(text_to_arr('concurrency', d), 3)
# k = np.array([
#     [1, 5, 1],
#     [3, 9, 4],
#     [9, 4, 6]
# ])
# y = np.array([], dtype=int)
# for chunk in chunks:
#     # print(type(encrypt(k, chunk)[0]))
#     y = np.append(y, encrypt(k, chunk))



if __name__ == '__main__':
    k = np.array([
        [1, 5, 1],
        [3, 9, 4],
        [9, 4, 6]
    ])
    print(f'ENCRYPTION KEY: \n{k}')
    print('-----')
    hc = HillCipher(k, 3)
    text = 'concurrency'
    print(f'Text: {text}')

    encrypted_text = hc.encrypt(text)

    print(f'Encrypted text: {encrypted_text}')

    decrypted_text = hc.decrypt(encrypted_text)
    print('-----')
    print(f'Decryption key: \n{hc.inv_key}')
    print('-----')
    print(f'Decrypted text: {decrypted_text}')
