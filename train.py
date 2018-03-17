from histograms import Dictogram
import re
import argparse
import pickle
import os
import sys

r_alphabet = re.compile(u'[а-яa-zA-ZА-Я0-9-]+|[.,:;?!]+')


def new_parser():  # Создание консольной оболочки
    pars = argparse.ArgumentParser(
        description='''Данная программа составляет последовательности из слов
         и сохраняет их в заданном файле.''',
        epilog='''(с) 2018. Created by Roslyakov Misha'''
    )
    pars.add_argument('--input', '--input-dir', nargs='?',
                      help='Путь к директории, в которой лежит коллекция '
                           'документов. Если данный аргумент не '
                           'задан, считается, что тексты вводятся из stdin. '
                           'ВНИМАНИЕ: в конце ввода текстов из stdin '
                           'для завершения ввода '
                           'необходимо написать строку:"*END*" или пустую строку.')
    pars.add_argument('--model', required=True,
                      help='Путь к файлу, в который сохраняется модель.'
                           'Формат файла *****.txt'
                           'хранить в папке с train.py и generate.py.')
    return pars


def gen_tokens(line_w):  # делим на слова
    for token in r_alphabet.findall(line_w):
        yield token


def make_markov_model(data):
    markov_model = dict()

    for i in range(0, len(data)-1):
        if data[i] in markov_model:
            # Просто присоединяем к уже существующему распределению
            markov_model[data[i]].update([data[i+1]])
        else:
            markov_model[data[i]] = Dictogram([data[i+1]])
    return markov_model


models = dict()
parser = new_parser()
commands = parser.parse_args(sys.argv[1:])
way_to_file = commands.input
if way_to_file is not None:  # ищем путь к текстам
    d_list = os.listdir(way_to_file)
    txt_files = list(filter(lambda x: x.endswith('.txt'), d_list))
    for bad_file in txt_files:
        path = os.path.join(way_to_file, bad_file)
        with open(path, 'r', encoding='UTF-8') as file:
            for line in file:
                tokens = list(gen_tokens(line))
                print(len(tokens))
                models = make_markov_model(tokens)
            file.close()
else:
    ls = ' '
    while ls != '*END*':
        try:
            ls = input().lower()
        except EOFError:
            break
        tokens = gen_tokens(ls)
        models = make_markov_model(tokens)
with open(commands.model, 'wb') as f:
    pickle.dump(models, f)