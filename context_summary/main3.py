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
        # label_sentences = split_sentences(row['summary'])
        # Feature sentences에서 중요 문장과 비중요 문장 구분
        label_index = 0
        label_tokens = word_tokenize(row['summary'])
        for feature in feature_sentences:

            new_index = get_match(label_tokens[label_index:], feature)
            labels_str = ''
            label_flag = 0
            if new_index > 0:
                labels_str = ' '.join(label_tokens[label_index:label_index + new_index])
                label_flag = 1
                label_index += new_index

            check_df = check_df.append(pd.Series([feature, labels_str, label_flag], index=df.columns), ignore_index=True)

        check_df.to_csv('check.csv', sep=',', index=False)
