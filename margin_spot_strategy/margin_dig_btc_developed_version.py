## 千千量化
## 现货杠杆高频策略源码   开发版本
from fcoin3 import Fcoin
import ccxt
import time
import logging
import threading
import random

'''
from multiprocessing import Pool

def test(p):     
    return p

if __name__=="__main__":
    pool = Pool(processes=10)
    result=[]
    for i  in xrange(50000):
       result.append(pool.apply_async(test, args=(i,)))#维持执行的进程总数为10，当一个进程执行完后添加新进程.       

    pool.join()
    for i in result:
        print i.get()
'''




class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result 
        except:
            return {'asks':[[0, 0]],'bids':[[0, 0]]}


# super params
SYMBOL = 'BTC/USDT'
symbol = 'btcusdt'
price_increment = 0.1
level = 4
ratio = 10
max_ratio = 15
min_ratio = 0
interval = 0.05
s_amount = 0.02
max_amount = 0.4
min_amount = 0.005

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(message)s')
handler = logging.FileHandler("btc_%s.txt" % time.strftime("%Y-%m-%d %H-%M-%S"))
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(console)
logger.addHandler(handler)

f = open('accounts.txt')
lines = f.readlines()
acct_id = int(lines[-1])
api_key = lines[acct_id*2 - 2].strip('\n')
seceret_key = lines[acct_id*2 - 1].strip('\n')
fcoin = Fcoin()
fcoin.auth(api_key, seceret_key)  # fcoin.margin_buy('ethusdt', 0.01, 10)
ex0 = ccxt.fcoin()
ex1 = ccxt.okex3()
ex2 = ccxt.binance()
ex3 = ccxt.huobipro()
type = 'limit'
trend = 0 
trend_0, trend_1, trend_2, trend_3, trend_cmb = [], [], [], [], []
pre_price_0 = 0
pre_price_1, score_1 = 0, 0
pre_price_2, score_2 = 0, 0
pre_price_3, score_3 = 0, 0
pre_price_4, score_4 = 0, 0
pre_price_5, score_5 = 0, 0
pre_price_cmb, score_cmb = 0, 0
buy_id = []
sell_id = []
loop = 0
while True:
    loop += 1
    try:
        # amount = s_amount + random.randint(0, 99) / 100000
    
        # fetch orderbook
        t = []
        result = []
        t.append(MyThread(ex0.fetch_order_book, args=(SYMBOL,)))
        t.append(MyThread(ex1.fetch_order_book, args=(SYMBOL,)))
        t.append(MyThread(ex2.fetch_order_book, args=(SYMBOL,)))
        t.append(MyThread(ex3.fetch_order_book, args=(SYMBOL,)))
        for i in t:
            i.setDaemon(True)
            i.start()
        for i in t:
            i.join()
            result.append(i.get_result())
        price_bid = result[0]['bids'][0][0]
        price_ask = result[0]['asks'][0][0]
        price_0 = (price_bid + price_ask) / 2
        price_1 = (result[1]['bids'][0][0] + result[1]['asks'][0][0]) / 2
        price_2 = (result[2]['bids'][0][0] + result[2]['asks'][0][0]) / 2
        price_3 = (result[3]['bids'][0][0] + result[3]['asks'][0][0]) / 2
        price_cmb = (price_1 + price_2 + price_3)/3
        bidq0, askq0 = result[0]['bids'][0][1], result[0]['asks'][0][1]
        bidq1, askq1 = result[1]['bids'][0][1], result[1]['asks'][0][1]
        bidq2, askq2 = result[2]['bids'][0][1], result[2]['asks'][0][1]
        bidq3, askq3 = result[3]['bids'][0][1], result[3]['asks'][0][1]
        
        # choose trend
        
        if price_0 > pre_price_0 + price_increment: trend_0.append(1)
        if price_0 <= pre_price_0 + price_increment and \
            price_0 >= pre_price_0 - price_increment: trend_0.append(0)
        if price_0 < pre_price_0 - price_increment: trend_0.append(-1)

        if price_1 > pre_price_1 + level * price_increment: trend_1.append(1)
        if price_1 <= pre_price_1 + level * price_increment and \
            price_1 >= pre_price_1 - level * price_increment: trend_1.append(0)
        if price_1 < pre_price_1 - level * price_increment: trend_1.append(-1)

        if price_2 > pre_price_2 + level * price_increment: trend_2.append(1)
        if price_2 <= pre_price_2 + level * price_increment and \
            price_2 >= pre_price_2 - level * price_increment: trend_2.append(0)
        if price_2 < pre_price_2 - level * price_increment: trend_2.append(-1)

        if price_3 > pre_price_3 + level * price_increment: trend_3.append(1)
        if price_3 <= pre_price_3 + level * price_increment and \
            price_3 >= pre_price_3 - level * price_increment: trend_3.append(0)
        if price_3 < pre_price_3 - level * price_increment: trend_3.append(-1)

        if price_cmb > pre_price_cmb + level * price_increment: trend_cmb.append(1)
        if price_cmb <= pre_price_cmb + level * price_increment and \
            price_cmb >= pre_price_cmb - level * price_increment: trend_cmb.append(0)
        if price_cmb < pre_price_cmb - level * price_increment: trend_cmb.append(-1)

        if len(trend_0)>3:
            del(trend_0[0])
            del(trend_1[0])
            del(trend_2[0])
            del(trend_3[0])
            del(trend_cmb[0])
        
        if trend_0[-1] > 0:
            if 1 in trend_1:score_1 += 1
            if 1 in trend_2:score_2 += 1
            if 1 in trend_3:score_3 += 1
            if 1 in trend_cmb:score_cmb += 1
            if -1 in trend_1:score_1 -= 1
            if -1 in trend_2:score_2 -= 1
            if -1 in trend_3:score_3 -= 1
            if -1 in trend_cmb:score_cmb -= 1
        if trend_0[-1] < 0:
            if 1 in trend_1:score_1 -= 1
            if 1 in trend_2:score_2 -= 1
            if 1 in trend_3:score_3 -= 1
            if 1 in trend_cmb:score_cmb -= 1
            if -1 in trend_1:score_1 += 1
            if -1 in trend_2:score_2 += 1
            if -1 in trend_3:score_3 += 1
            if -1 in trend_cmb:score_cmb += 1
        if trend_0[-1] == 0:
            if 1 in trend_1:score_1 -= 0
            if 1 in trend_2:score_2 -= 0
            if 1 in trend_3:score_3 -= 0
            if 1 in trend_cmb:score_cmb -= 0
            if -1 in trend_1:score_1 -= 0
            if -1 in trend_2:score_2 -= 0
            if -1 in trend_3:score_3 -= 0
            if -1 in trend_cmb:score_cmb -= 0

        avg = (score_1 + score_2 + score_3)/3

        trend = trend_1[-1] if score_1 - avg > 0 else 0 + trend_2[-1] if score_2 - avg > 0 else 0 + \
            trend_3[-1] if score_3 - avg > 0 else 0

        # logger.info('price: %f trend:%f score1:%f score2:%f score3:%f scorecmb:%f ' % ( \
        #     price_0, trend, score_1, score_2, score_3, score_cmb))
    
        # record price
        pre_price_0 = price_0
        pre_price_1 = price_1
        pre_price_2 = price_2
        pre_price_3 = price_3
        pre_price_cmb = price_cmb

        # get margin balance
        try:
            balance = fcoin.get_margin_balance()
            if balance['status'] == 'ok':
                for i in balance['data']:
                    if i['leveraged_account_type'] == symbol:
                        if trend > 0:amount = float(i[u'available_quote_currency_amount'])/price_ask - 0.0001
                        if trend < 0:amount = float(i[u'available_base_currency_amount']) - 0.0001
        except:
            amount = s_amount + random.randint(0, 99) * 0.0001

        # create order
        buy_id = []
        sell_id = []
        if trend > 0 and loop > 0:
            try:
                if amount > min_amount:
                    if amount > max_amount:amount = max_amount
                    result = fcoin.margin_buy(symbol, round(price_ask + ratio * price_increment, 1), round(amount, 4))
                buy_id.append(result['data'])
            except Exception as e:
                pass
                # try:
                    # balance = fcoin.get_margin_balance()
                    # for i in balance['data']:
                    #     if i['currency']=='usdt':USDT_amount = float(i['available'])
                    #     if i['currency']=='btc':BTC_amount = float(i['available'])
                    # buy_amount =  USDT_amount/price_ask -0.00001
                    # if buy_amount > min_amount:
                #     result = fcoin.margin_buy(symbol, round(price_bid + ratio * price_increment, 1), round(min_amount, 4))
                #     buy_id.append(result['data'])
                #     logger.info('>> buy   ' + str(price_bid) + '   ' + str(min_amount) + '   ' + str(ratio))
                # except:
                #     pass
        if trend < 0 and loop > 0:
            try:
                if amount > min_amount:
                    if amount > max_amount:amount = max_amount
                    result = fcoin.margin_sell(symbol, round(price_bid - ratio * price_increment, 1), round(amount, 4))
                sell_id.append(result['data'])
            except Exception as e:
                pass
                # try:
                    # balance = fcoin.get_margin_balance()
                    # for i in balance['data']:
                    #     if i['currency']=='usdt':USDT_amount = float(i['available'])
                    #     if i['currency']=='btc':BTC_amount = float(i['available'])
                    # sell_amount =  BTC_amount -0.00001
                    # if sell_amount> min_amount:
                #     result = fcoin.margin_sell(symbol, round(price_ask - ratio * price_increment, 1), round(min_amount, 4))
                #     sell_id.append(result['data'])
                #     logger.info('>> sell   ' + str(price_ask) + '   ' + str(min_amount) + '   ' + str(ratio))
                # except:
                #     pass

        # sleep
        time.sleep(interval)

        # cancel order
        for id in buy_id: 
            try:
                result = fcoin.cancel_order(id)
                if result == None:
                    logger.info('>> buy   ' + str(price_ask) + '   ' + str(amount) + '   ' + str(ratio))
                    if ratio > min_ratio:ratio -= 1
                if result['status'] == 0:
                    logger.info('submit-cancel')
                    if ratio < max_ratio:ratio += 1
            except:
                pass
        for id in sell_id:
            try:
                result = fcoin.cancel_order(id)
                if result == None:
                    logger.info('>> sell   ' + str(price_bid) + '   ' + str(amount) + '   ' + str(ratio))
                    if ratio > min_ratio:ratio -= 1
                if result['status'] == 0:
                    logger.info('submit-cancel')
                    if ratio < max_ratio:ratio += 1
            except:
                pass

    except Exception as e:
        logger.error(e)
