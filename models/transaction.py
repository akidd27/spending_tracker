class Transaction:

    def __init__(self, merchant, tag, amount, date, time, id=None):
        self.merchant = merchant
        self.tag = tag
        self.amount = amount
        self.date = date
        self.time = time
        self.id = id