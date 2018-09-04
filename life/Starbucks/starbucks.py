import requests
import json

url='https://www.starbucks.com.cn/api/stores/nearby?lat=30.287459&lon=120.153576&limit=1000&locale=ZH&features=&radius=100000'
res=requests.get(url)
re=res.json()
count=0
for item in re.get('data'):
    count+=1
    name=item.get('name')
    addrd=item.get('address')
    addr1=addrd.get('city') if addrd.get('city') else '' 
    addr2=addrd.get('streetAddressLine1') if addrd.get('streetAddressLine1') else '' 
    addr3=addrd.get('streetAddressLine2') if addrd.get('streetAddressLine2') else ''
    addr4=addrd.get('streetAddressLine3') if addrd.get('streetAddressLine3') else ''
    addr=addr1+addr2+addr3+addr4
    coordinated=item.get('coordinates')
    coordinate=str(coordinated.get('longitude'))+','+str(coordinated.get('latitude'))
    dic={
        'count':count,
        'name':name,
        'addr':addr,
        'coordinate':coordinate
    }
    print(dic)