from flask import Flask, render_template, request, redirect
from flask import Blueprint

import datetime

from models.transaction import Transaction
from modules.logic_functions import *

import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

transactions_blueprint = Blueprint("transactions", __name__)

date_sort_newest_first = True

#show all transactions
@transactions_blueprint.route("/transactions")
def all_transactions():
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

#View individual transaction to edit or delete
@transactions_blueprint.route('/transactions/<id>')
def edit_transaction(id):
    transaction = transaction_repository.select(id)
    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()
    return render_template('transactions/edit.html', title=f"Transaction {transaction.id}", transaction=transaction, merchants=merchants, tags=tags)

#delete transaction
@transactions_blueprint.route('/transactions/<id>/delete', methods=['POST'])
def delete_transaction(id):
    transaction_repository.delete(id)
    return redirect('/transactions')

#update transaction from form data
@transactions_blueprint.route('/transactions/<id>/edit', methods=['POST'])
def update_transaction(id):
    transaction = transaction_repository.select(id)
    transaction.merchant = merchant_repository.select(request.form['merchant_id'])
    transaction.tag = tag_repository.select(request.form['tag_id'])
    transaction.amount = request.form['amount']
    transaction.date = request.form['date']
    transaction.time = request.form['time']
    transaction_repository.update(transaction)
    return redirect('/transactions')

#choose filter options
@transactions_blueprint.route('/transactions/filter')
def select_filters():
    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()

    #get transactions
    transactions = transaction_repository.select_all()
    transactions_sorted = sort_by_date(transactions)

    #get total of all transactions
    transactions_total = total_of_transactions(transactions)
    default_date = datetime.datetime.now().date()

    return render_template('transactions/filter.html', title="Select Filters", merchants=merchants, tags=tags, transactions_sorted=transactions_sorted, transactions_total=transactions_total)

#show filtered results
@transactions_blueprint.route('/transactions/filter', methods=['POST'])
def filtered_transactions():

    #convert date strings to date objects
    start_date = datetime.date.fromisoformat(request.form['start_date'])
    end_date = datetime.date.fromisoformat(request.form['end_date'])
    tag_id = int(request.form['tag_id'])
    merchant_id = int(request.form['merchant_id'])
    sort_by = int(request.form['sort_by'])

    transactions_sorted = filter_and_sort(merchant_id, tag_id, start_date, end_date, sort_by)

    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()

    transactions_total = total_of_transactions(transactions_sorted)

    return render_template('transactions/filter.html', title="Results", merchants=merchants, tags=tags, transactions_sorted=transactions_sorted, transactions_total=transactions_total)
