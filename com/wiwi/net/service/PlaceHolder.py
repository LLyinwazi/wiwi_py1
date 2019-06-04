# 测试占位符
print("host:{host}, msg:{msg}".format(**{"host": "wiwi.com", "msg": "success"}))
print("host:%s, msg:%d" % ("wiwi.com", 100))
print("host:{0}, msg:{1}".format("wiwi.com", "success"))