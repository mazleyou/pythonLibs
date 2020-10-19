import os
import pandas
import tensorflow as tf
import numpy
import copy
def find(s, el):
    for i in s.index:
        if s[i] == el:
            return i
    return None

xls = pandas.read_excel('ex2.xls')
xls_list = xls.values.tolist()

for roundIdx in range(len(xls_list)):
    for nextIdx in range(1, 8):
        if xls_list[roundIdx][0] == xls_list[roundIdx+nextIdx][0]:
            print(roundIdx)
    for numberIdx in range(len(xls_list[roundIdx])):
        print(xls_list[roundIdx][numberIdx])


df = pandas.DataFrame(columns=("f1", "f2", "f3", "f4", "f5", "f6", "f7", "label"))



beforerow = []
predictrows = []
for i, row in xls.iterrows():
    if len(beforerow) > 0:
        tempa = []
        for j in range(1, 8):
            #feture
            tempa.append(row[j])
        #label is last time not exist number
        for j in range(0, 46):
            if numpy.where(beforerow.values == j)[0].size > 0:
                df = df.append(pandas.Series(tempa + [j - 1], index=df.columns), ignore_index=True)
    else:
        tempa = []
        for j in range(1, 8):
            tempa.append(row[j])
        predictrows.append(tempa)
    beforerow = row


modelfilename = 'my_model.h5'

train_dataset_url = 'data_df_2.csv'

df.to_csv(train_dataset_url, sep=',', index= False)

column_names = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "label"]

feature_names = column_names[:-1]
label_name = column_names[-1]

print("특성: {}".format(feature_names))
print("레이블: {}".format(label_name))

class_names = list(range(0, 45))
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
      tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(7,)),  # 입력의 형태가 필요합니다.
      tf.keras.layers.Dense(10, activation=tf.nn.relu),
      tf.keras.layers.Dense(45)
    ])

    predictions = model(features)
    predictions[:7]

    tf.nn.softmax(predictions[:7])

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

    num_epochs = 401

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


def make_predict_list(inputdatas):
    return_results = []
    predict_dataset = tf.convert_to_tensor(inputdatas)
    predictions = model(predict_dataset)

    for i, logits in enumerate(predictions):
        array = logits.numpy()
        temp = (-array).argsort()
        temp = temp[:45]+1
        return_results.extend(temp)

    return return_results

finalresults = make_predict_list(predictrows)



key_index = {}

for pred_value in predictrows[0]:
    key_index[pred_value] = 1
lastnumbers = [[0 for col in range(6)] for row in range(6)]

finalresultsindex = 0
for index2, value2 in enumerate(finalresults):
    if not value2 in key_index.keys() and finalresultsindex < 6:
        key_index[value2] = 1
        lastnumbers[finalresultsindex][0] = value2
        finalresultsindex = finalresultsindex + 1

del predictrows[0][0]
sample = copy.deepcopy(predictrows)


for j in range(0, 6):
    sample[0].extend(lastnumbers[j][:1])
    numbers2 = make_predict_list(sample)
    for index2, value2 in enumerate(numbers2):
        if not value2 in key_index.keys():
            key_index[value2] = 1
            lastnumbers[j][1] = value2
            break
    del sample[0][5]

del predictrows[0][0]
sample2 = copy.deepcopy(predictrows)
for j in range(0, 6):
    sample2[0].extend(lastnumbers[j][:2])
    numbers2 = make_predict_list(sample2)
    for index2, value2 in enumerate(numbers2):
        if not value2 in key_index.keys():
            key_index[value2] = 1
            lastnumbers[j][2] = value2
            break
    del sample2[0][4:6]

del predictrows[0][0]
sample3 = copy.deepcopy(predictrows)
for j in range(0, 6):
    sample3[0].extend(lastnumbers[j][:3])
    numbers2 = make_predict_list(sample3)
    for index2, value2 in enumerate(numbers2):
        if not value2 in key_index.keys():
            key_index[value2] = 1
            lastnumbers[j][3] = value2
            break
    del sample3[0][3:6]

del predictrows[0][0]
sample4 = copy.deepcopy(predictrows)
for j in range(0, 6):
    sample4[0].extend(lastnumbers[j][:4])
    numbers2 = make_predict_list(sample4)
    for index2, value2 in enumerate(numbers2):
        if not value2 in key_index.keys():
            key_index[value2] = 1
            lastnumbers[j][4] = value2
            break
    del sample4[0][2:6]

del predictrows[0][0]
sample5 = copy.deepcopy(predictrows)
for j in range(0, 6):
    sample5[0].extend(lastnumbers[j][:5])
    numbers2 = make_predict_list(sample5)
    for index2, value2 in enumerate(numbers2):
        if not value2 in key_index.keys():
            key_index[value2] = 1
            lastnumbers[j][5] = value2
            break
    del sample5[0][1:6]

print(lastnumbers)