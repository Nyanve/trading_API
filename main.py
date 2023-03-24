from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector


def connect_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="currency_api"
    )

    mycursor = mydb.cursor()

    return mydb


app = Flask(__name__)
api = Api(app)

db = connect_db()
cursor = db.cursor()


class CurrencyName(Resource):
    def get(self, c_code):
        cursor.execute("SELECT name FROM currencies WHERE code = %s", (c_code,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "Currency not found"


class ExchangeRate(Resource):
    def get(self, c1, c2, amount):
        # # Parse arguments and convert amount to float
        # parser = reqparse.RequestParser()
        # parser.add_argument('c1', type=str, required=True)
        # parser.add_argument('c2', type=str, required=True)
        # parser.add_argument('amount', type=float, required=True)
        # args = parser.parse_args()



        # Calculate exchange rate
        cursor.execute("SELECT cur_to_EUR FROM conversion_rates WHERE currency_code = %s", (c1,))
        result1 = cursor.fetchone()
        print(result1)
        if not result1:
            return "Currency not found"
        cursor.execute("SELECT EUR_to_cur FROM conversion_rates WHERE currency_code = %s", (c2,))
        result2 = cursor.fetchone()
        print(result2)
        if not result2:
            return "Currency not found"

        rate1 = result1[0]
        rate2 = result2[0]
        print(rate1)
        print(rate2)
        eur_amount = amount * rate1
        print(eur_amount)
        result_amount = eur_amount * rate2
        print(result_amount)

        # Return result with 2 decimal places and the currency code
        return str(round(result_amount, 2)) + " " + c2




api.add_resource(CurrencyName, "/name/<string:c_code>")
api.add_resource(ExchangeRate, "/exchange_rate/<string:c1>/<string:c2>/<int:amount>")


if __name__ == '__main__':
    app.run(debug=True)
