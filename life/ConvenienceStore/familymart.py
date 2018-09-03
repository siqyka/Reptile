import requests
import json

class FamilyMart():
    def __init__(self,cid):

        self.url='http://www.familymart.com.cn/store/Search'

        self.data={
            'cid': str(cid),  #城市编码：1--上海，2--苏州,3--深圳,4--广州,5--杭州,6--成都,7--无锡,8--北京,9--东莞
            'page': '1'
            }

    def get_msg(self):
        res=requests.post(self.url,data=self.data)
        re=res.json()
        mapmsg=re.get('mapmsg')
        # print(mapmsg)
        count=0
        for item in mapmsg:
            count+=1
            name=item['name'],
            street=item['street'],
            telphone=item['telphone']
            if telphone:
                dic={
                    'uid':count,
                    'name':name[0],
                    'address':street[0],
                    'telphone':telphone
                }
            else:
                dic={
                    'uid':count,
                    'name':name[0],
                    'address':street[0],
                    'telphone':''
                }
            yield dic
            

if __name__ == '__main__':
    familymart=FamilyMart(1)
    dics=familymart.get_msg()
    for dic in dics:
        print(dic)
