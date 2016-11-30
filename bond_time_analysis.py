import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure, draw
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY


import datetime as dt
from WindPy import *
import math

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
sns.set_context("talk")#这一部分是为了保证在画图时正常显示中文

intDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/YC/int.xlsx") #把excel中的数据再读出来
t1 = intDF.T
t2 = list(t1.iloc[1,:])	
t1.drop('Term',0,inplace=True)
t1.drop('Type',0,inplace=True)
t1.columns = t2
t1['Type'] = 'int'

creditDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/YC/credit.xlsx") 
t3 = creditDF.T
t4= list(t3.iloc[1,:])	
t3.drop('Term',0,inplace=True)
t3.drop('Type',0,inplace=True)
t3.columns = t4
t3['Type'] = 'credit'

#直接点
t3.columns = ['TradingDate',0.0^^^]

def linear_ytm(term,type,tr_date):
	up_term = math.ceil(term)
	down_term = math.floor(term)

	ycDF[ycDF['Type'] == type][]