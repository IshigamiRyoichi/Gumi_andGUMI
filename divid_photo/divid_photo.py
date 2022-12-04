import shutil
from keras.models import  load_model
import cv2
import glob
import os
import numpy as np

resnet =load_model("./gumi_resnet.h5")
type_list = [ "食べ物","ボーカロイド"]

pos = 0
neg = 0
os.makedirs("./Gumi", exist_ok=True)
os.makedirs("./グミ", exist_ok=True)
for type in type_list:
    img_file_name_list = glob.glob("../ITwitter_Image/gumi_folder/*.jpg")
    for img_data in img_file_name_list:
        img = cv2.imread(img_data)
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        img_exp = np.expand_dims(img,axis=0)
        rate = resnet.predict(img_exp)[0]
        y_p = nameNumLabel=np.argmax(rate)
        if y_p == 0:
            shutil.copy(img_data, "グミ")
        else:
            shutil.copy(img_data, "Gumi")