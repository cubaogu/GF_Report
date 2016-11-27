import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure, draw
import matplotlib.dates as mdates

import datetime as dt
from WindPy import *
from math import floor

stock_list_origin = ['000968.SZ','600546.SH','601918.SH','600408.SH','600397.SH','601011.SH',
'601001.SH','600403.SH','601101.SH','600971.SH','000937.SZ','000552.SZ','600997.SH',
'600123.SH','601699.SH','002128.SZ','000723.SZ','600395.SH','601666.SH','000780.SZ',
'600740.SH','601015.SH','601225.SH','600508.SH','000983.SZ','000571.SZ','600188.SH',
'600348.SH','900948.SH','600157.SH','600792.SH','600121.SH','601088.SH','601898.SH']

# stock_list = []
# profit_down_degree = [] # 计算13年归母净利润相对于前两年的降幅
# for stock in stock_list_origin:
# 	qq = []
# 	for i in range(2011,2014):
# 		td = w.wss(stock, "np_belongto_parcomsh","rptDate=%s1231;rptType=1"%i).Data
# 		qq.append(td[0][0])
# 	if sum([1 if x < 0 else 0 for x in qq ]) == 0: #只考虑2011-2013这三年归母净利润均为正的公司
# 		stock_list.append(stock)
# 		profit_down_degree.append(qq[2]/(qq[0]+qq[1]))



w.start()
all_origin_data = []
for stock in stock_list_origin:
	for i in range(2007,2016):
		tmp_origin = []
		td = w.wss(stock, "grossprofitmargin,operateexpensetogr,adminexpensetogr,finaexpensetogr,netprofitmargin,debttoassets,current,quick,arturn,faturn,invturn,assetsturn,z_score,interestdebt,workingcapital,tot_assets,tot_liab,tot_oper_rev,oper_rev,int_exp,selling_dist_exp,gerl_admin_exp,fin_exp_is,tot_oper_cost,oper_cost,net_cash_flows_oper_act,net_cash_flows_inv_act,net_incr_cash_cash_equ_dm,net_profit_is,np_belongto_parcomsh,cash_pay_acq_const_fiolta,cash_recp_sg_and_rs","rptDate=%s1231;rptType=1"%i).Data
		all_origin_data.append([dt.datetime(i,1,1)] + [x[0] for x in td])
w.stop()



indicator_list = ['会计年度','销售毛利率','销售费用/营业总收入','管理费用/营业总收入','财务费用/营业总收入',
'销售净利率','资产负债率','流动比率','速动比率','应收账款周转率','固定资产周转率','存货周转率','总资产周转率',
'Z值','带息债务','营运资本','资产总计','负债合计','营业总收入','营业收入','利息支出','销售费用','管理费用',
'财务费用','营业总成本','营业成本','经营现金流净额','投资现金流净额','现金及等价物净增加额','净利润',
'归属母公司股东的净利润','购建固定无形长期资产支付现金','销售商品劳务收到现金']

stockDF = pd.DataFrame(all_origin_data,columns=indicator_list)

stockDF['股票代码'] = [stock_list_origin[floor(i/9)] for i in range(306)]

cols = stockDF.columns.tolist()
cols.remove('股票代码')
cols.insert(0,'股票代码')
stockDF = stockDF[cols]
stockDF.to_excel("C:/Users/chenchen/Desktop/coalStock.xls")




###以上是原始数据处理，如果后续处理进来之后需要先读取数据和各种变量
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


stock_list = ['000968.SZ','601918.SH','600408.SH','600397.SH','601011.SH','601001.SH','601101.SH',
 '600971.SH','000937.SZ','600997.SH','600123.SH','601699.SH',	 '002128.SZ',	 '600395.SH',
 '601666.SH',	 '000780.SZ',	 '600740.SH',	 '600508.SH',	 '000983.SZ',	 '000571.SZ',	
 '600188.SH',	 '600348.SH',	 '900948.SH',	 '600157.SH',	 '600792.SH',	 '600121.SH',	 
 '601088.SH',	 '601898.SH']#这是删掉2007-2015年有缺失数据的公司之后的股票，共31支 再删掉缺失固定资产和在建工程的三只，共28只


