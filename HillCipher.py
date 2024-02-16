import numpy as np
from helpers import gcd_extended


def get_random_matrix():
    arr = np.random.randint(10, size=(3, 3))
    while np.linalg.det(arr) % 29 == 0:
        arr = np.random.randint(10, size=(3, 3))
    return arr


# print(arr, np.linalg.det(arr))

d = {chr(ord('a') + i): i for i in range(26)}
d[' '] = 26
d[','] = 27
d['.'] = 28
print(d)

inv_d = {v: k for k, v in d.items()}


def text_to_arr(text, d):
    ans = []
    for c in text:
        # if c not in d:
        #     raise ValueError(f'Invalid character {c}. Must be in {list(d.keys())}')
        if c in d:
            ans.append(d[c])
    return ans


def arr_to_text(arr, inv_d):
    ans = []
    for num in arr:
        if num not in inv_d:
            raise ValueError(f'{num} is not in {list(d.keys())}')
        ans.append(inv_d[num])
    return ''.join(ans)


print(text_to_arr('concurrency', d))


def split_arr(arr, n):
    '''arr - array of indeces, n - size of portion'''
    ans = []
    for i in range(0, len(arr), n):
        # print(i, n, i + n)
        ans.append(arr[i:i + n])
    if len(ans[-1]) < n:
        ans[-1] += [-1 for _ in range(n - len(ans[-1]))]
    return ans


chunks = split_arr(text_to_arr('concurrency', d), 3)


def encrypt(k, x):
    return np.dot(k, x) % 29


k = np.array([
    [1, 5, 1],
    [3, 9, 4],
    [9, 4, 6]
])
y = np.array([], dtype=int)
for chunk in chunks:
    # print(type(encrypt(k, chunk)[0]))
    y = np.append(y, encrypt(k, chunk))

print(y)

encrypted_text = arr_to_text(y, inv_d)
print(encrypted_text)


def matrix_minor(arr, i, j):
    return np.delete(np.delete(arr, i, axis=0), j, axis=1)


# function for computing matrix inverse modulo n , input: matrix A and modulo m
def inv_matrix_mod_n(matrix, mod):
    n = len(matrix)

    # inverse = (1/detM) * adj(M) ,where adj(M) is adjugate of matrix M
    det = int(round(np.linalg.det(matrix)) % mod)

    inverse_det = [0]
    inv2 = [0]
    if gcd_extended(det, mod, inverse_det, inv2) != 1:
        print("БЕДА, из-за округления нод не равен 1", det, mod, inverse_det, inv2, matrix)
        return None

    # calculate adjugate
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):  # rows
        for j in range(n):  # columns
            # calculate cofactor of A(i,j)
            minor = matrix_minor(matrix, i, j)
            # use adj[j][i] - INV !!!
            adj[j][i] = int((round(
                np.linalg.det(minor)) % mod))  # определитель минора по модулю
            if (i + 1 + j + 1) % 2 == 1:
                adj[j][i] = (-1 * adj[j][i]) % mod  # алг. дополнение
    return (inverse_det * adj) % mod


inv_key = inv_matrix_mod_n(k, 29)
print(inv_key)
print('text to arr')
print(text_to_arr(encrypted_text, d))
encr_chunks = split_arr(text_to_arr(encrypted_text, d), 3)


def decrypt(inv_key, y):
    return np.dot(inv_key, y) % 29


deciphered = np.array([], dtype=int)
for chunk in encr_chunks:
   deciphered = np.append(deciphered, decrypt(inv_key, chunk))

print(deciphered)

print(arr_to_text(deciphered, inv_d))
