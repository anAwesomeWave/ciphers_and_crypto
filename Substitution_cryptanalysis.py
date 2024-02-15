import json
import random

from SubstitutionCipher import SubstitutionCipher
import helpers as hps
import cryptanalysis_helpers as crypta_hps


def break_substitution(freq_native, ciphertext):
    """ Поиск ключа дешифования (обратного ключу шифрования)
        Алгоритм:
            1. Выбирается случайная последовательность букв — основной ключ. Шифртекст расшифровывается
            с помощью основного ключа. Для получившегося текста вычисляется коэффициент,
            характеризующий вероятность принадлежности к естественному языку.

            2. Основной ключ подвергается небольшим изменениям (перестановка двух произвольно выбранных букв).
            Производится расшифровка и вычисляется коэффициент полученного текста.

            3. Если коэффициент выше сохраненного значения, то основной ключ заменяется на модифицированный вариант.

            4. Шаги 2-3 повторяются пока коэффициент не станет постоянным.
        функция возвращает ключ дешифрования
    """
    # 1. генерируем рандомный ключ
    parent_key = hps.Permutation(length=hps.ALPHABET_LEN)
    # вычисляем score перестановки
    parent_score = crypta_hps.cost_function(
        freq_native,
        crypta_hps.freq_analysis_of_text(SubstitutionCipher(parent_key.permutation).decrypt(ciphertext))
        # дешифруем шифртекст с помощью данной перестновки, берем частотный анализ и смотрим на значение
        # cost_function
    )
    flag = True
    while flag:
        print(f'Current encr. key: {parent_key}')
        print(f'It\'s score {parent_score}')
        best_child_score = parent_score  # храним лучший score порожденной перестановки
        best_child_key = None
        flag = False
        for _ in range(2000):
            # меняем позиции 2 элементов
            child_key_list = parent_key.permutation[:]
            ind_a, ind_b, = random.randint(0, hps.ALPHABET_LEN - 1), random.randint(0, hps.ALPHABET_LEN - 1)
            child_key_list[ind_a], child_key_list[ind_b] = child_key_list[ind_b], child_key_list[ind_a]

            child_key = hps.Permutation(permutation_list=child_key_list)

            child_score = crypta_hps.cost_function(
                freq_native,
                crypta_hps.freq_analysis_of_text(
                    SubstitutionCipher(child_key.permutation).decrypt(ciphertext))
                # дешифруем шифртекст с помощью данной перестновки, берем частотный анализ и смотрим на значение
                # cost_function
            )
            if child_score > parent_score:
                parent_key = child_key
                parent_score = child_score
                flag = True
                break
    return parent_key


if __name__ == '__main__':
    text = '''On an exceptionally hot evening early in July a young man came out of
the garret in which he lodged in S. Place and walked slowly, as though
in hesitation, towards K. bridge.

He had successfully avoided meeting his landlady on the staircase. His
garret was under the roof of a high, five-storied house and was more
like a cupboard than a room. The landlady who provided him with garret,
dinners, and attendance, lived on the floor below, and every time
he went out he was obliged to pass her kitchen, the door of which
invariably stood open. And each time he passed, the young man had a
sick, frightened feeling, which made him scowl and feel ashamed. He was
hopelessly in debt to his landlady, and was afraid of meeting her.

This was not because he was cowardly and abject, quite the contrary; but
for some time past he had been in an overstrained irritable condition,
verging on hypochondria. He had become so completely absorbed in
himself, and isolated from his fellows that he dreaded meeting, not
only his landlady, but anyone at all. He was crushed by poverty, but the
anxieties of his position had of late ceased to weigh upon him. He had
given up attending to matters of practical importance; he had lost all
desire to do so. Nothing that any landlady could do had a real terror
for him. But to be stopped on the stairs, to be forced to listen to her
trivial, irrelevant gossip, to pestering demands for payment, threats
and complaints, and to rack his brains for excuses, to prevaricate, to
lie--no, rather than that, he would creep down the stairs like a cat and
slip out unseen.'''
    native_freq = json.loads(open('freq_analysis_Crime_And_Punishment.json').read())
    sc = SubstitutionCipher()
    print(f'INITIAL TEXT: {text[0:70]}...')
    print(f"ENCRYPTION KEY: {sc.key}")
    print(f"DECRYPTION KEY: {sc.decryption_key}")
    encrypted_text = sc.encrypt(text)
    print(f'ENCRYPTED TEXT: {encrypted_text[0:70]}...')
    encr_key = break_substitution(native_freq, encrypted_text)
    print(f'POSSIBLE ENCRYPTION_KEY: {encr_key}')
    print(f'POSSIBLE DECRYPTION_KEY: {encr_key.inverse_permutation()}')
    break_sc = SubstitutionCipher(key=encr_key.permutation)
    print(f'DECRYPTED TEXT: {break_sc.decrypt(encrypted_text)}')
