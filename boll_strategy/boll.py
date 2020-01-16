# 介绍本次课程内容 本次课程主要讲怎么创造并编写策略 今天的示例策略以boll指标为主  并结合了rsi\atr指标
# 如果还没有观看 趋势框架介绍 指标计算 这两个视频的朋友 请关注微信公众号“千千的量化世界”  微信公众号和github上免费提供本次课程源码
# 喜欢的朋友 请点个赞 欢迎加入我们的量化策略微信讨论群
# 提示：本次课程主要讲怎么编写策略 下次课程再介绍回测  
# BOLL策略
def StrategyBoll(self):
	# 打印本策略开仓情况
	kd, kk, pd, pk = self.kd, self.kk, self.pd, self.pk
	# 准备好策略所需的数据
	upper = self.upper
	middle = self.middle
	lower = self.lower
	rsi = self.rsi6
	atr = self.atr
	trend_cur = upper[-2] - lower[-2]
	trend_pre = upper[-3] - lower[-3]
	# 策略逻辑  
	# 趋势类策略交易原则 严开仓 松平仓 抑制过度交易 同时避免被震出场
	# 获取灵感的方法：1、多看图表；2、加入讨论群交流 
	# 开多条件 开口扩大（波动率扩大） 均线向上（避免逆势） 避免超买时入场 波动率扩大（趋势可能延续）
	if upper[-2] > upper[-3] and middle[-2] > middle[-3] and lower[-2] < lower[-3]\
			and rsi[-2] < 70 and rsi[-2] > 50 and rsi[-2] > rsi[-3] and rsi[-1] < 80 and rsi[-1] > rsi[-2]\
			and atr[-2] > atr[-3] and trend_cur > trend_pre:
		self.kd += self.one_hand
		self.pk += self.one_hand
		if atr[-1] > atr[-2] and rsi[-1] < 60 and rsi[-1] > 50:
			self.kd += self.one_hand
	# 开空条件 开口扩大（波动率扩大） 均线向下（避免逆势） 避免超卖时入场 波动率扩大（趋势可能延续）
	if upper[-2] > upper[-3] and middle[-2] < middle[-3] and lower[-2] < lower[-3]\
			and rsi[-2] > 30 and rsi[-2] < 50 and rsi[-2] < rsi[-3] and rsi[-1] > 20 and rsi[-1] < rsi[-2]\
			and atr[-2] > atr[-3] and trend_cur > trend_pre:
		self.kk += self.one_hand
		self.pd += self.one_hand
		if atr[-1] > atr[-2] and rsi[-1] > 40 and rsi[-1] < 50:
			self.kk += self.one_hand
	# 平仓条件 波动率缩小 价格回归均线
	if upper[-2] < upper[-3] or lower[-2] > lower[-3]:
		if trend_cur < trend_pre and middle[-2] > middle[-3]:
			self.pk += self.one_hand
		if trend_cur < trend_pre and middle[-2] < middle[-3]:
			self.pd += self.one_hand
	self.log.info('策略： BOLL  信号： kd:%d  kk:%d  pd:%d  pk:%d'%(self.kd - kd, self.kk- kk, self.pd - pd, self.pk - pk))