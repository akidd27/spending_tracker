from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository

merchants_blueprint = Blueprint("merchants", __name__)

#show all active merchants
@merchants_blueprint.route("/merchants")
def merchants():
    active_merchants = merchant_repository.select_active()
    return render_template("merchants/index.html", title='My Merchants', active_merchants=active_merchants)

#form to create new merchant
@merchants_blueprint.route("/merchants/new")
def new_merchant():
    return render_template("/merchants/new.html", title="New Merchant")

#add new merchant and return to /merchants
@merchants_blueprint.route("/merchants", methods=['POST'])
def add_merchant():
    name = request.form['name']
    if not merchant_repository.check_by_name(name):
        merchant = Merchant(name)
        merchant_repository.save(merchant)
        return redirect('/merchants')
    else:
        return render_template('/merchants/already_exists.html', title="Error", name=name)

#form to edit/delete/deactivate merchant
@merchants_blueprint.route("/merchants/<id>")
def edit_merchant(id):
    merchant = merchant_repository.select(id)
    return render_template('/merchants/edit.html', title=merchant.name, merchant=merchant)

#update merchant from form data
@merchants_blueprint.route("/merchants/<id>", methods=['POST'])
def update_merchant(id):
    name = request.form['name']
    merchant = Merchant(name, True, id)
    merchant_repository.update(merchant)
    return redirect('/merchants')

#delete merchant
@merchants_blueprint.route('/merchants/<id>/delete', methods=['POST'])
def delete_merchant(id):
    merchant_repository.delete(id)
    return redirect('/merchants')

#deactivate merchant
@merchants_blueprint.route('/merchants/<id>/deactivate', methods=['POST'])
def deactivate_merchant(id):
    merchant = merchant_repository.select(id)
    merchant.active = False
    merchant_repository.update(merchant)
    return redirect('/merchants')

#show deactivated merchants
@merchants_blueprint.route('/merchants/inactive')
def inactive_merchants():
    inactive_merchants = merchant_repository.select_active(False)
    return render_template('/merchants/inactive.html', title='Inactive Merchants', inactive_merchants=inactive_merchants)

#activate merchant
@merchants_blueprint.route('/merchants/<id>/activate', methods=['POST'])
def activate_merchant(id):
    merchant = merchant_repository.select(id)
    merchant.active = True
    merchant_repository.update(merchant)
    return redirect('/merchants/inactive')