indicator_list = ['销售毛利率(%)','销售费用率(%)','管理费用率(%)','财务费用率(%)',
'销售净利率(%)','资产负债率(%)','流动比率','速动比率','应收账款周转率','固定资产周转率','存货周转率','总资产周转率',
'Z值','带息债务','营运资本','资产总计','负债合计','营业总收入','营业收入','销售费用','管理费用',
'财务费用','营业总成本','营业成本','经营现金流净额','投资现金流净额','现金及等价物净增加额','净利润',
'归属母公司股东的净利润','购建固定无形长期资产支付现金','销售商品劳务收到现金','固定资产','在建工程','公司规模'] #去掉了会计年度和利息支出

percent_indicator_list = ['销售毛利率(%)','销售费用率(%)','管理费用率(%)','财务费用率(%)','销售净利率(%)','资产负债率(%)']
rate_indicator_list = ['流动比率','速动比率','应收账款周转率','固定资产周转率','存货周转率','总资产周转率','Z值']
amount_indicator_list =  ['带息债务(亿)','营运资本(亿)','资产总计(亿)','负债合计(亿)','营业总收入(亿)','营业收入(亿)','销售费用(亿)','管理费用(亿)',
'财务费用(亿)','营业总成本(亿)','营业成本(亿)','经营现金流净额(亿)','投资现金流净额(亿)','现金及等价物净增加额(亿)','净利润(亿)',
'归属母公司股东的净利润(亿)','购建固定无形长期资产支付现金(亿)','销售商品劳务收到现金(亿)','固定资产(亿)','在建工程(亿)']

#indicator_list = percent_indicator_list+rate_indicator_list+amount_indicator_list +['公司规模']

#stockDF.columns = ['股票代码','会计年度']+indicator_list #改变column指标名字

stockDF = pd.read_excel("C:/Users/chenchen/Desktop/coalStock_adj2.xls") #把excel中的数据再读出来

#stockDF['会计年度'] = stockDF['会计年度'].map(lambda x:x.year)#先尝试了一个，时间改成年度，即从datetime类型改成整数类型

#此处是增加固定资产和在建工程指标的，再重新存储下
# w.start()
# all_origin_data = []
# for stock in stock_list:
# 	for i in range(2007,2016):
# 		td = w.wss(stock, "const_in_prog","rptDate=%s1231;rptType=1"%i).Data #fix_assets
# 		all_origin_data.append(td[0][0])
# stockDF['在建工程'] = all_origin_data #固定资产
# w.stop()

# stockDF.to_excel("C:/Users/chenchen/Desktop/coalStock_adj.xls")


date_list = []
for i in range(9):
	date_list.append(dt.datetime(2007+i,1,1))

cost_indicator_list = ['销售毛利率','销售费用/营业总收入','管理费用/营业总收入','财务费用/营业总收入']

#del stockDF['利息支出'] 利息支出项均为空值，所以删除

# nan_stock_list = [] #把那些有空值的票给剃掉

# for stock in stock_list:		
# 		single_stock_DF = stockDF[stockDF['股票代码'] == stock]
# 		if single_stock_DF.isnull().any().any() == True: #此处也可以考虑用groupby筛选
# 			nan_stock_list.append(stock)
nan_stock_list = ['600403.SH', '000552.SZ', '000723.SZ'] #固定资产、在建工程项没有的

stock_list = [x for x in stock_list if x not in nan_stock_list] #最终无空值的票的list

stockDF = stockDF[stockDF['股票代码'].isin(stock_list)] #map(lambda x : False if x in nan_stock_list else True)] #处理后的DF,没必要这么复杂，直接用isin即可
stockDF.to_excel("C:/Users/chenchen/Desktop/coalStock_adj2.xls")

#把数量型指标除以10**8，改成以亿为单位
for indicator in amount_indicator_list:
	stockDF[indicator] = stockDF[indicator]/10**8



#1. 第一个图：把所有数据都画成散点，新集标红突出
fig = figure()
for i,indicator in enumerate(cost_indicator_list): #注意：其实使用groupby就能完成很多初步处理了，只不过比较粗糙
	ax = fig.add_subplot(2,2,i+1)
	for stock in stock_list:		
		tmp_data = stockDF[stockDF['股票代码'] == stock][indicator]
		try:
			if stock == '601918.SH':
				gt = ax.scatter(date_list,list(tmp_data),color = 'r',label ='国投新集')
				ax.legend(loc=1)
			else:
			 	ax.scatter(date_list,list(tmp_data))

		except ValueError:
			print(stock,indicator)

	years = mdates.YearLocator()
	ax.xaxis.set_major_locator(years)#设置x轴间隔为年

	fmt = mdates.DateFormatter('%Y')
	ax.xaxis.set_major_formatter(fmt)#设置x轴刻度格式为2015这样（只显示Y年）

	ax.set_xlabel(r"年", fontsize=15, color = "r")
	ax.set_ylabel(r"%")
	ax.set_title(indicator)

