import random

ALPHABET_LEN = 26


class Permutation:
    def __init__(self, length=0, permutation_list=None):
        if length == 0 and permutation_list is None:
            raise TypeError('''
                На вход ожидался хотя бы один из аргументов: 'length', 'permutation_list'
            ''')

        self.permutation = permutation_list
        if self.permutation is None:
            self.permutation = [i for i in range(length)]
            random.shuffle(self.permutation)

    def __mul__(self, other):
        return [other.permutation[i] for i in self.permutation]

    def __str__(self):
        return '[' + ' '.join([str(x) for x in self.permutation]) + ']'

    def inverse_permutation(self):
        """ i -> p[i], reversed p[i] -> i """
        reversed_perm = [0 for _ in range(len(self.permutation))]
        for i in range(len(self.permutation)):
            reversed_perm[self.permutation[i]] = i
        return Permutation(len(reversed_perm), reversed_perm)


def str_to_array(text: str) -> list[int]:
    """
        convert string to array of int.
        Where each int represents index of letter in en. alphabet

        erase all non alphabet letters, and make all letters lowercased
    """
    text = text.lower()  # make all letters lowercased for simplicity
    symbols = []
    for sym in text:
        if sym.isalpha():
            symbols.append(ord(sym) - ord('a'))
    return symbols


def arr_to_str(arr: list[int]) -> str:
    """
    inverse operation to "str_to_array" func.
    convert an array of letters' indices to string
    """
    ans = []
    for ind in arr:
        ans.append(chr(ind + ord('a')))  # TODO: могу создать словарь, где 26-28 символы будут ' ', ',', '.'
    return ''.join(ans)


def gcd(x, y):
    if x == 0:
        return y
    return gcd(y % x, x)


def gcd_extended(a: int, b: int, x: list[int], y: list[int]):
    """https://e-maxx.ru/algo/diofant_2_equation"""

    # x and y are lists, bcs I want to change them inside function
    if a == 0:
        x[0] = 0
        y[0] = 1
        return b
    x1, y1 = [0], [0]
    d = gcd_extended(b % a, a, x1, y1)
    x[0] = y1[0] - (b // a) * x1[0]
    y[0] = x1[0]
    return d


if __name__ == '__main__':
    a = Permutation(3)
    print(a)

    b = Permutation(4, [1, 3, 2, 0])
    print(b)
    print(a * b)
    print(b.inverse_permutation())

    a = [0]
    b = [0]
    print(gcd_extended(9, 26, a, b))
    print(a)
'''
[3, 1, 2]

i -> p[i] -> p[p[i]]
[2, 3, 1]
'''
