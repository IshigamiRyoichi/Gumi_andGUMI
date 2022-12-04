import os
import cv2
import glob

type_list = ["ボーカロイド", "食べ物"]

for type in type_list:
    os.makedirs("./resize/"+type, exist_ok=True)
    in_dir = "./assets/"+type+"/*.jpg"
    out_dir = "./resize/"+type
    img_list = glob.glob(in_dir)
    for i, img_data in enumerate(img_list):
        img = cv2.imread(img_data)
        img_resize = cv2.resize(img, dsize=(100, 100))
        fileName = os.path.join(out_dir,str(i)+"_"+".jpg")
        cv2.imwrite(str(fileName), img_resize)