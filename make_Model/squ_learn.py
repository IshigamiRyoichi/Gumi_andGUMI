import glob
import cv2
import numpy as np
from keras.layers import Dense, Dropout, Input,Activation, Conv2D, Flatten, MaxPooling2D
from keras.models import Sequential, Model
from keras.utils.np_utils import to_categorical
from tensorflow.keras.applications.resnet50 import ResNet50
from keras.preprocessing.image import ImageDataGenerator

type_list = ["ボーカロイド", "食べ物"]

X_train = []
y_train = []
i = 0

for type in type_list:
    img_file_name_list = glob.glob("../Image_Data/data/"+type+"/*.jpg")
    for img_data in img_file_name_list:
        img = cv2.imread(img_data)
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        X_train.append(img)
        y_train.append(i)
    i += 1

X_test = []
y_test = []
i = 0
for type in type_list:
    img_file_name_list = glob.glob("../Image_Data/test/"+type+"/*.jpg")
    for img_data in img_file_name_list:
        img = cv2.imread(img_data)
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        X_test.append(img)
        y_test.append(i)
    i += 1

X_train=np.array(X_train)
X_test=np.array(X_test)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

model = Sequential()
#畳み込みオートエンコーダーの動作
#ここの64は画像サイズ
#画像サイズがあっていないと、エラーが発生する
#3×3のフィルターに分ける
model.add(Conv2D(input_shape=(100, 100, 3), filters=32,kernel_size=(5, 5), 
                 strides=(1, 1), padding="same"))
#2×2の範囲で最大値を出力
model.add(MaxPooling2D(pool_size=(2, 2)))
#畳み込みオートエンコーダーの動作
#3×3のフィルターに分ける
model.add(Conv2D(filters=32, kernel_size=(3, 3), 
                 strides=(1, 1), padding="same"))
#2×2の範囲で最大値を出力
model.add(MaxPooling2D(pool_size=(2, 2)))
#畳み込みオートエンコーダーの動作
#3×3のフィルターに分ける
model.add(Conv2D(filters=32, kernel_size=(3, 3), 
                 strides=(1, 1), padding="same"))
#2×2の範囲で最大値を出力
model.add(MaxPooling2D(pool_size=(2, 2)))
#1次元配列に変換
model.add(Flatten())
#出力の次元数を256にする
model.add(Dense(256))
#非線形変形の処理をするらしい
model.add(Activation("sigmoid"))
#出力の次元数を128にする
model.add(Dense(128))
#非線形変形の処理をするらしい
model.add(Activation('sigmoid'))
#出力の次元数を3にする
model.add(Dense(2))
#非線形変形の処理をするらしい
model.add(Activation('softmax'))

# コンパイル
model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 学習
history = model.fit(X_train, y_train, batch_size=8, 
                    epochs=120, verbose=1, validation_data=(X_test, y_test))#validation_data=(X_test, y_test)

# 汎化制度の評価・表示
score = model.evaluate(X_test, y_test, batch_size=8, verbose=0)
print('validation loss:{0[0]}\nvalidation accuracy:{0[1]}'.format(score))

#モデルを保存
model.save("./gumi_squ.h5")