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


#来对Bond2015中的初步数据做一些清洗工作
for x in ['A','B','C']:
	origingDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15%s_washed.xlsx"%x)
	origingDF['dir'] = origingDF['direc'].map(lambda x: 1 if x == 3 else -1)
	# origingDF['ct'] = origingDF['ct'].map(lambda x: 1 if x == '是' else 0)
	# origingDF['duration'] = origingDF['dur']
	# origingDF.
[origingDF['opt_dur'] == 0,'duration'] = origingDF[origingDF['opt_dur'] == 0]['dur']

	# washedDF = origingDF.drop(['direc','dur','opt_dur'],axis =1)
	washedDF = origingDF.drop(['direc'],axis =1)
	washedDF.to_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15%s_washed.xlsx"%x)


#清洗后的数据放在Washed文件夹里



aDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15A_washed.xlsx")
bDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15B_washed.xlsx")
cDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15C_washed.xlsx")


t1 = aDF['name'].drop_duplicates()
t2 = bDF['name'].drop_duplicates()
t3 = cDF['name'].drop_duplicates()

t3 = [x for x in t1 if x in t2] #检查ABC里面是否有重叠的

#下面这一部分来增加辅助行
w.start()
for xx in ['A','B','C']:
	aDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15%s_washed.xlsx"%xx)
	#t4 = aDF[aDF['name'].duplicated()]['name'].drop_duplicates()
	# aDF['d_position'] = aDF['dir']*aDF['amount'] 
	# aDF['AI'] = 0.000
	# aDF['help_line'] = 0
	# for i in aDF.index:
	# 	tmp_data = w.wss(aDF.iat[i,1], "accruedinterest","tradeDate=%s;credibility=1"%(str(aDF.iat[i,0]))).Data
	# 	aDF.iat[i,13] = tmp_data[0][0]
				
	t5 = aDF.groupby('code')['d_position'].sum()
	t5.sort(ascending=False)

	ct_func = lambda x: 1 if x =='是' else 0

	for i,x in enumerate(t5.index):
		tmp_amount = int(t5[i])
		if tmp_amount < 0:
			tmp_data = w.wss(x, "yield_cnbd,net_cnbd,accruedinterest,municipalbond,windl1type,sec_name,ptmyear,creditrating","tradeDate=20141231;credibility=1").Data
			ct_sign = ct_func(tmp_data[3][0])
			ddd=pd.Series(['20141231',x,tmp_data[5][0],tmp_data[0][0],tmp_data[1][0],-tmp_amount,tmp_data[4][0],tmp_data[6][0],ct_sign,tmp_data[7][0],0,1,-tmp_amount,tmp_data[2][0],1],index = aDF.columns)
			aDF = aDF.append(ddd,ignore_index=True)
		elif tmp_amount > 0 : 
			tmp_data = w.wss(x, "yield_cnbd,net_cnbd,accruedinterest,municipalbond,windl1type,sec_name,ptmyear,creditrating,maturitydate","tradeDate=20151231;credibility=1").Data
			tmp_mat = int(tmp_data[8][0].strftime("%Y%m%d")) #防止是在2015年底之前到期的，然后还有正持仓的，说明卖出去了
			if  tmp_mat<= 20151231:
				tmp_data = w.wss(x, "yield_cnbd,net_cnbd,accruedinterest,municipalbond,windl1type,sec_name,ptmyear,creditrating,maturitydate","tradeDate=%s;credibility=1"%str(tmp_mat-1)).Data
				ct_sign = ct_func(tmp_data[3][0])
				ddd=pd.Series([str(tmp_mat),x,tmp_data[5][0],tmp_data[0][0],tmp_data[1][0],tmp_amount,tmp_data[4][0],tmp_data[6][0],ct_sign,tmp_data[7][0],0,-1,-tmp_amount,tmp_data[2][0],1],index = aDF.columns)
				aDF = aDF.append(ddd,ignore_index=True)
			else :
				ct_sign = ct_func(tmp_data[3][0])
				ddd=pd.Series(['20151231',x,tmp_data[5][0],tmp_data[0][0],tmp_data[1][0],tmp_amount,tmp_data[4][0],tmp_data[6][0],ct_sign,tmp_data[7][0],0,-1,-tmp_amount,tmp_data[2][0],1],index = aDF.columns)
				aDF = aDF.append(ddd,ignore_index=True)

	aDF.to_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15%s_washed.xlsx"%xx)
	#t4 = aDF[aDF['name'].duplicated()]['name'].drop_duplicates()
w.stop()


#下面开始按规定分类了
aDF = pd.read_excel("C:/Users/chenchen/Desktop/AtWork/TradeAnalysis/Bond2015/Washed/15B_washed.xlsx")

dDF = aDF #之前配平搞错了，下面重新配平

dDF.loc[(dDF['help_line'] == 1)&(dDF['dir'] == -1),'d_position'] = -dDF.loc[(dDF['help_line'] == 1)&(dDF['dir'] == -1),'d_position']

aDF =dDF
t5 = aDF.groupby('code')['d_position'].sum()
t5.sort(ascending=False)

aDF['full_price'] = aDF['AI'] + aDF['cleanP']
aDF['TrueCash'] = aDF['full_price']*aDF['d_position']/100

