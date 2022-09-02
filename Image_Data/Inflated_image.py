import os
import cv2
import glob

def mosaic(img, scale):
    h,w = img.shape[:2]
    dst = cv2.resize(img, dsize=None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    dst = cv2.resize(dst, dsize=(w, h), interpolation=cv2.INTER_NEAREST)
    return dst

type_list = ["ボーカロイド","食べ物"]
for type in type_list:
    os.makedirs("./data/"+type, exist_ok=True)
    in_dir = "./resize/" + type + "/*.jpg"
    out_dir = "./data/" + type
    jpg_list = glob.glob(in_dir)

    for i, img_data in enumerate(jpg_list):
        img = cv2.imread(img_data)
        fileName = os.path.join(out_dir,str(i)+"_ori.jpg")
        cv2.imwrite(str(fileName), img)
        img_thr = cv2.threshold(img, 80, 255, cv2.THRESH_TOZERO)[1]
        fileName = os.path.join(out_dir,str(i)+"_thr.jpg")
        cv2.imwrite(str(fileName), img_thr)
        img_gas = cv2.GaussianBlur(img, (3, 3), 0)
        fileName = os.path.join(out_dir,str(i)+"_gas.jpg")
        cv2.imwrite(str(fileName), img_gas)
        img_res = cv2.convertScaleAbs(img, alpha=0.6, beta=0.0)
        fileName = os.path.join(out_dir,str(i)+"_res.jpg")
        cv2.imwrite(str(fileName), img_res)
        img_dst = mosaic(img, 0.6)
        fileName = os.path.join(out_dir,str(i)+"_dst.jpg")
        cv2.imwrite(str(fileName), img_dst)