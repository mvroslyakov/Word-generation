from histograms import Dictogram
import argparse
import sys
import random
import os
import pickle
import math


def new_parser():  # Создаем консольную оболочку
    pars = argparse.ArgumentParser(
        description='''Эта программа принимает на вход словарь,
        составленный с помощью программы train.py, и на его основе
        генерирует свой текст. Надо ввести путь к файлу
        со словарем и длину выводимой последовательности.''',
        epilog='''(с) 2018. Created by Roslyakov Misha'''
    )
    pars.add_argument('--seed', nargs='?', default='END',
                      help='Задает начальное слово. Если не указано, '
                           'выбираем слово случайно из всех слов '
                           '(не учитывая частоты).')
    pars.add_argument('--length', type=int, required=True,
                      help='Длина генерируемой последовательности.')
    pars.add_argument('--model', required=True,
                      help='Путь к файлу, из которого загружается модель.'
                           'Вид файла *****.text'
                           'и находиться в папке с файлами программы.')
    pars.add_argument('--output', nargs='?',
                      help='Файл, в который будет записан результат. '
                           'Если аргумент отсутствует, выводить в stdout.')
    return pars


def generate_random_start(model):  # создаем рандомное начало
    if 'END' in model:
        seed = 'END'
        while seed == 'END':
            seed = model['END'].return_weighted_random_word()
        return seed
    return random.choice(list(model.keys()))


def generate_random_sentence(length, markov_model):  # создаем предложение заданной длины
    if seed_w != 'END':
        if seed_w not in markov_model:
            print("Слово не найдено, сгенерируется рандомное слово")
            current_word = generate_random_start(markov_model)
        else:
            current_word = seed_w
    else:
        current_word = generate_random_start(markov_model)
    print(current_word)
    sentence = [current_word]
    i = 0
    while i != length:
        while current_word == 'ENDS':
            current_word = generate_random_start(markov_model)
        current_dictograms = markov_model[current_word]
        random_weighted_word = current_dictograms.return_weighted_random_word()
        current_word = random_weighted_word
        print(sentence)
        if current_word == 'ENDS':
            i -= 1
        else:
            sentence.append(current_word)
        i += 1
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '.'
    return sentence


parser = new_parser()
commands = parser.parse_args(sys.argv[1:])
model_file = commands.model
seed_w = commands.seed
with open(model_file, 'rb') as file:
    models = pickle.load(file)
len_s = commands.length
print(models.keys())
phrase = generate_random_sentence(int(len_s), models)
if not commands.output:
    print('Our text:')
    print(phrase)
else:
    out_file = open(commands.output, 'w')
    out_file.write(phrase)
