import requests as r
import json
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt

def get_stock_data(start_year, start_month, end_year, end_month, stock_code):
    start_date = str(date(start_year, start_month, 1))
    end_date = str(date(end_year, end_month, 1))
    month_list = pd.date_range(start_date, end_date, freq='MS').strftime("%Y%m%d").tolist()
    
    df = pd.DataFrame()
    for month in month_list:
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+ month + "&stockNo=" + str(stock_code)
        res = r.get(url)
        stock_json = res.json()
        stock_df = pd.DataFrame.from_dict(stock_json['data'])
        df = df._append(stock_df, ignore_index = True)
    
    df.columns = ['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']
    return df

stock  = get_stock_data(start_year = 2024, start_month = 1, end_year = 2024, end_month = 7, stock_code = 2330)

#日期從字串(string)換成時間(datetime)，並將民國年換成西元年
for row in range(stock.shape[0]):
    date2 = stock.iloc[row,0].split('/')
    stock.iloc[row, 0] = datetime(int(date2[0]) + 1911, int(date2[1]), int(date2[2]))

#把"成交股數" "成交金額" "開盤價", "最高價", "最低價", "收盤價" "漲跌價差" "成交筆數"帶有逗號的字串(string)換成浮點數(float)
for col in [1, 2, 3, 4, 5, 6, 8]:
    for row in range(stock.shape[0]):
        stock.iloc[row, col] = float(stock.iloc[row,col].replace(',', ''))

# print(stock.head(10))

#將下載的個股資料另存成csv檔
#stock.to_csv("2330_202407.csv")

stock2 = stock[:21]
print(stock2)

fig = plt.figure(figsize = (10, 5),frameon=True)
plt.title('2330 202401 Stock Price')
#plt.subplot()
plt.plot(stock2['日期'], stock2['收盤價'])
plt.plot(stock2['日期'], stock2['開盤價'])
plt.legend(['Close', 'Open'])
plt.show()