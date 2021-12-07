import repositories.transaction_repository as transaction_repository
import datetime

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

#filter list by tag
def filter_by_tag(transactions, tag_id):
    if tag_id == 0:
        #0 signifies select all
        return transactions
    else:
        tag_id = int(tag_id)
        filtered_transactions = []
        for transaction in transactions:
            if transaction.tag.id == tag_id:
                filtered_transactions.append(transaction)
        return filtered_transactions

#filter list by date range
def filter_by_date_range(transactions, start_date, end_date):
    if start_date == "all" and end_date == "all":
        return transactions
    else:
        filtered_transactions = []
        for transaction in transactions:
            if start_date <= transaction.date <= end_date:
                filtered_transactions.append(transaction)
        return filtered_transactions


#get transactions, then filter and sort
def filter_and_sort(merchant_id, tag_id, start_date, end_date, sort_by):
    #get transactions by merchant
    if merchant_id == 0:
        #0 signifies select all
        transactions_by_merchant = transaction_repository.select_all()
    else:
        transactions_by_merchant = transaction_repository.select_by_merchant(merchant_id)
    
    #filter transactions_by_merchant by tag
    transactions_by_merchant_tag = filter_by_tag(transactions_by_merchant, tag_id)

    #filter transactions_by_merchant_tag by date range
    transactions_by_merchant_tag_date = filter_by_date_range(transactions_by_merchant_tag, start_date, end_date)

    #sort
    if sort_by == 0:
        #by date newest first
        filtered_transactions = sort_by_date(transactions_by_merchant_tag_date)
    elif sort_by == 1:
        #by date oldest first
        filtered_transactions = sort_by_date(transactions_by_merchant_tag_date, False)
    elif sort_by == 2:
        #by amount high to low
        filtered_transactions = sort_by_amount(transactions_by_merchant_tag_date)
    elif sort_by == 3:
        #by amount low to high
        filtered_transactions = sort_by_amount(transactions_by_merchant_tag_date), False
    return filtered_transactions