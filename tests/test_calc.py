import pytest
from app.calculation import add,subtract,multiply,divide,BankAccount,Insufficient_funds


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(500)


@pytest.mark.parametrize("num1,num2,expected",[
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1,num2,expected):
    print("Testing add Function")
    assert add(num1,num2) == expected
    
    
def test_multiply():
    print("Testing Multiply Function")
    assert multiply(2,5) == 10
    
    
def test_divide():
    print("Testing divide Function")
    assert divide(25,5) == 5
 
def test_subtract():
    print("Testing subtract Function")
    assert subtract(34,3) == 31
    

def test_bank_set_initial_amount(bank_account):
    bank_account.deposit(40)
    assert bank_account.balance==540
    
 
def test_bank_set_default_amount(zero_bank_account):
    bank_account=BankAccount()
    assert bank_account.balance==0
    
    

def test_bank_withdraw_amount(bank_account):
    bank_account.withdraw(40)
    assert bank_account.balance==460
    
    

def test_bank_deposit_amount(bank_account):
    bank_account.deposit(40)
    assert bank_account.balance==540
    

def test_bank_interest_amount(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance==550
    

@pytest.mark.parametrize("deposit,withdraw,balance",[
    (200,100,100),
    (100,1,99),
    (12,4,8)
])
def test_bank_transaction(zero_bank_account,deposit,withdraw,balance):
    print("doing some transactions")
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance==balance
    
    
    
def test_insufficient_funds(bank_account):
    with pytest.raises(Insufficient_funds):
        bank_account.withdraw(2000)
    
