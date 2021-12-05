from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.transaction import Transaction

import repositories.transaction_repository as transaction__repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

transactions_blueprint = Blueprint("transactions", __name__)

#return sum of amounts in given list of transactions
def total_of_transactions(transactions):
    transactions_total = 0
    for transaction in transactions:
        transactions_total += transaction.amount
    return transactions_total

#takes transaction object and returns date and time as tuple
def date_time_tuple(transaction):
    return (transaction.date, transaction.time)

#show all transactions
@transactions_blueprint.route("/transactions")
def transactions():
    #get transactions
    transactions = transaction__repository.select_all()

    #get total of all transactions
    transactions_total = total_of_transactions(transactions)

    return render_template("transactions/index.html", title='My Transactions', transactions=transactions, transactions_total=transactions_total)

#form to create new transaction
@transactions_blueprint.route("/transactions/new")
def new_transaction():
    merchants = merchant_repository.select_active()
    tags = tag_repository.select_active()
    return render_template("/transactions/new.html", title="New Transaction", tags=tags, merchants=merchants)

#add new transaction and return to /transactions
@transactions_blueprint.route("/transactions", methods=['POST'])
def add_transaction():
    merchant = merchant_repository.select(request.form['merchant_id'])
    tag = tag_repository.select(request.form['tag_id'])
    transaction = Transaction(merchant, tag, request.form['amount'], request.form['date'], request.form['time'])
    transaction__repository.save(transaction)
    return redirect('/transactions')

#delete?
#delete/clear all? with "are you sure?"
#Filters: by tag, merchant, date range, sort by date, sort by amount
#min/max for date/time inputs?