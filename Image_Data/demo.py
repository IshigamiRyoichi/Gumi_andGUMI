import glob

b_list = glob.glob("./data/ボーカロイド/*")
f_list = glob.glob("./data/食べ物/*")

print(len(b_list))
print(len(f_list))