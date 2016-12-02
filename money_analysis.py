import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure, draw
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY


import datetime as dt
from WindPy import *
from math import floor

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
sns.set_context("talk")#这一部分是为了保证在画图时正常显示中文

import re
zhPattern = re.compile(u'[\u4e00-\u9fa5]+') #用来判断一段文本中是否包含简体中文的pattern

moneyDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/money15.xls") #把excel中的数据再读出来

moneyDF.drop(0,inplace=True) #删掉首尾两行
moneyDF.drop(8326,inplace=True)

#统计不同回购期限出现的频次
t8 = moneyDF.groupby('证券名称')
t8['券面总额(万元)'].count() # t8.委托方向.count().plot()

t9 = t8['券面总额(万元)'].count()
t9.sort(ascending=False)

repotype_list = t9.index.values[0:3]#取成交次数前3多的期限(001,007,014)
repotype_list = ['R001','R007','R014']

#统计不同交易对手出现的频次
t8 = moneyDF.groupby('交易对手')
t8['券面总额(万元)'].count() # t8.委托方向.count().plot()

t9 = t8['券面总额(万元)'].count()
t9.sort(ascending=False)

counterparty_count_list = t9.index.values[0:10] #取最多次数出现的交易对手


#统计不同交易对手的成交总额
t8 = moneyDF.groupby('交易对手')# t8.委托方向.count().plot()
t9 = t8['券面总额(万元)'].sum()
t9.sort(ascending=False)

counterparty_sum_list = t9.index.values[0:10] #取最多交易金额的交易对手

#找按交易额和交易笔数前十大交易对手排序中的不同的
# c1 = tmp_count.index.tolist()
# c2 = tmp_sum.index.tolist()
# unique_c = [x for x in c1 if x not in c2] #结果这是一个空集，说明完全重合

#按照交易对手和回购期限分组，画堆积条形图(纵坐标分别是交易的次数和交易的总金额)
t5 = moneyDF[(moneyDF['交易对手'].isin(counterparty_sum_list)) & (moneyDF['证券名称'].isin(repotype_list))].groupby(['交易对手','证券名称'])
t6 = t5['券面总额(万元)'].sum() #.sum()

t7 = t6.unstack()
t7['sum'] = t7.sum(1)
t7.sort(['sum'],ascending= False,inplace=True)
del (t7['sum'])

t7.plot(kind = 'bar',stacked = True) #可以尝试在按照交易对手是银行/基金这些类别作个统计  【还有"交易方向" "交易金额"】
plt.ylabel('交易总额(万元)') #'交易总额(万元)'


#对重要交易对手的笔数和金额数据单独拎出来
important_partners = ["105911-工商银行","104714-光大银行","105947-北京银行","105204-邮储银行","104099-包商银行","102851-成都农商银行"]
important_partners_names = [x.split('-')[1] for x in important_partners]


important_counts = [334,421,615,512,922,732]
important_amounts = [3734.27,3462.68,3146.39,3014.94,893.98,1721.08]
important_avgs = [important_amounts[i]/important_counts[i] for i in range(6)]

impDF = moneyDF[moneyDF['交易对手'].isin(important_partners)]

impDF['交易对手'] = impDF['交易对手'].map(lambda x: x.split('-')[1])


impDF['券面总额(亿)'] = impDF['券面总额(万元)']/10**4

#重要对手气泡图
fig = figure()
ax = fig.add_subplot(111)
plt.ylim(0,1200)

	
ax.scatter(list(range(0,6)),important_counts,s=important_amounts*10**4)

for a,b,c in zip(list(range(0,6)),important_counts,important_amounts):
		plt.text(a, b+100, '%.0f' % c + '亿', ha='center', va= 'bottom',fontsize=15)

plt.ylabel("交易笔数和总额")
plt.xticks(list(range(-1,7)),['']+important_partners_names+[''])


#重要对手提琴图
fig = figure()
ax = fig.add_subplot(111)
sns.violinplot(x = '交易对手', y = '券面总额(亿)', data = impDF,order = important_partners_names,cut = 0)

ax.plot([3.93 for x in range(6)],'r',label= '所有交易笔均交易额3.93亿') #画出一条代表所有机构笔均交易金额的水平横线
ax.legend()


