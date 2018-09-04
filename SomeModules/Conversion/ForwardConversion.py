import requests
import json



base_url = "https://restapi.amap.com/v3/geocode/geo?address="

class ServerError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Conversion():
    '''
    key为高德地图api的key
    '''
    def __init__(self,key='',city=''):
        self.key=key
        self.city=city


    def message(self,msg):
        try:
            specific_address=msg.get('geocodes')[0].get('formatted_address')
            location=msg.get('geocodes')[0].get('location').split(',')
            message=[specific_address,location]
        except:
            message='error'
        return message
            

    def conversion(self,addr=''):
        url=base_url+addr+'&city='+self.city+'&key='+self.key
        conversion = requests.get(url)
        # print(conversion.url)
        if conversion.status_code != 200:
            raise ServerError("server return %s"%conversion.status_code)
        # print(conversion.json())
        return self.message(conversion.json())


if __name__ == '__main__':
    addr=Conversion(key='168b99f6d53264cf074ec1eccbe943c0',city='')
    msg=addr.conversion(addr='火炬大厦')
    print(msg)