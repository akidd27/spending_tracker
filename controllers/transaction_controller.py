from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.transaction import Transaction
from models.tag import Tag
from models.merchant import Merchant

import repositories.transaction_repository as transaction__repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

transactions_blueprint = Blueprint("transactions", __name__)

#show all transactions
@transactions_blueprint.route("/transactions")
def transactions():
    transactions = transaction__repository.select_all()
    return render_template("transactions/index.html", title='My Transactions', transactions=transactions)

#form to create new transaction
@transactions_blueprint.route("/transactions/new")
def new_transaction():
    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()
    return render_template("/transactions/new.html", title="New Transaction", tags=tags, merchants=merchants)

#add new transaction and return to /transactions
@transactions_blueprint.route("/transactions", methods=['POST'])
def add_transaction():
    merchant = merchant_repository.select(request.form['merchant_id'])
    tag = tag_repository.select(request.form['tag_id'])
    transaction = Transaction(merchant, tag, request.form['amount'], request.form['date'], request.form['time'])
    transaction__repository.save(transaction)
    return redirect('/transactions')
