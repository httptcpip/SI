# _*_ coding:utf-8 _*_
# @Time: 2022/6/10  20:51
import time

star_time = int(round(time.time()*1000))
while True:
    if((int(round(time.time()*1000))-star_time)>=300):
        star_time+=300
        print(int(round(time.time()*1000)))