plt.ylabel("单笔交易金额分布和均值")
for a,b,c in zip(list(range(6)),important_avgs,important_avgs): #把均值在提琴图上标注出来
		plt.text(a+0.3, b+0.05, '%.2f' % c + '亿', ha='center', va= 'bottom',fontsize=15,color = 'b')






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
	#x = 'R001'
	fig = figure()
	ax = fig.add_subplot(111)
	ax.set_title("前十大交易对手总笔数vs总金额")
	plt.xlim(-0.5,10.5)
	
	# t10 = tmp_sum_mix_count[x+'总额'].apply(lambda x:str(x/10**4))
	# list(t10.values)

	ax.scatter(list(range(1,11,1)),tmp_sum_mix_count[x],s=tmp_sum_mix_count[x+'总额']/10**4)
	
	for a,b,c in zip(list(range(1,11,1)),list(tmp_sum_mix_count[x].values),list(tmp_sum_mix_count[x+'总额'].values/10**4)):
		plt.text(a, b+0.05, '%.0f' % c + '亿', ha='center', va= 'bottom',fontsize=15)

	plt.xticks(list(range(1,11,1)),[x.split('-')[1] for x in tmp_sum_mix_count.index.tolist()])
	
	plt.ylabel(x+'交易笔数') #'交易总额(万元)'

	plt.show()



#算每个交易对手每种期限的回购在每天的平均资金利率(再尝试画一个分布？boxplot)
moneyDF['日利息'] = moneyDF['券面总额(万元)']*moneyDF['回购/拆借利率(%)'] #增加一个日利息项用于下面算加权平均利率

t0 = moneyDF.groupby(['交易对手','证券名称','成交日期'])

t1 = t0['券面总额(万元)']
t2 = t0['日利息']

t3 = t2.sum()/t1.sum()

t4 = list(t3.index)
t5 = pd.DataFrame(t4)
t5['加权利率'] = list(t3.values)
t5.columns = ['交易对手','证券名称','成交日期','加权利率'] # t5就是每天每家对手每个期限的加权资金利率

change_tr_date = lambda x : dt.datetime.strptime(str(x), "%Y%m%d")

t5['新日期'] = t5['成交日期'].map(change_tr_date)#日期换成datetime的格式

#下面算一下每天每种期限的价格作为画图时候的参考标准线
t11 = moneyDF.groupby(['证券名称','成交日期'])
t12 = t11['券面总额(万元)']
t13 = t11['日利息']

t14 = t13.sum()/t12.sum()

t15 = list(t14.index)
t16 = pd.DataFrame(t15)
t16['加权利率'] = list(t14.values)
t16.columns = ['证券名称','成交日期','加权利率'] 

t16['新日期'] = t16['成交日期'].map(change_tr_date)


fig = figure(figsize=(18,9))
for i,y in enumerate(['R001']):#,'R007']):
	ax = fig.add_subplot(1,2,i+1)
	plt.ylim(0.5+i,5.5+i)
	#plt.yticks(list(range(1.8,4.0,0.2)),[(str(mm)[0]+'.'+str(mm)[1]) for mm in range(18,40,2)])

	ax.set_title('重要交易对手%s平均利率(日)'%y)
	months = mdates.MonthLocator()
	ax.xaxis.set_major_locator(months)#设置x轴间隔为月

	fmt = mdates.DateFormatter('%b')
	ax.xaxis.set_major_formatter(fmt)#设置x轴刻度格式

	t17 = t16[t16['证券名称'] == y] #先画平均值的参考线
	ax.plot(t17['新日期'],t17['加权利率'],color="#000000",linestyle='-.',label='当日所有成交平均',linewidth=3)

	for x in important_partners: 
		t10 = t5[(t5['交易对手'] == x) & (t5['证券名称'] == y)]
		ax.plot(t10['新日期'],t10['加权利率'],label = x.split('-')[1] )
		ax.legend(ncol =3)

	#plt.xticks(list(range(0,9)),[str(x+1)+'月' for x in range(9)])

#算一下年度的均值和标准差
int_mean = []
int_std= []
for x in important_partners: 
		t10 = t5[(t5['交易对手'] == x) & (t5['证券名称'] == 'R001')]
		int_mean.append(t10['加权利率'].mean())
		int_std.append(t10['加权利率'].std())

t17 = t16[t16['证券名称'] == 'R001']
t17['加权利率'].mean()
t17['加权利率'].std()

#画每天的