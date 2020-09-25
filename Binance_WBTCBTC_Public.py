import math
import time
from datetime import datetime
from binance.client import Client

client = Client(api_key = '', api_secret = '')

##_0_參數調整

WBTC_Bid_Depth_To_Ignore = 5 #買單深度閾值
WBTC_Ask_Depth_To_Ignore = 5 #賣單深度閾值
Highest_Bid_Price = 1.00009 #買單最高價格
Lowest_Ask_Price = 1.00399 #賣單最低價格
Refresh_Time = 116.5 #更新頻率(秒)

x = -2

while True :

    ##_1_清空所有訂單

    orders = client.get_open_orders(symbol='WBTCBTC')
    
    time.sleep(0.5)

    for i in range(0, len(orders), 1) :
        cancel = client.cancel_order(symbol = 'WBTCBTC', orderId = orders[i]['orderId'])
        time.sleep(0.1)
    
    ##_2_取得帳戶當前之BTC與WBTC餘額

    BTC = client.get_asset_balance(asset='BTC')
    BTC_Balance = float(BTC.get('free'))
        
    WBTC = client.get_asset_balance(asset='WBTC')
    WBTC_Balance = float(WBTC.get('free'))
    Available_WBTC_Balance_For_Ask = math.floor(WBTC_Balance*10000)/10000

    time.sleep(0.5)
    
    ##_3_計算市場買賣單深度並依條件掛單

    depth = client.get_order_book(symbol='WBTCBTC')
    all_bids = 0
    all_asks = 0

    time.sleep(0.5)

    if BTC_Balance >= 0.0001 :
        for i in range(0, len(depth['bids']), 1) :
            bid = float(depth['bids'][i][1])
            all_bids = all_bids + bid        
        
            if all_bids >= WBTC_Bid_Depth_To_Ignore :
                WBTC_Bid_Price = math.floor((float(depth['bids'][i][0]) + 0.00001)*100000)/100000
                                                
                if WBTC_Bid_Price <= Highest_Bid_Price :
                    print('Bid Price :')
                    print(WBTC_Bid_Price)
                    Available_WBTC_Balance_For_Bid = math.floor((BTC_Balance / WBTC_Bid_Price)*10000)/10000
                    order = client.order_limit_buy(
                        symbol = 'WBTCBTC',
                        quantity = Available_WBTC_Balance_For_Bid,
                        price = WBTC_Bid_Price)        
                    break
                else :
                    print('Bid Price :')
                    print(Highest_Bid_Price)
                    Available_WBTC_Balance_For_Bid = math.floor((BTC_Balance / Highest_Bid_Price)*10000)/10000
                    order = client.order_limit_buy(
                        symbol = 'WBTCBTC',
                        quantity = Available_WBTC_Balance_For_Bid,
                        price = Highest_Bid_Price)
                    break

    time.sleep(0.5)

    if Available_WBTC_Balance_For_Ask > 0 :
        for i in range(0, len(depth['asks']), 1) :
            ask = float(depth['asks'][i][1])
            all_asks = all_asks + ask
        
            if all_asks >= WBTC_Ask_Depth_To_Ignore :
                WBTC_Ask_Price = math.floor((float(depth['asks'][i][0]) - 0.00001)*100000)/100000
                
                if WBTC_Ask_Price >= Lowest_Ask_Price :
                    print('Ask Price :')
                    print(WBTC_Ask_Price)
                    order = client.order_limit_sell(
                        symbol = 'WBTCBTC',
                        quantity = Available_WBTC_Balance_For_Ask,
                        price = WBTC_Ask_Price) 
                    break
                else :
                    print('Ask Price :')
                    print(Lowest_Ask_Price)                
                    order = client.order_limit_sell(
                        symbol = 'WBTCBTC',
                        quantity = Available_WBTC_Balance_For_Ask,
                        price = Lowest_Ask_Price)
                    break

    time.sleep(1)

    ##_4_當前時間與掛單狀況

    orders = client.get_open_orders(symbol='WBTCBTC')

    if len(orders) >= 1 :
        if orders[0]['side'] == 'BUY' :
            print('Buy :')
            print(orders[0]['symbol'] + ' ' + orders[0]['price'] + ' ' + orders[0]['origQty'])

        if orders[0]['side'] == 'SELL' :
            print('Sell :')
            print(orders[0]['symbol'] + ' ' + orders[0]['price'] + ' ' + orders[0]['origQty'])

    if len(orders) >= 2 :
        if orders[1]['side'] == 'BUY' :
            print('Buy :')
            print(orders[1]['symbol'] + ' ' + orders[1]['price'] + ' ' + orders[1]['origQty'])

        if orders[1]['side'] == 'SELL' :
            print('Sell :')
            print(orders[1]['symbol'] + ' ' + orders[1]['price'] + ' ' + orders[1]['origQty'])

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    x = x + 2
    print('運行了', x, '分鐘', '\n')

    time.sleep(Refresh_Time)

