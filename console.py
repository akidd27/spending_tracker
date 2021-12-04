from models.transaction import Transaction
from models.merchant import Merchant
from models.tag import Tag

import datetime

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

tag_1 = Tag('Retail')
tag_repository.save(tag_1)

merchant_1 = Merchant('Amazon')
merchant_repository.save(merchant_1)

time_1 = datetime.time(14, 30, 00)
date_1 = datetime.date(2021, 12, 4)

transaction_1 = Transaction(merchant_1, tag_1, 50, date_1, time_1)

transaction_repository.save(transaction_1)