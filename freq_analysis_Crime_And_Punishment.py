from collections import defaultdict
import json


dictionary_of_all_letters = defaultdict(int)
cnt_all_letters = 0

with open('Dostoevsky-Crime and Punishment.txt', 'r', encoding='utf8') as f:
    text = f.read()
    for letter in text:
        if letter.isalpha() and ord('a') <= ord(letter.lower()) <= ord('z'):
            dictionary_of_all_letters[letter.lower()] += 1
            cnt_all_letters += 1

print(dictionary_of_all_letters)
for key in dictionary_of_all_letters:
    dictionary_of_all_letters[key] /= cnt_all_letters

print(dictionary_of_all_letters)
print(cnt_all_letters)
# json_data = json.dump(dictionary_of_all_letters, indent=4)
# print(json_data)
with open('freq_analysis_Crime_And_Punishment.json', 'w') as out_file:
    json.dump(dictionary_of_all_letters, out_file, indent=4)
