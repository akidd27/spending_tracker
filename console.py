from models import merchant
from models import transaction
from models.transaction import Transaction
from models.merchant import Merchant
from models.tag import Tag

import datetime
from modules import logic_functions

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

transactions = transaction_repository.select_all()

filtered = logic_functions.filter_and_sort('all', 27, datetime.date(1990,1,1), datetime.date(2025,1,1), 'date_newest_first')

print(filtered)