#Program for Cardamom Price Alerter Telegram bot

import requests
from bs4 import BeautifulSoup  
import pandas as pd 
from datetime import date
import sys


Auctioneer_name = []
Number_of_lots = []
Total_quantity = []
Quantity_sold = []
Remaining_quantity = []
Max_Price = []
Avg_Price = []
number_of_auctioners = 0
token = "1806166019:AAHnBPMcXxXtm4sEdxNkFbHr6H8l7C50BgQ"
chat_id = "-568093680"                                                                        #"1815946443" Chat Id for Personal messagebox

def send_message(token, chat_id, message_text, average_price_message_text, max_price_message_text):
    telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, chat_id, message_text)
    message_sent_response = requests.get(telegram_url)
    status = message_sent_response.content.decode("utf8")
    print(status)

    telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, chat_id, average_price_message_text)
    message_sent_response = requests.get(telegram_url)
    status = message_sent_response.content.decode("utf8")
    print(status)

    telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, chat_id, max_price_message_text)
    message_sent_response = requests.get(telegram_url)
    status = message_sent_response.content.decode("utf8")
    print(status)


today = date.today()
today = today.strftime("%d-%b-%Y")
print(today)

url = "http://www.indianspices.com/marketing/price/domestic/daily-price-small.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html')                                                                         #Use 'lxml' when running on the local machine and 'html' when running on heroku 
table_data =  soup.find('table', width = "100%")
print(table_data)

headers = ["Sno", "Date of Auction", "Auctioneer", "No.of Lots", "Total Qty Arrived (Kgs)", "Qty Sold (Kgs)", "MaxPrice (Rs./Kg)", "Avg.Price (Rs./Kg)"]
df = pd.DataFrame(columns = headers)

for i in table_data.find_all('tr'):
    row_data = i.find_all('td')
    row = [tr.text.strip() for tr in row_data]
    length = len(df)
    df.loc[length] = row
print(df)

today_df = df.loc[df['Date of Auction'] == today]
number_of_auctioners = len(today_df.index)
print(today_df)

i = 0 
for i in range(number_of_auctioners):
    Auctioneer_name.append(today_df['Auctioneer'].iloc[i])
    Number_of_lots.append(today_df['No.of Lots'].iloc[i])
    Total_quantity.append(today_df['Total Qty Arrived (Kgs)'].iloc[i])
    Quantity_sold.append(today_df['Qty Sold (Kgs)'].iloc[i])
    Max_Price.append(today_df['MaxPrice (Rs./Kg)'].iloc[i])
    Avg_Price.append(today_df['Avg.Price (Rs./Kg)'].iloc[i])
    tot_qty = float(today_df['Total Qty Arrived (Kgs)'].iloc[i])
    sold_qty = float(today_df['Qty Sold (Kgs)'].iloc[i])
    remain_qty = tot_qty - sold_qty
    remain_qty = str(remain_qty)
    Remaining_quantity.append(remain_qty)

print(Auctioneer_name)
print(Number_of_lots)
print(Total_quantity)
print(Quantity_sold)
print(Remaining_quantity)
print(Max_Price)
print(Avg_Price)

message_text = ""
average_price_message_text = ""
i = 0
message_text = "Cardamom Price Details for {}: \n-----------------------------------------------------\n".format(today)
average_price_message_text = "Average Price for {}: \n----------------------------------------------\n".format(today)
max_price_message_text = "Maximum Price for {}: \n-----------------------------------------------\n".format(today)

for i in range(number_of_auctioners):
    message_text = message_text + "\nAuctioneer: {}\nNumber of Lots: {}\nTotal Quantity Arrived: {}\nQuantity Sold: {}\nRemaining Quantity: {}\nMaximum Price: Rs. {}\nAverage Price: Rs. {}\n".format(Auctioneer_name[i], Number_of_lots[i], Total_quantity[i], Quantity_sold[i], Remaining_quantity[i], Max_Price[i], Avg_Price[i])

for price in Avg_Price:
    average_price_message_text = average_price_message_text + "Rs. {}\n".format(price)

for price in Max_Price:
    max_price_message_text = max_price_message_text + "Rs. {}\n".format(price)

print(message_text)
print(average_price_message_text)
print(max_price_message_text)

send_message(token, chat_id, message_text, average_price_message_text, max_price_message_text)

sys.exit()