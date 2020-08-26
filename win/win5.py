from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pandas
import tensorflow as tf
import numpy

def find(s, el):
    for i in s.index:
        if s[i] == el:
            return i
    return None

xlsx = pandas.read_excel('ex.xlsx')

df = pandas.DataFrame(columns=("f1", "f2", "f3", "f4", "f5", "label"))

beforerow = []
predictrows = []
for i, row in xlsx.iterrows():
    if len(beforerow) > 0:
        tempa = []
        for j in range(2, 7):
            #feture
            tempa.append(row[j]-row[j-1])
        #label
        tempa.append(45 - row[6] + beforerow[1])
        df = df.append(pandas.Series(tempa, index=df.columns), ignore_index=True)

        for j in range(2, 7):
            #tempa 첫번째 원소 제거
            del tempa[0]
            #label
            tempa.append(beforerow[j]-beforerow[j-1])
            df = df.append(pandas.Series(tempa, index=df.columns), ignore_index=True)
    else:
        tempa = []
        for j in range(2, 7):
            tempa.append(row[j]-row[j-1])
        predictrows.append(tempa)
        lastnum = row[6]
    beforerow = row


modelfilename = 'my_model.h5'

train_dataset_url = 'data_df_2.csv'

df.to_csv(train_dataset_url, sep=',', index= False)

column_names = ["f1", "f2", "f3", "f4", "f5", "label"]

feature_names = column_names[:-1]
label_name = column_names[-1]

print("특성: {}".format(feature_names))
print("레이블: {}".format(label_name))

class_names = list(range(0, 35))
batch_size = 32

if not os.path.exists(modelfilename):
    train_dataset = tf.data.experimental.make_csv_dataset(
        train_dataset_url,
        batch_size,
        column_names=column_names,
        label_name=label_name,
        num_epochs=1)

    features, labels = next(iter(train_dataset))

    print(features)

    def pack_features_vector(features, labels):
      """특성들을 단일 배열로 묶습니다."""
      features = tf.stack(list(features.values()), axis=1)
      return features, labels

    train_dataset = train_dataset.map(pack_features_vector)

    features, labels = next(iter(train_dataset))

    model = tf.keras.Sequential([
      tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(5,)),  # 입력의 형태가 필요합니다.
      tf.keras.layers.Dense(10, activation=tf.nn.relu),
      tf.keras.layers.Dense(35)
    ])

    predictions = model(features)
    predictions[:14]

    tf.nn.softmax(predictions[:5])

    print("  예측: {}".format(tf.argmax(predictions, axis=1)))
    print("레이블: {}".format(labels))

    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    def loss(model, x, y):
      y_ = model(x)

      return loss_object(y_true=y, y_pred=y_)


    l = loss(model, features, labels)
    print("손실 테스트: {}".format(l))

    def grad(model, inputs, targets):
      with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
      return loss_value, tape.gradient(loss_value, model.trainable_variables)

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

    loss_value, grads = grad(model, features, labels)

    print("단계: {}, 초기 손실: {}".format(optimizer.iterations.numpy(),
                                              loss_value.numpy()))

    optimizer.apply_gradients(zip(grads, model.trainable_variables))

    print("단계: {},      손실: {}".format(optimizer.iterations.numpy(),
                                              loss(model, features, labels).numpy()))

    ## 노트: 이 셀을 다시 실행하면 동일한 모델의 변수가 사용됩니다.

    # 도식화를 위해 결과를 저장합니다.
    train_loss_results = []
    train_accuracy_results = []

    num_epochs = 301

    for epoch in range(num_epochs):
      epoch_loss_avg = tf.keras.metrics.Mean()
      epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

      # 훈련 루프 - 32개의 배치를 사용합니다.
      for x, y in train_dataset:
        # 모델을 최적화합니다.
        loss_value, grads = grad(model, x, y)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        # 진행 상황을 추적합니다.
        epoch_loss_avg(loss_value)  # 현재 배치 손실을 추가합니다.
        # 예측된 레이블과 실제 레이블 비교합니다.
        epoch_accuracy(y, model(x))

      # epoch 종료
      train_loss_results.append(epoch_loss_avg.result())
      train_accuracy_results.append(epoch_accuracy.result())

      if epoch % 50 == 0:
        print("에포크 {:03d}: 손실: {:.3f}, 정확도: {:.3%}".format(epoch,
                                                                    epoch_loss_avg.result(),
                                                                    epoch_accuracy.result()))

    model.save(modelfilename)
else:
    model = tf.keras.models.load_model(modelfilename)

predict_dataset = tf.convert_to_tensor(predictrows)

predictions = model(predict_dataset)

finalresults = []
for i, logits in enumerate(predictions):
    array = logits.numpy()
    temp = (-array).argsort()
    temp = temp[:5]
    finalresults.extend(temp)

for i in range(len(temp)):
    if i % 6 == 0:
        print('')
    print(temp[i] + 1, end=',')

#예상 넘버 리스트 가져오는 함수


#기존에 나온수인지 체크하는 함수


