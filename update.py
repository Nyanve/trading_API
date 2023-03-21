import mysql.connector
import requests
from datetime import datetime

# establish connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="currency_api"
)

mycursor = mydb.cursor()

def create_database_and_tables():
    # create database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS currency_api")

    # switch to currency_api database
    mycursor.execute("USE currency_api")

    # create table for currency data
    mycursor.execute("CREATE TABLE IF NOT EXISTS currencies (id INT AUTO_INCREMENT PRIMARY KEY, currency_code VARCHAR(5), currency_name VARCHAR(50), currency_icon VARCHAR(255))")

    # create table for conversion rates
    mycursor.execute("CREATE TABLE IF NOT EXISTS conversion_rates (id INT AUTO_INCREMENT PRIMARY KEY, currency_code VARCHAR(5), cur_to_EUR FLOAT, EUR_to_cur FLOAT, updated_date DATE)")

def update_currencies():
    currencies_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json"
    currencies_data = requests.get(currencies_url).json()

    currencies_query = "INSERT INTO currencies (id, code, name, icon) VALUES (%s, %s, %s, %s)"
    for currency_code, currency_name in currencies_data.items():
        mycursor.execute(currencies_query, (None, currency_code, currency_name, None))

    mydb.commit()

def update_conversion_rates():
    # get the code, eur to cur and date
    eur_to_cur = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur.json"
    converison1 = requests.get(eur_to_cur).json()['eur']
    curent_date = requests.get(eur_to_cur).json()['date']

    converison_query = "INSERT INTO conversion_rates (id, currency_code, cur_to_EUR, EUR_to_cur, updated_date) VALUES (%s, %s, %s, %s, %s)"
    for currency_code, EUR_to_cur in converison1.items():
        mycursor.execute(converison_query, (None, currency_code, None, EUR_to_cur, curent_date))

    # cur to eur and date
    #this section will fetch currencies from the database and send a request for each currency to api to get the conversion rate. use this url to get the conversion rate: https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{}/eur.json .format(cur) where "cur" is the currency code.
    mycursor.execute("SELECT code FROM currencies")
    currencies = mycursor.fetchall()
    for currency in currencies:
        cur_to_eur = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{}/eur.json".format(currency[0])
        cur_to_EUR = requests.get(cur_to_eur).json()['eur']
        curent_date = requests.get(cur_to_eur).json()['date']

        converison_query = "INSERT INTO conversion_rates (id, currency_code, cur_to_EUR, EUR_to_cur, updated_date) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(converison_query, (None, currency_code, cur_to_EUR, None, curent_date))

    mydb.commit()


# create database and tables
create_database_and_tables()

# update the currencies
update_currencies()

# update the conversion rates
update_conversion_rates()

# close connection
mycursor.close()
mydb.close()