#2. 第二个图：所有的提琴+新集的散点
stockDF['会计年度'] = stockDF['会计年度'].map(lambda x:x.year)#先尝试了一个，时间改成年度，即从datetime类型改成整数类型

fig = figure()
for i,indicator in enumerate(cost_indicator_list):
	ax = fig.add_subplot(2,2,i+1)
	# violin_list = [list(stockDF[stockDF['股票代码'] == stock][indicator]) for stock in stock_list]
	# violinDF = pd.DataFrame(violin_list,index = stock_list,columns = date_list)
	# ax.violinplot(violinDF.values,showmeans=False,showmedians=True)
	# sns.lmplot(x = '会计年度', y = indicator, data=tmp_data, fit_reg=False, dropna=True,hue="z",scatter_kws={"marker": "D", "s": 100})
	# plt.setp(ax, xticks=[y+1 for y in range(len(date_list))],xticklabels=date_list)
	
	tmp_data = stockDF[stockDF['股票代码'] == '601918.SH'][indicator]	
	gt = ax.plot(list(tmp_data),color = 'r',label ='国投新集')
	ax.legend(loc=1)

	sns.violinplot(x = '会计年度', y = indicator, data = stockDF)
	ax.set_ylabel(r"")
	ax.set_xlabel(r"") #尝试学习如何调整图与画图区域之间的空隙距离大小
	ax.set_title(indicator+r"%",fontsize = 11, color = "b") #注意，有些字体并不是所有字号都能用，比如雅黑就不能用10，多试几次

	

#3. 下面针对所有的指标。每个指标生成一个提琴图并保存
stockDF['会计年度'] = stockDF['会计年度'].map(lambda x:x.year)#先尝试了一个，时间改成年度

t_indicator_list = ['固定资产'] #购固现金流占比']
for i,indicator in enumerate(percent_indicator_list):
	fig = figure()
	ax = fig.add_subplot(111)
	
	tmp_data = stockDF[stockDF['股票代码'] == '601918.SH'][indicator] #/10**8需要除以亿的时候	
	gt = ax.plot(list(tmp_data),'ro-',label ='国投新集')
	# tmp_stockDF = stockDF
	# tmp_stockDF[indicator] = tmp_stockDF[indicator]/10**8 #需要除以亿的时候	，下面用tmp_stockDF

	sns.violinplot(x = '会计年度', y = indicator, hue = '公司规模', data = stockDF,cut = 0, inner="quartile",split=True)
	ax.legend(loc='best',ncol = 3)
	# hue="sex",scale="count",inner="quartile")hue可以用来再制定分类比较,可以指定ax来画否则默认当前ax，返回值也是一个ax类型
	# ax.set_ylabel(r"") #设置坐标轴标签，可以加"亿"或者"%"
	# ax.set_xlabel(r"") #尝试学习如何调整图与画图区域之间的空隙距离大小
	# ax.set_title(indicator,fontsize = 15, color = "b") #注意，有些字体并不是所有字号都能用，比如雅黑就不能用10，多试几次

	pic_name = "C:/Users/chenchen/Desktop/ViolinGraphs/Percent/%s.png"%indicator
	fig.savefig(pic_name)

#画图之后看一看如果有极端异常点，找出异常点是哪家公司
t2 = stockDF[stockDF['会计年度'] == 2015]
t2.sort(columns = ['财务费用率(%)'])[['股票代码','财务费用率(%)']]

t3 = stockDF[stockDF['会计年度'] == 2014].sort(columns = ['财务费用率(%)'],ascending=False)['股票代码'].values
t3[0]


#4. 构造一些新的指标,比如单独画一下有息债务的增长量
stockDF['购固现金流占比'] = stockDF['购建固定无形长期资产支付现金']/stockDF['资产总计']
stockDF['有息债务率'] = stockDF['带息债务']/stockDF['资产总计']
stockDF['有息债务增量'] = stockDF['带息债务'].diff()
stockDF['有息债务增率'] = stockDF['有息债务增量']/stockDF['带息债务']

