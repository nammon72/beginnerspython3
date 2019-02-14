from abc import ABCMeta
from timeit import default_timer

def timer(func):
    def inner(self, value):
        print('calling ', func.__name__, 'on', self, 'with', value)
        start = default_timer()
        func(self, value)
        end = default_timer()
        print('returned from ', func.__name__, 'it took', end - start, 'seconds')

    return inner

class Account(metaclass=ABCMeta):
    """" A class used to represent a type of account """

    instance_count = 0

    @classmethod
    def increment_instance_count(cls):
        print('Creating new Account')
        cls.instance_count += 1

    def __init__(self, account_number, account_holder, opening_balance, account_type):
        Account.increment_instance_count()
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = opening_balance
        self.type = account_type

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, *args):
        print('__exit__:', args)
        return True

    # Method called if attribute is unknown
    def __getattr__(self, attribute):
        print('__getattr__: unknown attribute accessed - ', attribute)
        return -1

    @timer
    def deposit(self, amount):
        self._balance += amount

    @timer
    def withdraw(self, amount):
        self._balance -= amount

    @property
    def balance(self):
        """ Provides the current balance """
        return self._balance

    def __str__(self):
        return 'Account[' + self.account_number +'] - ' + \
               self.account_holder + ', ' + self.type + ' account = ' + str(self.balance)


class BalanceError(Exception):
    """ Valid Ages must be between 0 and 120 """

    def __init__(self, account):
        self.account = account


class CurrentAccount(Account):

    def __init__(self, account_number, account_holder, opening_balance, overdraft_limit):
        super().__init__(account_number, account_holder, opening_balance, 'current')
        self.overdraft_limit = -overdraft_limit

    @timer
    def withdraw(self, amount):
        if self.balance - amount < self.overdraft_limit:
            print('Withdrawal would exceed your overdraft limit')
        else:
            self._balance -= amount

    def __str__(self):
        return super().__str__() + 'overdraft limit: ' + str(self.overdraft_limit)


class DepositAccount(Account):

    def __init__(self, account_number, account_holder, opening_balance, interest_rate):
        super().__init__(account_number, account_holder, opening_balance, 'deposit')
        self.interest_rate = interest_rate

    def __str__(self):
        return super().__str__() + 'interest rate: ' + str(self.interest_rate)


class InvestmentAccount(Account):
    def __init__(self, account_number, account_holder, opening_balance, investment_type):
        super().__init__(account_number, account_holder, opening_balance, 'investment')
        self.investment_type = investment_type

    def __str__(self):
        return super().__str__() + ', type: ' + self.type
