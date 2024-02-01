import random

LEN_OF_ENG_ALPHABET = 26


class Permutation:
    def __init__(self, length, permutation_list=None):
        self.permutation = permutation_list
        if self.permutation is None:
            self.permutation = [i for i in range(length)]
            random.shuffle(self.permutation)

    def __mul__(self, other):
        return [other.permutation[i] for i in self.permutation]

    def __str__(self):
        return '[' + ' '.join([str(x) for x in self.permutation]) + ']'

    def inversed_permutation(self):
        """ i -> p[i], reversed p[i] -> i """
        reversed_perm = [0 for _ in range(len(self.permutation))]
        for i in range(len(self.permutation)):
            reversed_perm[self.permutation[i]] = i
        return reversed_perm


def str_to_array(text: str) -> list[int]:
    """
        convert string to array of int.
        Where each int represents index of letter in en. alphabet

        erase all non alphabet letters, and make all letters lowercased
    """
    text.lower()  # make all letters lowercased for simplicity
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


if __name__ == '__main__':
    a = Permutation(3)
    print(a)

    b = Permutation(4, [1, 3, 2, 0])
    print(b)
    print(a * b)
    print(b.inversed_permutation())

'''
[3, 1, 2]

i -> p[i] -> p[p[i]]
[2, 3, 1]
'''
