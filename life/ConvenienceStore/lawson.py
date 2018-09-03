import requests
import json

class Lawson():
    def __init__(self,city='上海',district='',keyword=''):
        '''city:上海，常熟，常州，杭州，嘉兴，江阴，昆山，南京，宁波，绍兴，苏州，泰州，无锡，扬州，张家港，镇江'''
        
        self.url='http://www.lawson.com.cn/api/v1/stores?city=%s&district=%s&keyword=%s'%(city,district,keyword)

    def get_msg(self):
        res=requests.get(self.url)
        re=res.json()
        count=0
        for item in re:
            count+=1
            name=item.get('name')
            if '店' in name:
                pass
            else:
                name=name+'店'

            address=item.get('district')+item.get('address')
            coords=item.get('coords')

            dic={
                'uid':count,
                'name':name,
                'address':address,
                'coords':coords
            }
            yield dic
            


if __name__ == '__main__':
    lawson=Lawson()
    dics=lawson.get_msg()
    for dic in dics:
        print(dic)
            
