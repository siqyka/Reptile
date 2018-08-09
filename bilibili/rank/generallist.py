import urllib
import csv



url='https://www.bilibili.com/ranking/all/0/0/3'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}
req=urllib.request.Request(url=url,headers=headers)
res=urllib.request.urlopen(req)

#pyquery
import pyquery
html=pyquery.PyQuery(res.read().decode())
items=html('.rank-list .rank-item').items()
with open('./bilibili/rank/allrang_pq.csv','a') as f:
    fieldnames=['rank','title','view','author','score','url']
    writer=csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    for item in items:
        dic={
        "rank":item('.num').text(),
        "title":item('.info .title').text(),
        "view":item('.info .detail>span:first').text(),
        "author":item('.info .detail a span').text(),
        "score":item('.pts div').text(),
        "url":'https:'+item('.info .title').attr("href")
        }
        writer.writerow(dic)


#xpath

# import lxml
# html=lxml.etree.HTML(res.read().decode())
# ranks=html.xpath('//li[@class="rank-item"]/div[@class="num"]/text()')
# titles=html.xpath('//li[@class="rank-item"]//div[@class="info"]/a/text()')
# views=html.xpath('//li[@class="rank-item"]//div[@class="detail"]/span/text()')
# authors=html.xpath('//li[@class="rank-item"]//div[@class="detail"]/a/span/text()')
# scores=html.xpath('//li[@class="rank-item"]//div[@class="pts"]/div/text()')
# urls=html.xpath('//li[@class="rank-item"]//div[@class="info"]/a/@href')
# with open('./bilibili/rank/allrang_xpath.csv','a') as f:
#     fieldnames=['rank','title','view','author','score','url']
#     writer=csv.DictWriter(f,fieldnames=fieldnames)
#     writer.writeheader()
#     for i in range(len(ranks)-1):
#         dic={
#         "rank":ranks[i],
#         "title":titles[i],
#         "view":views[i],
#         "author":authors[i],
#         "score":scores[i],
#         "url":'https:'+urls[i]
#         }
#         writer.writerow(dic)