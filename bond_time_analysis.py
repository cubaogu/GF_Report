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
