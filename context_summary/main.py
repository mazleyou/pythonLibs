import pandas as pd
import nltk

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
from difflib import SequenceMatcher

# 한번만 다운로드 그 후엔 주석 처리
# nltk.download('treebank')
# nltk.download('punkt')


def split_sentences(input):
    word_tokens = word_tokenize(input)
    ret_sentences = []
    ret_sentences.append("");
    for token in word_tokens:
        ret_sentences[-1] += token + ' '
        m = p.search(token)
        if m is not None:
            ret_sentences.append("")
    return ret_sentences


def get_match(labels, target):
    ret_index = 0
    feature_tokens = word_tokenize(target)
    for feature_word in feature_tokens:
        last_check = False
        if SequenceMatcher(None, feature_word, labels[ret_index]).ratio() >= 0.5:
            ret_index += 1
            last_check = True

    return last_check, ret_index


df = pd.read_csv('train_data.csv')
check_df = pd.DataFrame(columns=("id", "summary", "text"))
p = re.compile('하고$|에도$|하여$|다면$')

for i, row in df.iterrows():
    if 100 > i >= 0:
        # Feature 문장 분리
        feature_sentences = split_sentences(row['text'])
        # # Label 문장 분리
        label_sentences = split_sentences(row['summary'])

        # Feature sentences에서 중요 문장과 비중요 문장 구분
        results = []
        result = {}

        label_index = 0
        label_tokens = word_tokenize(row['summary'])

        for idx_l, labels in enumerate(label_sentences):
            max_ratio = 0
            for idx_f, features in  enumerate(feature_sentences):
                now_ratio = SequenceMatcher(None, labels, features).ratio()
                if now_ratio > max_ratio:
                    if max_ratio > 0.5:
                        result[idx_l] = [labels, feature_sentences[idx_f-1] + features, max_ratio]
                    else:
                        result[idx_l] = [labels, features, max_ratio]
                    max_ratio = now_ratio
                else:
                    if now_ratio > 0.5:
                        result[idx_l] = [labels, result[idx_l][1] + features, max_ratio]


        print("s")
