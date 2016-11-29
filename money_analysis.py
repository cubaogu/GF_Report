import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure, draw
import matplotlib.dates as mdates

import datetime as dt
from WindPy import *
from math import floor

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
sns.set_context("talk")#这一部分是为了保证在画图时正常显示中文

import re
zhPattern = re.compile(u'[\u4e00-\u9fa5]+') #用来判断一段文本中是否包含简体中文的pattern

moneyDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/money16.xlsx") #把excel中的数据再读出来

moneyDF.drop(0,inplace=True) #删掉首尾两行
moneyDF.drop(7657,inplace=True)

#统计不同回购期限出现的频次
t8 = moneyDF.groupby('证券名称')
t8.委托方向.count() # t8.委托方向.count().plot()

t9 = t8.委托方向.count()
t9.sort(ascending=False)

repotype_list = t9.index.values[0:5]#取最多次数出现的回购期限

#统计不同交易对手出现的频次
t8 = moneyDF.groupby('交易对手')
t8.委托方向.count() # t8.委托方向.count().plot()

t9 = t8.委托方向.count()
t9.sort(ascending=False)

counterparty_count_list = t9.index.values[0:10] #取最多次数出现的交易对手


#统计不同交易对手的成交总额
t8 = moneyDF.groupby('交易对手')# t8.委托方向.count().plot()
t9 = t8['券面总额(万元)'].sum()
t9.sort(ascending=False)

counterparty_sum_list = t9.index.values[0:10] #取最多交易金额的交易对手

#找按交易额和交易笔数前十大交易对手排序中的不同的
c1 = tmp_count.index.tolist()
c2 = tmp_sum.index.tolist()
unique_c = [x for x in c1 if x not in c2] #结果这是一个空集，说明完全重合

#按照交易对手和回购期限分组，画堆积条形图(纵坐标分别是交易的次数和交易的总金额)
t5 = moneyDF[(moneyDF['交易对手'].isin(counterparty_sum_list)) & (moneyDF['证券名称'].isin(repotype_list))].groupby(['交易对手','证券名称'])
t6 = t5['券面总额(万元)'].count() #.sum()

t6.unstack().plot(kind = 'bar',stacked = True) #可以尝试在按照交易对手是银行/基金这些类别作个统计  【还有"交易方向" "交易金额"】
plt.ylabel('交易笔数') #'交易总额(万元)'

#得到交易金额和交易笔数的DF,并混合
t11 = t6.unstack()
t11[np.isnan(t11)] = 0 #获取回购期限*交易对手的交易金额数据（此处也可用np.nan_to_num函数，不过返回不是df了/或者直接apply也可以）


tmp_sum = t11
tmp_count = t11

repo_amount_list = [x+'总额' for x in repotype_list] #生成一个回购期限名称+总额的list
tmp_sum.columns = repo_amount_list

tmp_sum_mix_count = pd.concat([tmp_count,tmp_sum],axis=1) #混合后又有笔数又有金额的DF

#尝试针对金额笔数画一个气泡图,气泡大小代表金额多少

for x in repotype_list:
	x = 'R001'
	fig = figure()
	ax = fig.add_subplot(111)
	
	# t10 = tmp_sum_mix_count[x+'总额'].apply(lambda x:str(x/10**4))
	# list(t10.values)

	ax.scatter(list(range(1,11,1)),tmp_sum_mix_count[x],s=tmp_sum_mix_count[x+'总额']/10**4)
	for a,b,c in zip(list(range(1,11,1)),list(tmp_sum_mix_count[x].values),list(tmp_sum_mix_count[x+'总额'].values/10**4)):
		plt.text(a, b+0.05, '%.0f' % c, ha='center', va= 'bottom',fontsize=7)

	plt.xticks(list(range(1,11,1)),[x.split('-')[1] for x in tmp_sum_mix_count.index.tolist()])
	
	plt.ylabel('交易笔数') #'交易总额(万元)'

	plt.show()
	