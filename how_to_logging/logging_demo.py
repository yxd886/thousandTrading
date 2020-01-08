# 千千量化
# 记录日志的DEMO
import  logging
import  time


def  initLog():
    log  =  logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    #  输出到txt
    formatter  =  logging.Formatter('[%(asctime)s]  %(message)s')
    handler  =  logging.FileHandler("log_%s.txt"  %  time.strftime("%Y-%m-%d  %H-%M-%S"))
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    #  输出到控制台
    console  =  logging.StreamHandler()
    console.setLevel(logging.INFO)
    #  将输出添加到log
    log.addHandler(handler)
    log.addHandler(console)
    # 返回log
    return log

if  __name__  ==  "__main__":
    # 实例化
    log  =  initLog()
    while  True:

        log.info("这里写打印信息，可以同时打印到控制台和日志文档中")
        time.sleep(5)