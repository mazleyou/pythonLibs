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


def getMatch(label, targets):
    ret_index = 0
    for target in targets:
        feature_tokens = word_tokenize(target)
        for feature_word in feature_tokens:
            if SequenceMatcher(None, feature_word, label_word).ratio() > 0.6:
                return ret_index
            else:
                ret_index += 1
                break
    return -1






df = pd.read_csv('train_data.csv')
check_df = pd.DataFrame(columns=("f_sentence", "l_sentence", "label"))
p = re.compile('하고$|에도$|하여$|다면$')

for i, row in df.iterrows():
    if 100 > i >= 0:
        # Feature 문장 분리
        feature_sentences = split_sentences(row['text'])
        # Label 문장 분리
        label_sentences = split_sentences(row['summary'])
        # Feature sentences에서 중요 문장과 비중요 문장 구분
        feature_index = 0
        for label in label_sentences:
            label_tokens = word_tokenize(label)
            for label_word in label_tokens:
                # feature_tokens = word_tokenize(feature_sentences[feature_index])
                # for feature_word in feature_tokens:
                new_index = getMatch(label_word, feature_sentences[feature_index:])
                if new_index > -1:
                    feature_index += new_index
                    
                if SequenceMatcher(None, feature_sentences[feature_index], label_word).ratio() > 0.6:
                    # feature word 와 label word 가 일치할 경우
                    # 일치한 단어를 feature sentence에서 삭제해야하는 것이 효율적인지 고려
                    break
                else:
                    feature_index += 1

                temp_list = []
                check_df = check_df.append(pd.Series(temp_list, index=df.columns), ignore_index=True)

    check_df.to_csv('check.csv', sep=',', index=False)
    print(token)