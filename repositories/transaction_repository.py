from db.run_sql import run_sql
from models import transaction

from models.transaction import Transaction
from models.merchant import Merchant
from models.tag import Tag

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

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

#read all
def select_all():
    #create empty list of transactions
    transactions = []

    sql = "SELECT * FROM transactions"
    results = run_sql(sql)
    #create Transaction object for each row in results and append to list
    for row in results:
        #create Merchant and Tag objects from row data
        merchant = merchant_repository.select(row['merchant_id'])
        tag = tag_repository.select(row['tag_id'])
        transaction = Transaction(merchant, tag, row['amount'], row['transaction_date'], row['transaction_time'], row['id'])
        transactions.append(transaction)
    return transactions


