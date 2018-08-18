try:
    print(x)
except:
    try:
        print(x)
    except Exception as e:
        print('123')
        print(e)
        # pass