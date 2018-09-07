

import requests
import json
from pyquery import PyQuery as pq



def cinema(url,count):
    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    res=requests.get(url,headers=headers)
    if res.status_code==200:
        re=pq(res.text)
        for item in re('.cinema-info').items():
            count+=1
            dic={
                'count':count,
                'name':item('a').text(),
                'addr':item('p').text()
            }
            yield dic
            # print(dic)


if __name__ == '__main__':
    for offset in range(0,15*12,12):
        # print(offset)
        url='http://maoyan.com/cinemas?offset='
        url=url+str(offset)
        print(url)
        cinemas=cinema(url,offset)
        for item in cinemas:
            print(item)
