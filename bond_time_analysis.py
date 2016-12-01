import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, draw
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY

import datetime as dt
from WindPy import *
import math

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
sns.set_context("talk")#这一部分是为了保证在画图时正常显示中文

aDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/15A.xlsx")
bDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/15B.xlsx")
cDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/15C.xlsx")


t1 = aDF['证券名称'].drop_duplicates()
t2 = bDF['证券名称'].drop_duplicates()
t3 = [x for x in t1 if x in t2]

t4 = aDF[aDF['证券名称'].duplicated()]['证券名称'].drop_duplicates()

t5 = aDF.groupby('证券名称')['券面总额(万元)'].count()
t5.sort()

aDF['方向'] = aDF['委托方向'].map(lambda x: 1 if x == '3-债券买入' else -1)
aDF['仓位变化'] = aDF['方向']*aDF['券面总额(万元)'] 

t7 = aDF.groupby('证券名称')['仓位变化'].sum() #券面总额(万元)
t7.sort()

t8 = aDF[aDF['证券名称'] == '15国开10']
t8['收益率仓位加权'] = t8['收益率（%）']*t8['仓位变化']

t9 = t8.groupby('成交日期')
t10 = t9['仓位变化'].sum()
sns.barplot(t10.index,t10.values)
t11 = t9['收益率仓位加权'].sum()/t9['仓位变化'].sum()
sns.plt(t11.values)

blank = t10.cumsum().shift(1).fillna(0)
step = blank.reset_index(drop=True).repeat(3).shift(-1)
step[1::3] = np.nan


#画持仓变化结合建仓点位的瀑布图
fig = figure()
ax1 = fig.add_subplot(111)

my_plot = t10.plot(kind='bar', stacked=True, bottom=blank,legend=None, title="150210 各点位持仓变化瀑布图")
my_plot.plot(step.index, step.values,'k')
ax1.legend(loc = 'upper left')

t11 = t9['收益率仓位加权'].sum()/t9['仓位变化'].sum()
ax2=ax1.twinx() #双轴，右轴表示利率
ax2.plot(t11.values,'rx-', label = '建仓平均点位(右轴)')
ax2.legend(loc ='upper right')



#先处理国债曲线
intDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/YC/int.xlsx") #把excel中的数据再读出来
t1 = intDF.T
term_list = list(t1.iloc[0,:])
t1.drop('中债国债',0,inplace=True)
date_list = t1.index.tolist()

t1.columns = term_list
t1['Date'] = date_list
t1['Type'] = 'int'
t1.index = list(range(len(date_list)))

#再处理AA企业债曲线
creditDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/YC/credit.xlsx") 
t2 = creditDF.T
t2.drop('中债企业债AA',0,inplace=True)
t2.columns = term_list
t2['Date'] = date_list
t2['Type'] = 'credit'
t2.index = list(range(len(date_list)))

#把两个处理的DF拼接
t3 = pd.concat([t1,t2])
t3.index = list(range(2*len(date_list)))
new_col_List = ['Type','Date'] + term_list
ycDF = t3[new_col_List]


term_num_list = [float(x[0:4]) for x in term_list]

def linear_ytm(term,bond_type,tr_date): #获取中间节点的
	global ycDF

	up_range = [x for x in term_num_list if x >= term] #找到所有比该券term大的
	down_range = [x for x in term_num_list if x <= term]

	up_term = up_range[0] #第一个为上限
	down_term = down_range[-1]

	up_loc = term_num_list.index(up_term) #找到对应的位置
	down_loc = term_num_list.index(down_term)

	up_ytm = ycDF[(ycDF['Type'] == bond_type)&(ycDF['Date'] == tr_date)].iat[0,2+up_loc] #找到对应的YTM
	down_ytm = ycDF[(ycDF['Type'] == bond_type)&(ycDF['Date'] == tr_date)].iat[0,2+down_loc]

	line_ytm = (up_ytm - down_ytm)*(term - down_term)/(up_term - down_term) + down_ytm

	return	line_ytm
