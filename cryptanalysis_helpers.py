from collections import defaultdict
import json


def cost_function(freq_data_native, freq_data_cipher):
    """ Целевая функция f = sum(native(sym) * cipher(sym) """
    return sum(
        [freq_data_cipher[key] * freq_data_native[key] if key in freq_data_cipher
         else 0 for key in freq_data_native.keys()]
    )


def freq_analysis_of_text(text):
    """ Проводит частотный анализ букв англ алфавита по заданному тексту. """
    d = defaultdict(int)
    cnt_all_letters = 0
    for letter in text:
        if letter.isalpha() and ord('a') <= ord(letter.lower()) <= ord('z'):
            d[letter.lower()] += 1
            cnt_all_letters += 1
    for k in d.keys():
        d[k] /= cnt_all_letters
    return d


if __name__ == '__main__':
    file = open('freq_analysis_Crime_And_Punishment.json')
    data = json.loads(file.read())
    print(data)

    file = open('freq_analysis_Crime_And_Punishment.json')
    data = json.loads(file.read())
    print(data)
    print(cost_function(data, {'a': 1}))

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
    freq = freq_analysis_of_text(text)
    print(freq)

    print(cost_function(data, freq))

    encrypted_text = '''gbidubqrenfvidtjbuqnjbaknkqbejqblbgcntfbecvitkvdececbprcdi
    vrpudizbiivtmbqkvqzvcdkovvqfdnqednqvkgibfecvenfvcvivdzcvktnovindneldtzdiinvkbqohf
    vdqtbgtbqndlcblibevvavihfbqecebecvidspfncnqtdqkivzvnavkdqdqtlvilnecpqgdnunqrivrpudinehde
    gniteecvhgbpqktbqndtuveevitkihdqkpqtdentgdzebihopeudevibqecvhzdfvebecvzbqzuptnbqecdeecvuvee
    vitzbpukqbeovoveevigbigibfecvtvuveevitecvhivzvnavkdzbfmuvevmnzepivbgecvnipqgbiepqdevoibecvitung
    vtbqndtuveevitlvivgpuubgecvfbtefdeevibggdzekvednuecvtnfmuvtedqkzuvdivtekvtzinmenbqbgduuidtjbuqnjba
    ttpiibpqknqrtdtdzbqanzeecvivldtqblbikbgcviblqcbmvtqbzbqyvzepivdtebecvgpepivqbkvtzinmenbqbgcvigvvunqrtn
    qtevdkbgdqhdeevfmeebnqevimivecnttedevbgfnqkdqknqqviungvtcvrdavecvtnfmuvgdzetecdentcntblqlbiktdqvwdzedzz
    bpqebgcntcvdueclcdecvdtjvkgbideecvninqevianvltlcdezbffnttnbqcvrdavcvidqktbbqduuecvtvgdzettcvrdavlnecvwei
    dbiknqdihfnqpevqvttecvmnzepivbgecvnipqcdmmhoibecvitebbkbpedeudtelnecrivdezuvdiqvttdqkmivzntnbqecvivzbpuk
    ovqbfntedjvovzdptvqbecnqrldtrnavqopegdzet'''

    freq_encr = freq_analysis_of_text(encrypted_text)
    print(freq_encr)
    print(cost_function(data, freq_encr))