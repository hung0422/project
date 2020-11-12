from liffpy import LineFrontendFramework as LIFF

liff = LIFF('4/CIQ3/kPw12albwqmprAzy/LZPNJWP6jA2a4HJvEJfn126d3xVEpqV57xnenOUxMqw11ndAxZ5wlO0lEXoF/stW7SISBOpgSfRJ17lERPWm11iaof+EyF+30m3hl0K0YBnTre85z9/xQ45yF+G+JgdB04t89/1O/w1cDnyilFU=')

#liff.add(view_type="tall",view_url='https://www.google.com.tw/webhp?tab=rw')
# url = 'https://liff.line.me/' + liff.add(view_type="tall",view_url='https://e9734a766c0a.ap.ngrok.io/detail/Ub52d90a6b2c9b05bed228af9d7538a6b/1603157435')
print(liff.get())
# print(url)
print(len(liff.get()))
#print(liff.get()[0]['liffId'])

try:
    if len(liff.get()) >= 1:
        for i in range(len(liff.get())):
            print(liff.get()[i]['liffId'])
            #liff.delete(liff.get()[i]['liffId'])
except:
    pass
