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
# profit_down_degree = [] #13年归母净利润相对于前两年的降幅
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


stock_list = ['000968.SZ',	'601918.SH',	 '600408.SH',	 '600397.SH',	 '601011.SH',	 
'601001.SH',	 '600403.SH',	 '601101.SH',	 '600971.SH',	 '000937.SZ',	 '000552.SZ',	 
'600997.SH',	 '600123.SH',	 '601699.SH',	 '002128.SZ',	 '000723.SZ',	 '600395.SH',	 
'601666.SH',	 '000780.SZ',	 '600740.SH',	 '600508.SH',	 '000983.SZ',	 '000571.SZ',	 
'600188.SH',	 '600348.SH',	 '900948.SH',	 '600157.SH',	 '600792.SH',	 '600121.SH',	 
'601088.SH',	 '601898.SH'] #这是删掉2007-2015年有缺失数据的公司之后的股票，共31支


indicator_list = ['销售毛利率','销售费用/营业总收入','管理费用/营业总收入','财务费用/营业总收入',
'销售净利率','资产负债率','流动比率','速动比率','应收账款周转率','固定资产周转率','存货周转率','总资产周转率',
'Z值','带息债务','营运资本','资产总计','负债合计','营业总收入','营业收入','销售费用','管理费用',
'财务费用','营业总成本','营业成本','经营现金流净额','投资现金流净额','现金及等价物净增加额','净利润',
'归属母公司股东的净利润','购建固定无形长期资产支付现金','销售商品劳务收到现金'] #去掉了会计年度和利息支出

stockDF = pd.read_excel("C:/Users/chenchen/Desktop/coalStock_adj.xls") #把excel中的数据再读出来

#del stockDF['利息支出'] 利息支出项均为空值，所以删除

# nan_stock_list = [] #把那些有空值的票给剃掉

# for stock in stock_list_origin:		
# 		single_stock_DF = stockDF[stockDF['股票代码'] == stock]
# 		if single_stock_DF.isnull().any().any() == True:
# 			nan_stock_list.append(stock)

# stock_list = [x for x in stock_list_origin if x not in nan_stock_list] #最终无空值的票的list

# stockDF = stockDF[stockDF['股票代码'].map(lambda x : False if x in nan_stock_list else True)] #处理后的DF,没必要这么复杂，直接用isin即可
# stockDF.to_excel("C:/Users/chenchen/Desktop/coalStock_adj.xls")

date_list = []
for i in range(9):
	date_list.append(dt.datetime(2007+i,1,1))



cost_indicator_list = ['销售毛利率','销售费用/营业总收入','管理费用/营业总收入','财务费用/营业总收入']

fig = figure()

#第一个图：把所有数据都画成散点，新集标红突出
for i,indicator in enumerate(cost_indicator_list):
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

#第二个图：所有的提琴+新集的散点
fig = figure()
for i,indicator in enumerate(cost_indicator_list):
	ax = fig.add_subplot(2,2,i+1)
	#violin_list = [list(stockDF[stockDF['股票代码'] == stock][indicator]) for stock in stock_list]
	#violinDF = 	pd.DataFrame(violin_list,index = stock_list,columns = date_list)
	tmp_data = stockDF[stockDF['股票代码'] == '601918.SH'][indicator]
	gt = ax.scatter(date_list,list(tmp_data),color = 'r',label ='国投新集')
	ax.legend(loc=1)
	sns.violinplot(x = '会计年度', y = indicator, data = stockDF)		
	
	
	years = mdates.YearLocator()
	ax.xaxis.set_major_locator(years)#设置x轴间隔为年

	fmt = mdates.DateFormatter('%Y')
	ax.xaxis.set_major_formatter(fmt)#设置x轴刻度格式为2015这样（只显示Y年）

	ax.set_xlabel(r"年", fontsize=15, color = "r")
	ax.set_ylabel(r"%")
	ax.set_title(indicator)




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
