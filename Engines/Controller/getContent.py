import _thread
import time, datetime
import pymysql


# 为线程定义一个函数
# def print_time( threadName, delay):
#    # count = 0
#    # while count < 5:
#    #    time.sleep(delay)
#    #    count += 1
#    time.sleep(delay)
#    print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#
# # 创建两个线程
# for i in range(20):
#     try:
#        _thread.start_new_thread(print_time, ("Thread-1-"+str(i), 2, ))
#        _thread.start_new_thread(print_time, ("Thread-2-"+str(i), 4, ))
#     except:
#        print ("Error: 无法启动线程")
#
#     while 1:
#        pass
# timearr = time.strptime("20170802", "%Y%m%d")
# timestamp1 = time.mktime(timearr)
# print(timestamp1)
#
# timearr = time.strptime("20178", "%Y%m")
# timestamp2 = time.mktime(timearr)
# print(timestamp2)
#
# if timestamp1 > timestamp2:
#     print("dayu")

# str = "2017年08月入住"
#
# str.split("年","月")

s = "这是一条带有乱码的评论😅😂"
print(s)

s1 = s.replace("[\\x{10000}-\\x{10ffff}\ud800-\udfff]", "")

# print(s1.encode("utf-8"))
print(type("😂😂"))