# 快速速成python量化交易  从如何阅读和编写量化交易源代码为切入点带大家一起入门python
# Python下载安装https://www.python.org/  版本：3.7.2
# 编程工具下载安装：VSC: https://code.visualstudio.com/   Pycharm: https://www.jetbrains.com/pycharm/
# 在本地测试需要vpn，因大家都懂的原因在此不多说，需要的朋友可以在讨论群提问

# 系统自带模块
import time
# 从第三方导入模块 pip install ccxt  GITHUB  CCXT
import ccxt

# 自定义类 （策略 + 框架）
class TrendStrategy():
    # 构造函数
    def __init__(self, api_key, secret_key):
        # 赋值 字符串
        self.name = 'qianqiancelue' + '20200105'
        # 实例化一个外部类 需要传入一个字典 dict {}
        self.api = ccxt.fcoin({'apiKey':api_key, 'secret':secret_key})
        # 声明列表 list []
        self.orders_id = []
        # 往列表添加元素
        self.orders_id.append(str(666))
        self.orders_id.append(int('888'))
        # for 循环遍历 同时 赋值
        for item in self.orders_id:
            print(item)  # '666' 888
        # 删除元素
        del(self.orders_id[1]) # delete 888
        del(self.orders_id[0]) # delete '666'
        # 赋值 整型
        self._time_interval = 10

    # 成员函数（内部）
    # 下单函数 传入参数 下单方向 数量 价格
    def _placeOrder(self, _side, _amount, _price):
        # if 语句结构 = 赋值 == 逻辑判断
        if _side == 'buy':
            # run part A
            result = self.api.create_order('BTC/USDT', 'limit', 'buy', _amount, _price)
        # is 也是判断
        elif _side is 'sell':
            # run part B
            result = self.api.create_order('BTC/USDT', 'limit', 'sell', _amount, _price)
        # in 也是判断
        elif _side not in ['buy', 'sell']:
            # run part C
            print('下单方向出错！')
            result = []
        else:
            # run part D
            print('下单方向出错！')
            result = []
        return result

    # 成员函数（外部）
    # 策略运行主函数
    def run(self):
        # bool 型 True False
        flag = True
        # 循环
        while flag:

            # 查询策略是否正常运行
            print('策略名称' + self.name + '正在运行！')

            # 通过API来访问行情 从交易所的服务器
            ticker = self.api.fetch_ticker('BTC/USDT')

            # ticker 是 dict 字典
            last_price = ticker['last']
            bestask = ticker['ask']
            bestbid = ticker['bid']

            # 浮点数 赋值
            amount = 0.123

            # 数学运算 加减乘除
            amount = amount + 0.0004  # 0.1234
            amount += 0.0004  # 0.1238
            amount -= 0.0004  # 0.1234
            amount *= 2       # 0.2468
            amount /= 2       # 0.1234

            # 取整 0.001  0.0005 1.0005 精度取舍
            amount = round(amount, 3) # 0.123

            # 字符串 赋值 运算 切片
            side = 'buy' + 'sell'  # 'buysell'
            side += 'qianqianlianghua'  # 'buysellqianqianlianghua'
            side = side[:3]  # 'buy'

            # 产生交易信号 （策略核心）
            if True:
                try:
                    # run place order
                    orderState = self._placeOrder(side, amount, last_price)
                except Exception as error:
                    # part B
                    print('下单出错!')
                    print(error)
                    orderState = {'id': '', 'info': 'place order wrong!'}
            
            # 记录订单号
            self.orders_id.append(orderState['id'])
            # print(self.orders_id[2:5])

            # 限制运行频率
            time.sleep(self._time_interval)
                
            
            # 判断策略是否应该继续运行
            # if time.time() is trading_time:
            #     flag = False



api_key = 'c778848925934310a15db6755659c4af'
secret_key = 'd7c9a9a9ced84200afe4f51a8e1bdc01'
myStrategy = TrendStrategy(api_key, secret_key)
myStrategy.run()