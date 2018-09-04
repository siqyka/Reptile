import requests
import json



base_url = 'http://116.196.105.215:1234/gis?auth_user=freevip&latitude=%s&longitude=%s'

class ServerError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class TypeError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class ReverseConversion():

    def message(self,msg):
        try:
            data=msg.get('data')
            if data.get('country')!='CHN':
                message=''
                for en in data.values():
                    if en:
                        en=en+','
                        message+=en
            else:
                message=''
                for en in data.values():
                    if en:
                        en=en+','
                        message+=en
            message=message[4:-2:]
        except:
            message='error'
        return message
            

    def conversion(self,*args):
        if len(args)==1:
            if len(args[0])==2:
                url=base_url%(args[0][1],args[0][0])
            else:
                raise TypeError("The number of iterable objects must be two (%s given)"%len(args[0]))

        elif len(args)==2:
            url=base_url%(args[1],args[0])
        else:
            raise TypeError("conversion() takes exactly one argument or iterable objects of length two(%s given)"%len(args))
        
        print(url)
        conversion = requests.get(url)
        # print(conversion.url)
        if conversion.status_code != 200:
            raise ServerError("server return %s"%conversion.status_code)
        # print(conversion.json())
        return self.message(conversion.json())


if __name__ == '__main__':
    addr=ReverseConversion()
    msg=addr.conversion(102.319375,17.305084)
    print(msg)