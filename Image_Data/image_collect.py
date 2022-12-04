from icrawler.builtin import BingImageCrawler
type_word_list = ["ボーカロイド", "食べ物"]
select_word_list = ["Gumi", "グミ"]
select_num = 200
for select_word, type in zip(select_word_list, type_word_list):
    crawler = BingImageCrawler(storage={"root_dir": "assets/" + type})
    crawler.crawl(keyword=type+"+"+select_word, max_num=int(select_num))