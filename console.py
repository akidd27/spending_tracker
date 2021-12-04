from models import merchant
from models.transaction import Transaction
from models.merchant import Merchant
from models.tag import Tag

import datetime

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

print(transaction_repository.select(10).merchant.id)