import shutil
import random
import glob
import os

type_list = ["ボーカロイド", "食べ物"]
os.makedirs("./test",exist_ok=True)
for type in type_list:
    in_dir = "./resize/" + type + "/*.jpg"
    jpg_list = glob.glob(in_dir)
    img_file_name_list = os.listdir("./resize/" + type + "/")
    random.shuffle(jpg_list)
    os.makedirs("./test/"+type, exist_ok=True)
    for t in range(len(jpg_list)//5):
        shutil.move(str(jpg_list[t]), "./test/"+type)