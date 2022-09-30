import account
import person
import transaction
import csv

LIST_ALL = 1
LIST_ACCOUNT = 2
QUIT = 3

all_accounts_objs = [] # list used to store instances of account objects for OOP version
csv_transactions = []
dict_accounts = {} # dict used to store account name and balance only

def read_file():
    # FILE NAMES = short.csv or Transactions2014.csv
    with open("Transactions2014.csv", "rt") as csv_file:
        csv_rows = csv.reader(csv_file)
        next(csv_rows, None)  # skip the first Heading row
        get_accounts_and_transactions(csv_rows)

def get_accounts_and_transactions(csv_rows):
    for row in csv_rows:
        date = row[0]
        from_person = row[1]
        to_person = row[2]
        details = row[3]
        pence_amount_as_float = float(row[4]) * 100
        pence_amount = int(pence_amount_as_float)

        # using dict of accounts (not list), add new user accounts if they dont already exist - do OOP version later with Account obj nested inside value of dictionary with name as key
        if from_person not in dict_accounts:
            new_account = account.Account(from_person)
            # currently still need list of Account objs so menu option 2 works
            all_accounts_objs.append(new_account)
            # For Now - set the balance to 0 instead of using the Account obj itself
            dict_accounts[from_person] = 0
            # Later - make OOP version work
            # dict_accounts[from_person] = new_account

        current_entry = transaction.Transaction(date, from_person, to_person, details, pence_amount)
        csv_transactions.append(current_entry)
        # OOP Version - now add the trans to the users account history, currently only based on from_person - need to be able to get history properties later
        new_account.history.append(current_entry)
    # end of for rows

# List All option should output the names of each person, and the total amount they owe, or are owed. First process the transactions to calculate the balance for each account
def process_account_balances():
    for i in range(len(csv_transactions)):
        from_name = csv_transactions[i].from_person
        to_name = csv_transactions[i].to_person
        pence_amount = csv_transactions[i].amount
        # todo later - use accounts dict with name as key & account obj as value, then do matching

        # todo - refactor these as one function, passing in account_name, amount and credit/debit option
        if from_name in dict_accounts:
            current_balance = dict_accounts.get(from_name)
            new_balance = int(current_balance) - pence_amount
            dict_accounts.update({from_name: new_balance})
            # nested second IF as these should be atomic transactions ie either both succeed or both fail
            if to_name in dict_accounts:
                current_balance = dict_accounts.get(to_name)
                new_balance = int(current_balance) + pence_amount
                dict_accounts.update({to_name: new_balance})
    # end of FOR list of transactions

def print_dict(dictionary):
    for i in range(len(dictionary)):
        print(dictionary)
        # how to print or access an obj inside a dictionary ?
        # print(dict_accounts[i].printme()) # throws KeyError: 0

# Print the dictionary of account balances, showing key of name and value of balance as currency
def print_account_balances():
    print("\nShowing all Accounts and Balances")
    for key in dict_accounts:
        pretty_currency = format_pence_as_currency(dict_accounts[key])
        print(key, ': ', pretty_currency)

# now currencies/balance are all in int of number of pence, needs formatting as currency when printing
# todo move minus sign before £ sign
def format_pence_as_currency(pence) -> str:
    pence_float = float(pence / 100)
    currency_str = "£{:,.2f}".format(pence_float)
    return currency_str

def print_list(some_list):
    for i in range(len(some_list)):
        print(some_list[i].printme())

def print_menu():
    print("\nMenu Options")
    print(" 1 - List All ")
    print(" 2 - List Account")
    print(" 3 - Quit")

def get_menu_option():
    option = 0
    while option <1 or option > 3:
        option = int(input("Enter your choice: "))
    return option

# show a list of customer accounts that user can choose to view transactions for
def get_cust_account():
    print("\nCustomer Accounts:")
    for i in range(len(all_accounts_objs)):
        print(f"{i}: {all_accounts_objs[i].account_name}")
    option = int(input("Enter a number to view transactions for an account: "))
    cust = all_accounts_objs[option].account_name
    return cust

# List [Account] option should also print a list of every transaction, with the date and narrative, for that account with that name.
def list_account(account_name):
    print(f"\nTransactions for Account Name: {account_name}")
    for i in range(len(csv_transactions)):
        if csv_transactions[i].from_person == account_name or csv_transactions[i].to_person  == account_name:
            print(csv_transactions[i].printme())
            # todo fix bug of `None` being printed after each transaction entry

def main():
    read_file()
    option = 0
    while option != QUIT:
        print_menu()
        option = get_menu_option()
        if option == LIST_ALL:
            process_account_balances()
            print_account_balances()
        elif option == LIST_ACCOUNT:
            cust = get_cust_account()
            list_account(cust)
    print('Quitting...')

if __name__ == '__main__':
    main()
