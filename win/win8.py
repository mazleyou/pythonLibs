import os
import pandas
import tensorflow as tf
import numpy
import copy

#전회 3회분을 조합해서 예측 하는 모델 생성
EXCELCOMLOMES = 7
FETURECOUNT = 3

def find(s, el):
    for i in s.index:
        if s[i] == el:
            return i
    return None


def df_to_list(pram_df):
    ret_list = []
    for row in pram_df.iterrows():
        for j in range(1, EXCELCOMLOMES):
            ret_list.append(row[1][j])
    return ret_list


modelfilename = 'my_model.h5'

train_dataset_url = 'data_df_2.csv'

xlsx = pandas.read_excel('ex2.xls')

if not os.path.exists(train_dataset_url):
    df = pandas.DataFrame(columns=("f1", "f2", "f3", "label"))

    #전회 3회분의 기록을 조합해서 입력데이터로 사용하기 때문에 인덱스 4부터 시작
    for xlsx_index in range(0, 100):
        record_1 = df_to_list(xlsx[xlsx_index+3:xlsx_index+4])
        record_2 = df_to_list(xlsx[xlsx_index+2:xlsx_index+3])
        record_3 = df_to_list(xlsx[xlsx_index+1:xlsx_index+2])
        label = df_to_list(xlsx[xlsx_index:xlsx_index+1])
        for row_1 in range(0, 6):
            for row_2 in range(0, 6):
                for row_3 in range(0, 6):
                    for row_label in range(0, 6):
                        tempa = [record_1[row_1], record_2[row_2], record_3[row_3], label[row_label] - 1]
                        df = df.append(pandas.Series(tempa, index=df.columns), ignore_index=True)
    df.to_csv(train_dataset_url, sep=',', index= False)


column_names = ["f1", "f2", "f3", "label"]

feature_names = column_names[:-1]
label_name = column_names[-1]

print("특성: {}".format(feature_names))
print("레이블: {}".format(label_name))

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
      tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(FETURECOUNT,)),  # 입력의 형태가 필요합니다.
      tf.keras.layers.Dense(10, activation=tf.nn.relu),
      tf.keras.layers.Dense(45)
    ])

    predictions = model(features)
    predictions[:FETURECOUNT]

    tf.nn.softmax(predictions[:FETURECOUNT])

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


predict_1 = df_to_list(xlsx[2:3])
predict_2 = df_to_list(xlsx[1:2])
predict_3 = df_to_list(xlsx[0:1])

final_dict = {}


def f2(x):
    return x[1]

for row_1 in range(0, 6):
    for row_2 in range(0, 6):
        for row_3 in range(0, 6):
            finalresults = make_predict_list([[predict_1[row_1], predict_2[row_2], predict_3[row_3]]])
            score = 100
            for result in finalresults:
                if result in final_dict:
                    final_dict[result] = final_dict[result] + score
                else:
                    final_dict[result] = score
                score = score - 1


res = sorted(final_dict.items(), key=(lambda x: x[1]), reverse = True)

line_end = 0
for key in res:
    line_end = line_end + 1
    if line_end == 6:
        line_end = 0
        print(key[0])
    else:
        print(key[0], end='\t')






