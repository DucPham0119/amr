import numpy as np
from keras import Input, Model
from keras.layers import LSTM, Dense, Bidirectional, TimeDistributed, Dropout
from keras.saving.save import load_model
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.layers import RepeatVector

from data import load_data, loadLabel, loadPhoBert, writeData


def padding(data, max_len=62):
    len_dt = len(data)
    len_col = len(data[0][0])
    for idx in range(len_dt):
        for j in range(max_len - len(data[idx])):
            data[idx].append([0] * len_col)

    data = np.array(data, dtype=np.float64)
    return data


def modelLSTM(train_x, train_y):
    input1 = Input(shape=(train_x[0].shape[0], train_x[0].shape[1]))
    lstm1 = Bidirectional(LSTM(units=62))(input1)
    dnn_hidden_layer1 = Dense(128, activation='relu')(lstm1)
    drop_layer = Dropout(0.1)(dnn_hidden_layer1)
    decoding_layer = RepeatVector(train_y[0].shape[0])(drop_layer)
    output_layer = Bidirectional(LSTM(128, return_sequences=True))(decoding_layer)
    dnn_output = TimeDistributed(Dense(units=train_y[0].shape[1], activation='softmax'))(output_layer)
    model_ = Model(inputs=input1, outputs=dnn_output)

    model_.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model_.summary()
    model_.fit(train_x, train_y, epochs=50, batch_size=128, validation_split=0.2)

    model_.save('model.h5')
    # model_.predict()
    # evaluating
    # loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
    # print("Loss: {0},\nAccuracy: {1}".format(loss, accuracy))


if __name__ == "__main__":
    labelAMR = loadLabel('./data/labelAMR.txt')
    labelPOS = loadLabel('./data/labelPOS.txt')
    phoBert = loadPhoBert('./data/phoBert.txt')
    input_dt, output_dt = load_data('./data', labelAMR, labelPOS, phoBert)
    maxLen = 0
    for i in input_dt:
        if maxLen < len(i):
            maxLen = len(i)
    input_dt = padding(input_dt, maxLen)
    output_dt = padding(output_dt, maxLen)
    x_train, x_test, y_train, y_test = train_test_split(input_dt, output_dt, test_size=0.2)

    writeData('./data/test.txt', x_test, y_test, phoBert, labelPOS, labelAMR)

    # Tranning
    modelLSTM(x_train, y_train)

    # evaluating
    model = load_model('model.h5')
    loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
    print("Loss: {0},\nAccuracy: {1}".format(loss, accuracy))

    # y_predict
    # y_predict = model.predict(x_test, batch_size=128)
    y_predict = model(x_test)
    print(y_predict[0])
    print("=========")
    print(y_test[0])
    writeData('./data/test_predict.txt', x_test, y_predict, phoBert, labelPOS, labelAMR)
