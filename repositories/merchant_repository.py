from db.run_sql import run_sql
from models.merchant import Merchant

#similar to tag repository

#create
def save(merchant):
    #sql query and values
    sql = "INSERT INTO merchants (name, active) VALUES (%s, %s) RETURNING id"
    values = [merchant.name, merchant.active]

    #save merchant to db, get id and save it to Merchant object
    results = run_sql(sql, values)
    merchant.id = results[0]['id']
    return merchant

#read all
def select_all():
    #create empty merchants list
    merchants = []

    #sql query
    sql = "SELECT * FROM merchants"
    results = run_sql(sql)

    #create merchant object for each row in results and append to list
    for row in results:
        merchant = Merchant(row['name'], row['active'], row['id'])
        merchants.append(merchant)
    return merchants

#read by id
def select(id):
    merchant = None

    #sql query and id value
    sql = "SELECT * FROM merchants WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    #if exists, return merchant object from query result
    if result is not None:
        merchant = Merchant(result['name'], result['active'], result['id'])
    return merchant

#read active/inactive merchants
def select_active(active=True):
    #create empty merchants list
    active_merchants = []

    #sql query and values
    sql = "SELECT * FROM merchants WHERE active = %s"
    values = [active]
    results = run_sql(sql, values)

    #create Merchant object for each result row and append to list
    for row in results:
        merchant = Merchant(row['name'], row['active'], row['id'])
        active_merchants.append(merchant)
    
    return active_merchants

#check if merchant already exists with given name
#returns True if already exists else False
def check_by_name(name):
    sql = "SELECT 1 FROM merchants WHERE name = %s"
    values = [name]
    result = run_sql(sql, values)
    if result:
        return True
    else:
        return False

#update merchant
def update(merchant):
    #sql query and values
    sql = "UPDATE merchants SET (name, active) = (%s, %s) WHERE id = %s"
    values = [merchant.name, merchant.active, merchant.id]
    run_sql(sql, values)

#delete all
def delete_all():
    sql = "DELETE  FROM merchants"
    run_sql(sql)

#delete by id
def delete(id):
    sql = "DELETE FROM merchants WHERE id = %s"
    values = [id]
    run_sql(sql, values)