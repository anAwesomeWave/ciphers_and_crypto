import numpy as np
from helpers import gcd_extended
from typing import Optional


class HillCipherBase:
    """ Базовый класс для Шифра Хилла. """
    MOD = 29
    d = {chr(ord('a') + i): i for i in range(26)}
    d[' '] = 26
    d[','] = 27
    d['.'] = 28
    inv_d = {v: k for k, v in d.items()}

    def __init__(self, chunk_len=1):
        self.chunk_len = chunk_len

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
                raise ValueError(f'{num} is not in {list(self.d.keys())}')
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

    def __encrypt_chunk__(self, x: list[int], key: np.ndarray) -> np.ndarray:
        return np.dot(key, x) % self.MOD

    def __decrypt_chunk__(self, y: list[int], inv_key: np.ndarray) -> np.ndarray:
        return np.dot(inv_key, y) % self.MOD


class HillCipher(HillCipherBase):

    def __init__(self, key: Optional[np.ndarray] = None, chunk_len=1) -> None:
        super().__init__(chunk_len)
        self.key = key
        if self.key is None:
            self.key = self.get_random_matrix()

        self.inv_key = self.inv_matrix_mod_n(self.key)
        if self.inv_key is None:
            print('Ошибка, обратная матрицы не исчеслима')
            raise ValueError
        # print(self.key)
        # print(self.inv_key)

    def encrypt(self, text: str) -> str:
        arr_from_text = self.text_to_arr(text)  # переводим text в массив
        arr_of_chunks = self.split_arr(
            arr_from_text
        )  # разделим его на куски равной длины, дополнив последний пустым символом
        ans = np.array([], dtype=int)
        for chunk in arr_of_chunks:
            ans = np.append(ans, self.__encrypt_chunk__(chunk, self.key))

        print(arr_of_chunks)
        print(ans)
        return self.arr_to_text(ans)

    def decrypt(self, ciphertext: str) -> str:
        arr_from_ciphertext = self.text_to_arr(ciphertext)
        arr_of_chunks = self.split_arr(arr_from_ciphertext)
        ans = np.array([], dtype=int)
        for chunk in arr_of_chunks:
            ans = np.append(ans, self.__decrypt_chunk__(chunk, self.inv_key))

        print(ans)
        return self.arr_to_text(ans)


class HillRecCipher(HillCipherBase):
    def __init__(self, k1: Optional[np.ndarray] = None, k2: Optional[np.ndarray] = None, chunk_len=1) -> None:
        super().__init__(chunk_len)
        self.k1 = k1
        self.k2 = k2
        if k1 is None:
            self.k1 = self.get_random_matrix()
        if k2 is None:
            self.k2 = self.get_random_matrix()
        self.dec_k1 = self.inv_matrix_mod_n(self.k1)
        self.dec_k2 = self.inv_matrix_mod_n(self.k2)
        if self.dec_k1 is None or self.dec_k2 is None:
            print('Ошибка, обратная матрицы не исчеслима')
            raise ValueError

    def encrypt(self, text: str) -> str:
        arr_from_text = self.text_to_arr(text)  # переводим text в массив
        arr_of_chunks = self.split_arr(
            arr_from_text
        )  # разделим его на куски равной длины, дополнив последний пустым символом
        ans = np.array([], dtype=int)
        cur_keys = []
        for chunk in arr_of_chunks:
            if len(cur_keys) == 0:
                ans = np.append(ans, self.__encrypt_chunk__(chunk, self.k1))
                cur_keys.append(self.k1)
            elif len(cur_keys) == 1:
                ans = np.append(ans, self.__encrypt_chunk__(chunk, self.k2))
                cur_keys.append(self.k2)
            else:
                cur_keys.append((np.dot(cur_keys[-1], cur_keys[-2]) % self.MOD))
                ans = np.append(ans, self.__encrypt_chunk__(chunk, cur_keys[-1]))
            print('ENC KEY')
            print(cur_keys[-1])

        print(ans)
        return self.arr_to_text(ans)

    def decrypt(self, ciphertext: str) -> str:
        arr_from_ciphertext = self.text_to_arr(ciphertext)
        arr_of_chunks = self.split_arr(arr_from_ciphertext)
        ans = np.array([], dtype=int)

        cur_keys = []
        for chunk in arr_of_chunks:
            if len(cur_keys) == 0:
                ans = np.append(ans, self.__decrypt_chunk__(chunk, self.dec_k1))
                cur_keys.append(self.dec_k1)
            elif len(cur_keys) == 1:
                ans = np.append(ans, self.__decrypt_chunk__(chunk, self.dec_k2))
                cur_keys.append(self.dec_k2)
            else:
                cur_keys.append((np.dot(cur_keys[-2], cur_keys[-1]) % self.MOD))
                # print('123213')
                # print(cur_keys[-1])
                ans = np.append(ans, self.__decrypt_chunk__(chunk, cur_keys[-1]))
            print('DEC KEY')
            print(cur_keys[-1])
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


def rec_example(k1, k2, n, text):
    print('HILL RECURRENT CIPHER')
    rhc = HillRecCipher(k1, k2, chunk_len=n)
    print(f'ENCRYPTION KEY 1:\n{rhc.k1}')
    # print(rhc.k1)
    print('-----')
    # print(rhc.k2)
    print(f'ENCRYPTION KEY 2:\n{rhc.k2}')
    print(f'INPUT TEXT IS {text}')
    print(f'INPUT TEXT IS {rhc.text_to_arr(text)}')
    enc = rhc.encrypt(text)

    print(f'ENCRYPTED TEXT IS {enc}')
    print(f'ENCRYPTED TEXT IS {rhc.text_to_arr(enc)}')

    print(f'DECRYPTED TEXT IS {rhc.decrypt(enc)}')


def hill_example(k, n, text):
    print(f'ENCRYPTION KEY: \n{k}')
    print('-----')
    hc = HillCipher(k, n)
    print(f'Text: {text}')

    encrypted_text = hc.encrypt(text)

    print(f'Encrypted text: {encrypted_text}')

    decrypted_text = hc.decrypt(encrypted_text)
    print('-----')
    print(f'Decryption key: \n{hc.inv_key}')
    print('-----')
    print(f'Decrypted text: {decrypted_text}')


if __name__ == '__main__':
    k = np.array([
        [1, 5, 1],
        [3, 9, 4],
        [9, 4, 6]
    ])
    hill_example(k, 3, 'concurrency')
    print('-----')
    k1 = np.array(
        [
            [4, 8],
            [2, 2]
        ]
    )
    k2 = np.array(
        [
            [5, 8],
            [1, 3]
        ]
    )
    rec_example(k1, k2, 2, 'symmetry')

    print("EX 2")
    k = np.array(
        [[7, 1, 7],
         [0, 0, 5],
         [8, 5, 8]]
    )

    hill_example(k, 3, "approve")
    k1 = np.array(
        [
            [1, 5],
            [4, 0]
        ]
    )
    k2 = np.array(
        [
            [1, 6],
            [5, 8]
        ]
    )
    rec_example(k1, k2, 2, 'constant')
