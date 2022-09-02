from keras.models import  load_model
import cv2
import glob
import numpy as np
from keras.utils.np_utils import to_categorical

resnet =load_model("./gumi_resnet.h5")
type_list = [ "食べ物","ボーカロイド"]

pos = 0
neg = 0
i = 0
for type in type_list:
    img_file_name_list = glob.glob("../Image_Data/test/"+type+"/*.jpg")
    for img_data in img_file_name_list:
        img = cv2.imread(img_data)
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        img_exp = np.expand_dims(img,axis=0)
        rate = resnet.predict(img_exp)[0]
        print(rate)
        y_p = nameNumLabel=np.argmax(rate)
        # print(y_p)
        if i == y_p:
            pos += 1
        else :
            neg += 1
    i += 1

print(pos / (pos+neg))


