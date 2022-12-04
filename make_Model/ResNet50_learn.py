import glob
import cv2
import numpy as np
from keras.layers import Dense, Dropout, Input,Activation, Conv2D, Flatten, MaxPooling2D
from keras.models import Sequential, Model
from keras.utils.np_utils import to_categorical
from tensorflow.keras.applications.resnet50 import ResNet50
from keras.preprocessing.image import ImageDataGenerator

type_list = [ "食べ物","ボーカロイド"]

X_train = []
Y_train = []
i = 0

for type in type_list:
    img_file_name_list = glob.glob("../Image_Data/data/"+type+"/*.jpg")
    for img_data in img_file_name_list:
        img = cv2.imread(img_data)
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        X_train.append(img)
        Y_train.append(i)
    i += 1

X_test = []
Y_test = []
i = 0
for type in type_list:
    img_file_name_list = glob.glob("../Image_Data/test/"+type+"/*.jpg")
    for img_data in img_file_name_list:
        img = cv2.imread(img_data)
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        X_test.append(img)
        Y_test.append(i)
    i += 1

X_train=np.array(X_train)
X_test=np.array(X_test)

Y_train = to_categorical(Y_train)
Y_test = to_categorical(Y_test)

train_datagen = ImageDataGenerator(rescale=1./255, zoom_range=0.3, rotation_range=50,
 width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, 
 horizontal_flip=True, fill_mode='nearest')
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow(X_train, Y_train,batch_size=8)
val_generator = val_datagen.flow(X_test, Y_test, batch_size=8)

# ResnNetの準備
input_tensor = Input(shape=(100, 100, 3))
resnet50 = ResNet50(include_top=False, weights='imagenet', input_tensor=input_tensor)

# FC層の準備
fc_model = Sequential()
fc_model.add(Flatten(input_shape=resnet50.output_shape[1:]))
fc_model.add(Dense(512, activation='relu'))
fc_model.add(Dense(256, activation='relu'))
fc_model.add(Dense(128, activation='relu'))
fc_model.add(Dropout(0.3))
fc_model.add(Dense(2, activation='sigmoid'))

# modelの準備
resnet50_model = Model(resnet50.input, fc_model(resnet50.output))
# #ResNet50の一部の重みを固定
for layer in resnet50_model.layers[:100]:
    layer.trainable = False
resnet50_model.summary()

# コンパイル
resnet50_model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 学習
history = resnet50_model.fit(train_generator, batch_size=8, 
                    epochs=80, verbose=1, validation_data=val_generator)#validation_data=(X_test, y_test)

# 汎化制度の評価・表示
score = resnet50_model.evaluate(X_test, Y_test, batch_size=8, verbose=1)
print('validation loss:{0[0]}\nvalidation accuracy:{0[1]}'.format(score))
print(score)
print(history.history['accuracy'])
print(history.history['val_accuracy'])

#モデルを保存
resnet50_model.save("./gumi_resnet.h5")