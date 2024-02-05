a='2022-01-01 00:00:00'
b='2022-01-01 00:00:14'
from cmath import nan
from datetime import datetime
import time
#a=datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
#b=datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
#a = time.strptime(a, "%Y-%m-%d %H:%M:%S")

#a+=1
a = time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S"))
a+=1
#print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(a)))
#print((b-a))
a='2022-01-01 00:00:00'
b='2022-01-01 00:00:05'
a=datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
b=datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
#print(time.mktime(time.strptime(b-a, "%Y-%m-%d %H:%M:%S")))
r=[nan,1,0].dropna()
print(min(r))