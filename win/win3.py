from keras.preprocessing.sequence import pad_sequences
from keras.layers.core import Dense
from keras.layers import LSTM
from keras.models import Model
from keras.layers.embeddings import Embedding
from sklearn.model_selection import train_test_split
from keras.layers import Input
import numpy
from keras.models import load_model
import pandas as pd
import os
from numpy import zeros

def find(s, el):
    for i in s.index:
        if s[i] == el:
            return i
    return None

xlsx = pd.read_excel('ex.xlsx')

df = pd.DataFrame(columns=("f1", "f2", "f3", "f4", "f5", "f6",  "l1",  "l2",  "l3",  "l4",  "l5",  "l6"))

beforerow = []
predictrows = []
for i, row in xlsx.iterrows():
    if len(beforerow) > 0:
        tempa = []
        for j in range(1, 7):
            tempa.append(int(row[j])%2)
        for j in range(1, 7):
            tempa.append(int(beforerow[j])%2)

        df = df.append(pd.Series(tempa, index=df.columns), ignore_index=True)
    else:
        predictrows = ''
    beforerow = row


train_dataset_url = 'data_df.csv'

df.to_csv(train_dataset_url, sep=',', index= False)


# sample
toxic_comments = pd.read_csv(train_dataset_url)

print(toxic_comments.shape)

toxic_comments.head()

toxic_comments_labels = toxic_comments[["l1", "l2", "l3", "l4", "l5", "l6"]]
toxic_features_labels = toxic_comments[["f1", "f2", "f3", "f4", "f5", "f6"]]
print(toxic_comments_labels.head())

# fig_size = plt.rcParams["figure.figsize"]
# fig_size[0] = 10
# fig_size[1] = 8
# plt.rcParams["figure.figsize"] = fig_size

#toxic_comments_labels.sum(axis=0).plot.bar()

X = toxic_features_labels.values

y = toxic_comments_labels.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)


maxlen = 12

X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

embeddings_dictionary = dict()

vocab_size = 2

embedding_matrix = zeros((2, 100))

deep_inputs = Input(shape=(maxlen,))
embedding_layer = Embedding(vocab_size, 100, weights=[embedding_matrix], trainable=False)(deep_inputs)
LSTM_Layer_1 = LSTM(128)(embedding_layer)
dense_layer_1 = Dense(6, activation='sigmoid')(LSTM_Layer_1)

modelfilename = 'kerasmodel.h5'

if not os.path.exists(modelfilename):

    model = Model(inputs=deep_inputs, outputs=dense_layer_1)

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

    print(model.summary())

    history = model.fit(X_train, y_train, batch_size=64, epochs=3, verbose=1, validation_split=0.2)

    score = model.evaluate(X_test, y_test, verbose=1)

    model.save(modelfilename)

    print("Test Score:", score[0])
    print("Test Accuracy:", score[1])
else:
    model = load_model(modelfilename)

    d = numpy.array([[1,0,1,0,1,0,1,0,1,0,1,0]], numpy.int32)
    predictions = model.predict(d)
    print(predictions)
