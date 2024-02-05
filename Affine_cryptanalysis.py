import json

import helpers as hps
from AffineCipher import AffineCipher
import cryptanalysis_helpers as crypta_hps


def break_affine(ciphertext, freq_native):
    """
    Алгоритм:
        1. Перебером всевозможный ключи.
        2. Проведем частотный анализ текстов, полученных при дешифровке с помощью каждой пары ключей
        3. Посчитаем целевую функцию (f=sum(native[i]*text[i]) для каждой пары ключей. (описана в модулее
                cryptanalysis_helpers.py в ф. cost_function)
        4. Пара ключей, с наибольшим значением cost_function, с наибольшей вероятностью будет являться ответом.
    """

    max_val = 0
    best_keys = (None, None)

    # 1. Переберем всевозможные ключи a и b

    b_keys = tuple(key for key in range(hps.ALPHABET_LEN))

    a_keys = tuple(key for key in range(hps.ALPHABET_LEN) if hps.gcd(key, hps.ALPHABET_LEN) == 1)

    # 2. Для каждого ключа расшифруем текст и проведем частотный анализ
    for key_a in a_keys:
        for key_b in b_keys:
            ac = AffineCipher(key_a=key_a, key_b=key_b)
            decrypted_text = ac.decrypt(ciphertext)

            freq_decrypted = crypta_hps.freq_analysis_of_text(decrypted_text)

            # 3. целевая функция

            cost_val_cur = crypta_hps.cost_function(freq_native, freq_decrypted)
            # print(cost_val_cur, key_a, k)
            if cost_val_cur > max_val:
                max_val = cost_val_cur
                best_keys = (key_a, key_b)

    return best_keys


if __name__ == '__main__':

    native_freq = json.loads(open('freq_analysis_Crime_And_Punishment.json').read())

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
    print(f'INITIAL TEXT: {text[0:50]}...')
    affine_cipher = AffineCipher()
    encrypted_text = affine_cipher.encrypt(text)
    print(f'ENCRYPTED TEXT: {encrypted_text[0:50]}...')
    print(f'REAL KEY_A {affine_cipher.key_a}')
    print(f'REAL KEY_B {affine_cipher.key_b}')
    print(f'REAL DECRYPTION_KEY {affine_cipher.decryption_key_a}')
    poss_keys = break_affine(encrypted_text, native_freq)
    print('RESULT OF BREAKING THE CIPHER')
    print(f'POSSIBLE KEY A {poss_keys[0]}')
    print(f'POSSIBLE KEY B {poss_keys[1]}')
    # decryption_key = [0]
    # hps.gcd_extended(poss_keys[0], hps.ALPHABET_LEN, decryption_key, [0])
    affine_breaker = AffineCipher(poss_keys[0], poss_keys[1])

    print(f'THEREFORE, DECRYPTION KEY A IS {affine_breaker.decryption_key_a} ')
    print(f'DECRYPTED_TEXT: {affine_breaker.decrypt(encrypted_text)[0:50]}...')

