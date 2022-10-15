#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def heuristica1treino(x0, x1, x2, x3, x4, ticker):
    # x e a variavel de controle
    # x[0]: preco: categorico {'open', 'close', 'low', 'high'}
    # x[1]: periodo da exponencial r√°pida int
    # x[2]: periodo da exponencial lenta int
    # x[3]: limiar de compra float
    # x[4]: limiar de venda float
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = ticker,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        start = "2010-01-01",
        end = "2010-12-31",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = '1d',

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = False,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

    data = data.dropna()

    if x0 == 'open':
        data['Price'] = data['Open']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif x0 == 'close':
        data['Price'] = data['Close']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif x0 == 'low':
        data['Price'] = data['Low']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    else:
        data['Price'] = data['High']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)

    # x[1] < x[2]
    if(x1 > x2):
      aux = x2
      x2 = x1
      x1 = aux
      
    tempo_curto = x1
    tempo_longo = x2

    data['EMA_curta'] = ta.EMA(data['Price'], timeperiod=tempo_curto)
    ema_curta = data['EMA_curta'].to_numpy()
    data['EMA_longa'] = ta.EMA(data['Price'], timeperiod=tempo_longo)
    ema_longa = data['EMA_longa'].to_numpy()
    
    #print(data)

    delta_c = x3
    delta_v = x4
    
    vacumulado = 0
    va_reservado = 0
    comprado = False

    t_compra = []
    t_venda = []
        
    
    datas = data.index
    
    for d in datas:
        #print(d.to_numpy())
        if data.loc[d]['EMA_curta'] > data.loc[d]['EMA_longa'] + delta_c and not comprado:
            #print('{} Compra: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra.append(d)
            comprado = True
            va_reservado = 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_curta'] < data.loc[d]['EMA_longa'] - delta_v and comprado:
            #print('{} Venda: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda.append(d)
            comprado = False
            vacumulado += 100*data.loc[d]['Price'] - va_reservado

    #print('Valor acumulado: R$ {:.2f}'.format(vacumulado))
    
    # Inverter o sinal do valor acumulado para a maximizaÁ„o no Irace
    return (-1*vacumulado)


# In[7]:


#heuristica1treino('close', 3, 6, 0.1, 0.1, 'aapl')


# In[14]:


def heuristica2treino(x, ticker):
    # x e a variavel de controle
    # x[0]: preco: categorico {'open', 'close', 'low', 'high'}
    # x[1]: periodo da exponencial r√°pida int
    # x[2]: periodo da exponencial m√©dia int
    # x[3]: periodo da exponencial lenta int
    # x[4]: limiar de compra c1_2 float
    # x[5]: limiar de venda v1_2 float
    # x[6]: limiar de compra c1_3 float
    # x[7]: limiar de venda v1_3 float
    # x[8]: limiar de compra c2_3 float
    # x[9]: limiar de venda v2_3 float
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = ticker,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        start = "2010-01-01",
        end = "2010-12-31",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = '1d',

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = False,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

    data = data.dropna()

    if x[0] == 'open':
        data['Price'] = data['Open']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif x[0] == 'close':
        data['Price'] = data['Close']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif x[0] == 'low':
        data['Price'] = data['Low']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    else:
        data['Price'] = data['High']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)

    # x[1] < x[2] < x[3]
    tempo_curto = x[1]
    tempo_medio = x[2]
    tempo_longo = x[3]

    data['EMA_curta'] = ta.EMA(data['Price'], timeperiod=tempo_curto)
    ema_curta = data['EMA_curta'].to_numpy()
    data['EMA_media'] = ta.EMA(data['Price'], timeperiod=tempo_medio)
    ema_media = data['EMA_media'].to_numpy()
    data['EMA_longa'] = ta.EMA(data['Price'], timeperiod=tempo_longo)
    ema_longa = data['EMA_longa'].to_numpy()
    
    #print(data)

    delta_c1_2 = x[4]
    delta_v1_2 = x[5]
    delta_c1_3 = x[6]
    delta_v1_3 = x[7]
    delta_c2_3 = x[8]
    delta_v2_3 = x[9]
    vacumulado1_2 = 0
    vacumulado1_3 = 0
    vacumulado2_3 = 0

    comprado1_2 = False
    comprado1_3 = False
    comprado2_3 = False

    t_compra1_2 = []
    t_venda1_2 = []
    t_compra1_3 = []
    t_venda1_3 = []
    t_compra2_3 = []
    t_venda2_3 = []
    #falta configurar compra inicial

    datas = data.index
    
    for d in datas:
        #print(d.to_numpy())
        if data.loc[d]['EMA_curta'] > data.loc[d]['EMA_media'] + delta_c1_2 and not comprado1_2:
            #print('{} Compra 1_2: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra1_2.append(d)
            comprado1_2 = True
            vacumulado1_2 -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_curta'] < data.loc[d]['EMA_media'] - delta_v1_2 and comprado1_2:
            #print('{} Venda 1_2: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda1_2.append(d)
            comprado1_2 = False
            vacumulado1_2 += 100*data.loc[d]['Price']
            
        if data.loc[d]['EMA_curta'] > data.loc[d]['EMA_longa'] + delta_c1_3 and not comprado1_3:
            #print('{} Compra 1_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra1_3.append(d)
            comprado1_3 = True
            vacumulado1_3 -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_curta'] < data.loc[d]['EMA_longa'] - delta_v1_3 and comprado1_3:
            #print('{} Venda 1_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda1_3.append(d)
            comprado1_3 = False
            vacumulado1_3 += 100*data.loc[d]['Price']
            
        if data.loc[d]['EMA_media'] > data.loc[d]['EMA_longa'] + delta_c2_3 and not comprado2_3:
            #print('{} Compra 2_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra2_3.append(d)
            comprado2_3 = True
            vacumulado2_3 -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_media'] < data.loc[d]['EMA_longa'] - delta_v2_3 and comprado2_3:
            #print('{} Venda 2_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda2_3.append(d)
            comprado2_3 = False
            vacumulado2_3 += 100*data.loc[d]['Price']
    
    vacumulado = vacumulado1_2 + vacumulado1_3 + vacumulado2_3
    #print('Valor acumulado 1_2: R$ {:.2f}'.format(vacumulado1_2))
    #print('Valor acumulado 1_3: R$ {:.2f}'.format(vacumulado1_3))
    #print('Valor acumulado 2_3: R$ {:.2f}'.format(vacumulado2_3))
    print('Valor acumulado total: R$ {:.2f}'.format(vacumulado))
    return vacumulado
   


# In[15]:


#heuristica2treino(['close', 3, 6, 9, 0.1, 0.1 , 0.1, 0.1, 0.1, 0.1], 'aapl')


# In[ ]:




