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