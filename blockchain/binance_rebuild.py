import requests
import pymysql
from apscheduler.schedulers.background import BackgroundScheduler
import time
import pandas
import os
import tensorflow as tf
import numpy
from matplotlib import pyplot as plt

def value_rebalansing(now, open):
    ret = 0
    ret = (now / open * 1000) - 970
    if ret < 0:
        ret = 0
    return int(ret)

def label_check(val1, val2):
    ret = 1
    if val1 / val2 > 1.01:
        ret = 2
    elif val1 / val2 < 0.99:
        ret = 0
    return ret

def klines():
    try:
        print("main start")
        conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
        curs = conn.cursor()

        lasttime = 160000000

        column_names = []
        for f_index in range(1, 51):
            column_names.append("f" + str(f_index))
        column_names.append("label")

        df = pandas.DataFrame(columns=(column_names))

        curs.execute("""select * from BTCUSDT_KLINES where OPEN_TIME >= %s order by OPEN_TIME""", lasttime)
        exist_record = curs.fetchall()
        len_record = len(exist_record)
        flag = 0
        tempa = []
        predictrows = []
        add_flag = 0
        for index in range(len_record):
            if index + 20 <= len_record:
                # print("no : " + str(exist_record[index][0]))
                opentime = exist_record[index][0]
                openvalue = exist_record[index][1]

                for i in range(0, 10):
                    tempa.append(value_rebalansing(exist_record[index + i][2], openvalue))
                    tempa.append(value_rebalansing(exist_record[index + i][3], openvalue))
                    tempa.append(value_rebalansing(exist_record[index + i][4], openvalue))
                    tempa.append(int(exist_record[index+i][5]))
                    tempa.append(int(exist_record[index+i][6]/100000))
                if index == 0:
                    predictrows.append(tempa[:50])
                label_value = label_check(exist_record[index + 19][1], exist_record[index + 10][1])

                if label_value == 2 or label_value == 0:
                    add_flag = 2
                else:
                    add_flag = add_flag - 1

                tempa.append(label_value)
                if add_flag >= 0:
                    df = df.append(pandas.Series(tempa, index=df.columns), ignore_index=True)

                tempa = []

        train_dataset_url = 'binance.csv'
        df.to_csv(train_dataset_url, sep=',', index=False)

        feature_names = column_names[:-1]
        label_name = column_names[-1]

        batch_size = 32
        modelfilename = 'binance_model.h5'

        if not os.path.exists(modelfilename):
            train_dataset = tf.data.experimental.make_csv_dataset(
                train_dataset_url,
                batch_size,
                column_names=column_names,
                label_name=label_name,
                num_epochs=1)

            features, labels = next(iter(train_dataset))

            def pack_features_vector(features, labels):
                """특성들을 단일 배열로 묶습니다."""
                features = tf.stack(list(features.values()), axis=1)
                return features, labels

            train_dataset = train_dataset.map(pack_features_vector)

            features, labels = next(iter(train_dataset))

            model = tf.keras.Sequential([
                tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(50,)),  # 입력의 형태가 필요합니다.
                tf.keras.layers.Dense(10, activation=tf.nn.relu),
                tf.keras.layers.Dense(3)
            ])

            predictions = model(features)
            predictions[:50]

            tf.nn.softmax(predictions[:50])

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
            return_results = 0
            predict_dataset = tf.convert_to_tensor(inputdatas)
            predictions = model.predict(predict_dataset)

            for i, logits in enumerate(predictions):
                return_results = numpy.argmax(logits)
            return return_results

        finalresults = make_predict_list(predictrows)
        print(finalresults)
    except Exception as e:
        print(e)

klines()