#对于整个账户所有券种盈利的一个统计
print(aDF['code'].drop_duplicates())
print(aDF[(aDF['help_line'] == 0)&(aDF['dir'] == 1)]['d_position'].count())
print(aDF[(aDF['help_line'] == 0)&(aDF['dir'] == 1)]['d_position'].sum())
print(aDF[(aDF['help_line'] == 0)&(aDF['dir'] == -1)]['d_position'].count())
print(aDF[(aDF['help_line'] == 0)&(aDF['dir'] == -1)]['d_position'].sum())
print(aDF['TrueCash'].sum())


#三类dict
int_standard_dic_1 = {"国债":(9,10.1),"金融债":(9,10.1),"政府支持机构债":(9,10.1)}

int_standard_dic_2 = {"国债":(4,5.1),"金融债":(4,5.1),"政府支持机构债":(4,5.1)}

type_standard_dic = {"中期票据":(4,5.1),"企业债":(6,7.1),"短期融资券":(0,1.1)}

#t6 = aDF.groupby('code').max()

#下面开始各类型的收益输出
for type_key,type_value in int_standard_dic_1.items():
	print(len(aDF[(aDF['type'] == type_key) & (aDF['term']>type_value[0]) & (aDF['term']<type_value[1])]['code'].drop_duplicates()))	
	tmp_qualified_code_list = list(aDF[(aDF['type'] == type_key) & (aDF['term']>type_value[0]) & (aDF['term']<type_value[1])]['code'].drop_duplicates())
	tmp_qualified_code_DF = aDF[aDF['code'].isin(tmp_qualified_code_list)]
	print(tmp_qualified_code_DF[(tmp_qualified_code_DF['help_line'] == 0)&(tmp_qualified_code_DF['dir'] == 1)]['d_position'].count())
	print(tmp_qualified_code_DF[(tmp_qualified_code_DF['help_line'] == 0)&(tmp_qualified_code_DF['dir'] == 1)]['d_position'].sum())
	print(tmp_qualified_code_DF[(tmp_qualified_code_DF['help_line'] == 0)&(tmp_qualified_code_DF['dir'] == -1)]['d_position'].count())
	print(tmp_qualified_code_DF[(tmp_qualified_code_DF['help_line'] == 0)&(tmp_qualified_code_DF['dir'] == -1)]['d_position'].sum())

	print(type_key,tmp_qualified_code_DF['TrueCash'].sum())



#把三个sheet给拼接一下
allDF = pd.concat([aDF,bDF,cDF])

allDF['d_position'] = allDF['dir']*allDF['amount'] 
allDF['dur_weighted_pos'] = allDF['duration']*allDF['d_position']
allDF['dur_weighted_pos_ytm'] = allDF['YTM']*allDF['dur_weighted_pos']

#分一下阶段
periods_list = [[20150101,20150225],[20150225,20150408],[20150408,20150514],[20150514,20150528],[20150528,20151231]]

trading_period = []

def get_period(x):
	tmp_period = 0
	for i,period in enumerate(periods_list):
		if (x <= period[1] and  x > period[0]):
			tmp_period = i
			break
	return tmp_period

allDF['period'] = allDF['date'].map(get_period) #period记录交易的阶段



t7 = allDF.groupby(['period','type'])['d_position'].sum() #amount
#t7.sort(ascending=False)
t8 = allDF.groupby(['period','type'])['dur_weighted_pos_ytm'].sum()/allDF.groupby(['period','type'])['dur_weighted_pos'].sum() #平均建仓YTM
t9 = allDF.groupby(['period','type'])['dur_weighted_pos'].sum()/allDF.groupby(['period','type'])['d_position'].sum() #平均建仓久期


tmpDF = allDF[(allDF['type'] == '企业债') & (allDF['ct'] == 1) & (allDF['term']>6) & (allDF['rating'] == 'AA')]

t7 = tmpDF.groupby('period')['d_position'].sum() #amount
#t7.sort(ascending=False)
t8 = tmpDF.groupby('period')['dur_weighted_pos_ytm'].sum()/tmpDF.groupby('period')['dur_weighted_pos'].sum() #平均建仓YTM
t9 = tmpDF.groupby('period')['dur_weighted_pos'].sum()/tmpDF.groupby('period')['d_position'].sum() #平均建仓久期

tmpDF[(tmpDF['period'] == 4) & (tmpDF['dir'] == 1)][['YTM','period','amount']].sum()
tmpDF[(tmpDF['period'] == 4) & (tmpDF['dir'] == -1)][['YTM','period','amount']].mean() #取其中一类出来看看






sns.barplot(t10.index,t10.values)
#sns.plt(t11.values)

blank = t10.cumsum().shift(1).fillna(0)
step = blank.reset_index(drop=True).repeat(3).shift(-1)
step[1::3] = np.nan


#画持仓变化结合建仓点位的瀑布图
fig = figure()
ax1 = fig.add_subplot(111)

my_plot = t10.plot(kind='bar', stacked=True, bottom=blank,legend=None, title="150210 各点位持仓变化瀑布图")
my_plot.plot(step.index, step.values,'k')
ax1.legend(loc = 'upper left')

for a,b,c in zip(list(range(18)),list(t10.values),list(t10.values)):#画仓位变动量标签,此处需更改
	plt.text(a, b+1000, ('%.1f' % (float(c)/10000 ))+ '亿', ha='center', va= 'bottom',fontsize=15)


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