stockDF['过去两年平均净利'] = (stockDF['净利润'].shift(1) + stockDF['净利润'].shift(2))/2
stockDF['净利相对两年平均增幅'] = (stockDF['净利润']-stockDF['过去两年平均净利'])/stockDF['过去两年平均净利']



fig = figure()#此处专门画一下有息债务增率，首先剔除2007年，其次把为Nan和inf(从0增长的)都剔除掉
ax = fig.add_subplot(111)

indicator = '净利相对两年平均增幅'
tmp_data = stockDF[(stockDF['会计年度'] != 2007) & (stockDF['会计年度'] != 2008)& (stockDF['股票代码'] == '601918.SH')][indicator]	
gt = ax.plot(list(tmp_data),color = 'r',label ='国投新集')
ax.legend(loc=1)
sns.violinplot(x = '会计年度', y = indicator, data = stockDF[(stockDF['会计年度'] != 2007) & (stockDF['会计年度'] != 2008) & (np.isnan(stockDF[indicator]) == False) & (np.isinf(stockDF[indicator]) == False)],cut = 0, inner="quartile")


#按主营业务收入区分公司规模，大公司标记1，小公司标记0(直接改为D大公司小公司)


rev_mean_2012 = stockDF[stockDF['会计年度'] == 2012]['营业总收入'].mean()

t3 = stockDF[(stockDF['会计年度'] == 2012) & (stockDF['营业总收入'] > rev_mean_2012)]['股票代码']
t4 = t3.drop_duplicates()
big_list = [x for x in t4]

#big_list = ['601088.SH','600546.SH','601898.SH','600348.SH','600188.SH','601225.SH','000983.SZ','000937.SZ'] #这是按2012年超过行业营业收入均值来排

stockDF['公司规模'] = ['小公司' for i in range(279)]

stockDF.loc[stockDF['股票代码'].isin(big_list),'公司规模'] = '大公司'

stockDF.loc[stockDF['股票代码'].isin(big_list),'公司规模'].apply(lambda x:  if x ==1 else 0)

stockDF.loc[:,'公司规模'].apply(lambda x: "大公司" if x ==1 else "小公司")

t5 = stockDF.loc[:,'公司规模'].map(lambda x: "大公司" if x ==1 else "小公司").values
t6 = [x for x in t5]
del stockDF['公司规模']
stockDF['公司规模'] = t6

#下面试一下分大公司和小公司画提琴图
fig = figure()
ax = fig.add_subplot(111)

tmp_data = stockDF[stockDF['股票代码'] == '601918.SH']['销售毛利率(%)'] #/10**8需要除以亿的时候	
gt = ax.plot(list(tmp_data),'ro-',label ='国投新集')
sns.violinplot(x = '会计年度', y = '销售毛利率(%)', hue = '公司规模', data = stockDF,cut = 0, inner="quartile",split=True)
ax.legend(loc='upper left',ncol = 3)


#!!!这一段为了找出2011年和2012年净利均不为负的股票代码
# tt = stockDF[stockDF['会计年度'] == 2011][['股票代码','净利润']]

# tt[tt['净利润']<0].股票代码 # 600408.SH5      000968.SZ 000723.SZ 600792.SH

# neg1112_list = ['600408.SH','000968.SZ', '000723.SZ','600792.SH']
# non_neg_list = [x for x in stock_list if x not in neg1112_list]

# profit_list = []

# for x in non_neg_list:
# 	single_profit = []
# 	for i in range(2011,2014):
# 		tt = stockDF[(stockDF['会计年度']== i) & (stockDF['股票代码'] == x)]['归属母公司股东的净利润']
# 		single_profit.append(tt.values[0])
# 	profit_list.append(single_profit)

# profitDF = pd.DataFrame(profit_list,index = non_neg_list, columns=list(range(2011,2014)))

# profitDF.to_excel("C:/Users/chenchen/Desktop/profit2011to2013.xls")



fig = figure()
ax = fig.add_subplot(111)
ax.scatter(list(range(10)),list(range(10)),label = '陈陈')
ax.legend()

ax = fig.add_subplot(111)
ax.scatter(date_list,list(df1[0]))

years = mdates.YearLocator()
ax.xaxis.set_major_locator(years)#设置x轴间隔为年

fmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_formatter(fmt)#设置x轴刻度格式

fig.autofmt_xdate()
draw()
