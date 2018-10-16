#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
from pyquery import PyQuery as pq

url = 'https://book.douban.com/review/best/?start='
full = 'https://book.douban.com/j/review/{}/full'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
                  'Safari/537.36'
}
# 爬取前50条书评
for i in range(5):
    page = url + str(i*20)
    html = requests.get(page, headers=headers).text
    doc = pq(html)
    doc.find('.spoiler-tip').remove()   # 移除不必要的标签
    items = doc('.review-list .review-item').items()
    for item in items:
        book = item.find('.subject-img img').attr('alt')    # 书名
        title = item.find('h2').text()  # 书评标题
        author = item.find('.name').text()
        # 获取完整的一条书评
        book_id = item.find('.review-short').attr('data-rid')       # 获取每本书的唯一id
        full_url = full.format(book_id)     # 单条书评链接
        json = requests.get(full_url, headers=headers).json()       # 返回json格式数据
        content = pq(pq(json['html']).html()).text()        # 网页格式化
        # 储存到本地
        file = open('book_review.txt', 'a', encoding='utf-8')
        file.write('\n'.join([book, title, author, content]))
        file.write('\n' + '=' * 50 + '\n')
        file.close()