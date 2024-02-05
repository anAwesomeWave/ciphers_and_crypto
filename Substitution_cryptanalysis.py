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
        crypta_hps.freq_analysis_of_text(SubstitutionCipher(parent_key.inverse_permutation().permutation).decrypt(ciphertext))
        # дешифруем шифртекст с помощью данной перестновки, берем частотный анализ и смотрим на значение
        # cost_function
    )
    flag = True
    while flag:
        best_child_score = parent_score  # храним лучший score порожденной перестановки
        best_child_key = None
        for _ in range(1000):
            # меняем позиции 2 элементов
            child_key_list = parent_key.permutation[:]
            ind_a, ind_b, = random.randint(0, hps.ALPHABET_LEN - 1), random.randint(0, hps.ALPHABET_LEN - 1)
            child_key_list[ind_a], child_key_list[ind_b] = child_key_list[ind_b], child_key_list[ind_a]

            child_key = hps.Permutation(permutation_list=child_key_list)

            child_score = crypta_hps.cost_function(
                freq_native,
                crypta_hps.freq_analysis_of_text(
                    SubstitutionCipher(child_key.inverse_permutation().permutation).decrypt(ciphertext))
                # дешифруем шифртекст с помощью данной перестновки, берем частотный анализ и смотрим на значение
                # cost_function
            )
            if child_score > best_child_score:
                best_child_score = child_score
                best_child_key = child_key
        if best_child_key is None:
            flag = False
            break
        else:
            parent_key = best_child_key
            parent_score = best_child_score
    return parent_key


if __name__ == '__main__':
    text = '''For a long time Raskolnikov did not know of his mother’s death, though
    a regular correspondence had been maintained from the time he reached
    Siberia. It was carried on by means of Sonia, who wrote every month
    to the Razumihins and received an answer with unfailing regularity. At
    first they found Sonia’s letters dry and unsatisfactory, but later on
    they came to the conclusion that the letters could not be better, for
    from these letters they received a complete picture of their unfortunate
    brother’s life. Sonia’s letters were full of the most matter-of-fact
    detail, the simplest and clearest description of all Raskolnikov’s
    surroundings as a convict. There was no word of her own hopes, no
    conjecture as to the future, no description of her feelings. Instead of
    any attempt to interpret his state of mind and inner life, she gave the
    simple facts--that is, his own words, an exact account of his health,
    what he asked for at their interviews, what commission he gave her
    and so on. All these facts she gave with extraordinary minuteness. The
    picture of their unhappy brother stood out at last with great clearness
    and precision. There could be no mistake, because nothing was given but
    facts.'''
    native_freq = json.loads(open('freq_analysis_Crime_And_Punishment.json').read())
    sc = SubstitutionCipher()
    print(f'INITIAL TEXT: {text[0:70]}...')
    print(f"ENCRYPTION KEY: {sc.key}")
    print(f"DECRYPTION KEY: {sc.decryption_key}")
    encrypted_text = sc.encrypt(text)
    print(f'ENCRYPTED TEXT: {encrypted_text[0:70]}...')
    print(break_substitution(native_freq, encrypted_text))