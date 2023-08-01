import csv
from time import sleep
from collections import defaultdict
# from .config import load_default
import os
from . import translate

# config = load_default()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(PROJECT_ROOT, 'book')
DICT_DIR = os.path.join(PROJECT_ROOT, 'dictionary')

punctuation_marks = ['.', ',', '"', '»', '«', '!', '?',
                     '...', ':', ';', '.,', '-', '(', ')',
                     "'", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
                  'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII',
                  'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX', 'XXXI',
                  'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX']


def open_text():
    '''
    Открываем текст из файла,
    складываем текст в переменную raw_text,
    возвращаем переменную raw_text.
    '''
    with open(os.path.join(BOOK_DIR, 'book.txt'), 'r') as file:
        raw_text = file.read()
    return raw_text


def pars_text2statement(raw_text):
    '''
    Читаем raw_text и делим его на предложения, конец предложения это точка.
    Записываем в словарь, где ключ номер предложения, вэлью само предложение.
    '''
    statement = str()
    parsed_statements = defaultdict(str)
    count = 1
    flag_end_marks = False
    flag_quote = False
    for char in raw_text:
        if char == ',':
            flag_end_marks = False
        if char == '«':
            flag_quote = True
        if char == '»':
            flag_quote = False
            flag_end_marks = True
        if flag_end_marks:
            if char == ' ':
                if statement[0].islower():
                    previous_statement = parsed_statements[count-1]
                    parsed_statements[count-1] = previous_statement + ' ' + statement
                    statement = str()
                    flag_end_marks = False
                    continue
                else:
                    parsed_statements[count] = statement
                    statement = str()
                    count += 1
                    flag_end_marks = False
                    continue
        statement = statement + char
        if char == '.' or char == '!' or char == '?':
            if flag_quote:
                continue
            if not flag_quote:
                flag_end_marks = True
    '''for key, value in parsed_statements.items():
        print(key, ' : ', value)'''
    return parsed_statements


def pars_text2words(raw_text):
    '''
    Читаем raw_text и делим его на слова, выкидывая знаки препинания.
    '''
    text_wo_pm = ''
    for char in raw_text:
        if char not in punctuation_marks:
            text_wo_pm = text_wo_pm + char
    list_of_words = text_wo_pm.split()
    return list_of_words


def prepare_dict(list_of_words):
    '''
    Записываем в словарь где ключ слово, а велью количество упоминаний в тексте.
    '''
    dictionary = defaultdict(int)
    for word in list_of_words:
        if word not in roman_numerals:
            dictionary[word] = dictionary[word] + 1
    return dictionary


def translate_dictionary(dictionary):
    '''
    Создать файл словаря, который будет лежать на диске,
    Функция должна проверить сначала файл на премет перевода слов,
    Если какие-то слова не нашлись, только их запрашивать в гугл переводчике.
    Новые переводы добавлять в файл словаря.
    '''
    sentences_128 = []
    sentences_all = defaultdict(str)

    dict_of_sentences = []
    count = 0
    file_dictionary = dictionary_from_file()
    for word in dictionary:
        if word not in file_dictionary.keys():
            dict_of_sentences.append(word)
    for word in dict_of_sentences:
        sentences_128.append(word)
        count += 1
        if count == 127:
            sentences_w_translate = translate.sentences('de', 'ru', sentences_128)
            for item in sentences_w_translate:
                sentences_all[item] = sentences_w_translate[item]
            count = 0
            sentences_128 = []
    dictionary_to_file(sentences_all)
    for word in dictionary:
        if word in file_dictionary.keys():
            sentences_all[word] = file_dictionary[word]
    return sentences_all


def dictionary_to_file(new_dict):
    for item in new_dict:
        with open(os.path.join(DICT_DIR, 'de_ru.csv'), 'w') as file:
            writer = csv.writer(file)
            row = f'{item}, {new_dict[item]}'
            writer.writerows(row)


def dictionary_from_file():
    file_dictionary = defaultdict(str)
    with open(os.path.join(DICT_DIR, 'de_ru.csv')) as file:
        reader = csv.reader(file)
        for row in reader:
            file_dictionary[row[0]] = row[1]
    return file_dictionary


def translate_text():
    pass


def words2phrases():
    '''Пока не понятно как искать,
    Но идея в том, чтобы склеивать слова в устоявшиеся выражения,
    И считать их за одно слово, если они являются идиомой.
    '''
    pass


def text_statistics(words, statements):
    '''
    Проверяем количество всего слов в тексте,
    Количество уникальных слов в тексте,
    Количество предложений в тексте,
    Количество знаков в тексте
    '''


def new_text_preparation():
    '''Готовим текст следующим образом:
    Делим книгу на логические еденицы, например 2 страницы А4(1 лист),
    Выводим словарь для этой единицы с переводом слов.
    Далее предложение в оригинале за ним через несколько пустых строк перевод предложения.
    В последующих словарях перед текстовыми еденицами слова не повторяются.
    '''
    pass


def main():
    '''raw_text = open_text()
    list_of_words = pars_text2words(raw_text)
    dictionary = prepare_dict(list_of_words)
    translate_dictionary(dictionary)
    pars_text2statement(raw_text)'''
    dictionary_from_file()


if __name__ == '__main__':
    main()
