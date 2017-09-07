#!/usr/bin/env python
# encoding: utf-8

# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import numpy as np
import pandas as pd

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 初始化待买股票池
    context.stock_pool=[]
    # 初始化卖空股票池
    context.short=[]
    # 初始化购买权重
    context.weight=[]
    # 初始化卖空股票权重
    context.short_weight=[]
    # 获取市场所有股票
    context.stock=index_components('399958.XSHE')
    # context.stock=all_instruments(type='CS').order_book_id
    scheduler.run_daily(stoploss)
    context.drawdown= 0.1 # 回撤限度 10%
    context.maxvalue=pd.DataFrame()

def stoploss(context,bar_dict):
    for stock in context.portfolio.positions:
        market_value=context.portfolio.positions[stock].market_value# 该股市场价值 单位（RMB）
        avg_price=context.portfolio.positions[stock].avg_price
        if stock in context.maxvalue:
            stockdic=context.maxvalue[stock]
            print(stock+'已卖出')
            maxvalue=stockdic[0]
            del context.maxvalue[stock]

            #currSP=context.initSPM*(1+math.floor((maxvalue/avg_price-1)/context.step)*context.increment) #阶梯止损算法 例： 该股市值增加10%， 止盈比例提高 5%

            temp=pd.DataFrame({str(stock):[max(maxvalue,market_value)]})
            context.maxvalue=pd.concat([context.maxvalue,temp], axis=1, join='inner') # 更新其盘中最高价值和先阶段比例。
            drawdown=1-market_value/max(maxvalue,market_value)

            print(str(stock)+'的成本为：' +str( avg_price) +', 最高价值为：'+str(maxvalue)+'现价值为：'+ str(market_value))
            print(str(stock) +'的现 回撤为: ' +str(drawdown*100)+ '%')
            #logger.info ( type(market_value))
            #logger.info(type(ontext.maxvalue[stock].values)))
            if drawdown>context.drawdown:# 现价低于 原价一定比例
                order_target_percent(stock,0)
                print(str(stock)+'回撤大于'+ str(context.drawdown*100)+ '%'+'  触发止损')
                del context.maxvalue[stock]

def createdic(context,bar_dict,stock):
    if stock not in context.maxvalue.columns:
        temp=pd.DataFrame({str(stock):[context.portfolio.positions[stock].avg_price]})
        context.maxvalue = pd.concat([context.maxvalue, temp], axis=1, join='inner')
    print(context.maxvalue)

# 在交易前计算所有股票alpha因子值，取最高的10组进行买入，这里也可以取最低的10组进行卖空操作
def before_trading(context):
    # 获取当前交易日日期
    date=str(context.now)[0:10]
    # 获取10个交易日前信息，根据选取因子所需计算的日期决定
    for i in range(1,10):
        date=get_previous_trading_date(date)
    # 获取股票历史数据
    pn_data=get_price(context.stock, start_date=date, end_date=None, frequency='1d', fields=None, adjust_type='pre', skip_suspended=False)
    # 实例化Alpha对象
    alpha=Alphas(pn_data)
    # 用户所选取的因子，返回所有股票的该因子值，这里选取001作为示范，用户可修改为其他自己感兴趣的因子
    alpha_use=alpha.alpha006()
    # 取得交易日前一天的因子值
    result=alpha_use.tail(1)
    # 将空值赋为0
    result[np.isnan(result)] = 0
    result=result.T
    # 获取上一交易日日期
    today=str(context.now)[0:10]
    yesterday=get_previous_trading_date(today)
    # 将前一天因子值排序后取出因子值最高的前10只股股票
    buy=result.sort(columns=yesterday,ascending=True)[-5:]
    # 将前一天因子值排序后取出因子值最低的前10只股股票
    short=result.sort(columns=yesterday,ascending=True)[0:10]
    context.short_weight=short.values/sum(buy.values)
    # 计算每只股票的权重，按照因子大小计算权重
    context.weight=buy.values/sum(buy.values)
    # 将选出的股票加入到待买股票池中
    context.stock_pool=buy.index
    # 将选出来的卖空股票加入带卖空股票池
    context.short=short.index

def handle_bar(context, bar_dict):
    # 获取权重的计数器
    i=0
    # 获取当前持有股票
    #hand_stock=context.portfolio.positions
    # 当前的现金，用于做空时使用，只做多时不考虑
    #cash=context.portfolio.cash
    # 当当前持有的股票不在待买股票池中，亦即因子值跌出前10，就清仓。
    # for stock in hand_stock:
    #     if stock not in context.stock_pool:
    #         order_target_percent(stock,0)
    # 买入待买股票池中的股票，买入权重为因子值大小
    for stock in context.stock_pool:
        weight=float(context.weight[i])
        # order_target_value(stock,weight*cash)
        order_target_percent(stock,weight)
        createdic(context,bar_dict,stock)
        i+=1
    # for stock in context.short:
    #     weight=float(context.short_weight[i])
    #     order_target_value(stock,-1*weight*cash)
    #     i+=1

