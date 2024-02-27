import os
import json

from HillCipher import HillCipher, HillRecCipher
import cryptanalysis_helpers as cah


def get_n_gram_json_file(text, filename, used_syms, n):
    """ Create JSON file with n-gram frequencies of a given text. """
    cah.to_json(filename, cah.freq_analysis_n_gram(text, used_syms, n))


def get_crime_and_punisment_3_gram_json():
    with open('Dostoevsky-Crime and Punishment.txt', 'r', encoding='utf8') as f:
        get_n_gram_json_file(f.read(), '3-gram-freq_analysis_Crime_and_Punishment.json', HillCipher.d, 3)



if __name__ == '__main__':
    with open('3-gram-freq_analysis_Crime_and_Punishment.json', 'r') as f:
        print(json.load(f))