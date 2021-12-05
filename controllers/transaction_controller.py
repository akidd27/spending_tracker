from flask import Flask, render_template, request, redirect
from flask import Blueprint

import datetime
from time import strftime

from models.transaction import Transaction

import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

transactions_blueprint = Blueprint("transactions", __name__)

date_sort_newest_first = True

#return sum of amounts in given list of transactions
def total_of_transactions(transactions):
    transactions_total = 0
    for transaction in transactions:
        transactions_total += transaction.amount
    return transactions_total

#takes transaction object and returns date and time as tuple
def date_time_tuple(transaction):
    return (transaction.date, transaction.time)

#sort transactions by date
def sort_by_date(transactions, newest_first=True):
    return sorted(transactions, key=date_time_tuple, reverse=newest_first)

#sort transactions by amount
def sort_by_amount(transactions, highest_first=True):
    return sorted(transactions, key= lambda h: h.amount, reverse=highest_first)

#show all transactions
@transactions_blueprint.route("/transactions")
def transactions():
    #get transactions
    transactions = transaction_repository.select_all()
    transactions_sorted = sort_by_date(transactions)

    #get total of all transactions
    transactions_total = total_of_transactions(transactions)

    return render_template("transactions/index.html", title='My Transactions', transactions_sorted=transactions_sorted, transactions_total=transactions_total, date_sort_newest_first=True, amount_sort_highest_first=True)

#form to create new transaction
@transactions_blueprint.route("/transactions/new")
def new_transaction():
    merchants = merchant_repository.select_active()
    tags = tag_repository.select_active()
    default_date = datetime.datetime.now().date()
    return render_template("/transactions/new.html", title="New Transaction", tags=tags, merchants=merchants, default_date=default_date)

#add new transaction and return to /transactions
@transactions_blueprint.route("/transactions", methods=['POST'])
def add_transaction():
    merchant = merchant_repository.select(request.form['merchant_id'])
    tag = tag_repository.select(request.form['tag_id'])
    transaction = Transaction(merchant, tag, request.form['amount'], request.form['date'], request.form['time'])
    transaction_repository.save(transaction)
    return redirect('/transactions')

#sort newest or oldest first
@transactions_blueprint.route('/transactions/sort', methods=['POST'])
def sort_transactions():

    #get transactions and total amount
    transactions = transaction_repository.select_all()
    transactions_total = total_of_transactions(transactions)

    if request.form['sort_by'] == 'date':
        #sort newest/oldest first based on user choice
        date_sort_newest_first = bool(int(request.form['date_sort_newest_first']))
        transactions_sorted = sort_by_date(transactions, date_sort_newest_first)
        amount_sort_highest_first = True

        
    elif request.form['sort_by'] == 'amount':
        #sort high-low or low-high based on user choice
        amount_sort_highest_first = bool(int(request.form['amount_sort_highest_first']))
        transactions_sorted = sort_by_amount(transactions, amount_sort_highest_first)
        date_sort_newest_first = True

    return render_template("transactions/index.html", title='My Transactions', transactions_sorted=transactions_sorted, transactions_total=transactions_total, date_sort_newest_first=date_sort_newest_first, amount_sort_highest_first=amount_sort_highest_first)
