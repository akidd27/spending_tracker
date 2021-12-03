from models import merchant
from models.merchant import Merchant
from models.tag import Tag

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

merchant_1 = Merchant('BHS', False)
merchant_repository.save(merchant_1)