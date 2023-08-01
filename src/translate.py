from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import os
from collections import defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred_path = os.path.join(PROJECT_ROOT, 'creds/lernprogramm-5ca8bb7ec8ad.json')
credentials = service_account.Credentials.from_service_account_file(
        cred_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
client = translate.Client(credentials=credentials)


def word(source_lang, target_lang, word):
    result = client.translate(word, source_language=source_lang, target_language=target_lang)
    word_tuple = (result['input'], result['translatedText'])
    return word_tuple


def sentences(source_lang, target_lang, sentences):
    '''{'translatedText': 'прыгнул', 'input': 'Gesprungen'}'''
    result = client.translate(sentences, source_language=source_lang, target_language=target_lang)

    sentence_tuple_list = defaultdict(str)
    for sentence in result:
        sentence_tuple_list[sentence['input']] = sentence['translatedText']
    return sentence_tuple_list


def text(source_lang, target_lang, text):
    result = client.translate(text, source_language=source_lang, target_language=target_lang)
    text_tuple = (result['input'], result['translatedText'])
    return text_tuple

