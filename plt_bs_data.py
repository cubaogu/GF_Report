import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure, draw
import matplotlib.dates as mdates

from datetime import datetime, timedelta
from WindPy import *

stock_list_origin = ['000968.SZ','600546.SH','601918.SH','600408.SH','600397.SH','601011.SH',
'601001.SH','600403.SH','601101.SH','600971.SH','000937.SZ','000552.SZ','600997.SH',
'600123.SH','601699.SH','002128.SZ','000723.SZ','600395.SH','601666.SH','000780.SZ',
'600740.SH','601015.SH','601225.SH','600508.SH','000983.SZ','000571.SZ','600188.SH',
'600348.SH','900948.SH','600157.SH','600792.SH','600121.SH','601088.SH','601898.SH']

stock_list = []
profit_down_degree = [] #13年归母净利润相对于前两年的降幅
for stock in stock_list_origin:
	qq = []
	for i in range(2011,2014):
		td = w.wss(stock, "np_belongto_parcomsh","rptDate=%s1231;rptType=1"%i).Data
		qq.append(td[0][0])
	if sum([1 if x < 0 else 0 for x in qq ]) == 0: #只考虑2011-2013这三年归母净利润均为正的公司
		stock_list.append(stock)
		profit_down_degree.append(qq[2]/(qq[0]+qq[1]))





w.start()
pp = []
for i in range(2011,2016):
    td = w.wss("600546.SH", "np_belongto_parcomsh,tot_oper_rev,net_cash_flows_inv_act,cash_pay_acq_const_fiolta,cash_recp_sg_and_rs","rptDate=%s1231;rptType=1"%i).Data
    pp.append([x[0] for x in td])

date_list = []
for i in range(5):
	date_list.append(dt.datetime(2011+i,1,1))

indicator_list = ['归母净利润','营业总收入','投资活动净现金流','构建固定资产无形资产和其他长期资产支付的现金','销售商品提供劳务收到的现金']

df1 = pd.DataFrame(pp,columns=indicator_list,index=date_list)

fig = figure()
ax = fig.add_subplot(111)
ax.scatter(date_list,list(df1[0]))

years = mdates.YearLocator()
ax.xaxis.set_major_locator(years)#设置x轴间隔为年

fmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_formatter(fmt)#设置x轴刻度格式

fig.autofmt_xdate()
draw()
