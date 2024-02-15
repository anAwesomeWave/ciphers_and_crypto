import numpy as np


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
        print(i, n, i + n)
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
    print(type(encrypt(k, chunk)[0]))
    y = np.append(y, encrypt(k, chunk))

print(y)

print(arr_to_text(y, inv_d))