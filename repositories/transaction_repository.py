from db.run_sql import run_sql

from models.transaction import Transaction
from models.merchant import Merchant
from models.tag import Tag

# def __init__(self, merchant, tag, amount, date, time, id=None):

#create
def save(transaction):
    #sql query and values
    sql = "INSERT INTO transactions (merchant_id, tag_id, amount, transaction_date, transaction_time) VALUES (%s, %s, %s, %s, %s) RETURNING id"
    values = [transaction.merchant.id, transaction.tag.id, transaction.amount, transaction.date, transaction.time]

    #save transaction to db, get id and save it to Transaction object
    results = run_sql(sql, values)
    transaction.id = results[0]['id']
    return transaction


