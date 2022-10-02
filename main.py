import account
import transaction
import csv

csv_transactions = []
dict_accounts = {} # dict used to store account name and balance only
# todo - could add more type hinting
def read_file():
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

        if from_person not in dict_accounts:
            # set the balance to 0 for now (instead of using the Account obj itself)
            dict_accounts[from_person] = 0
            # todo later OOP version - use accounts dict with name as key & Account obj as value, then try matching

        current_entry = transaction.Transaction(date, from_person, to_person, details, pence_amount)
        csv_transactions.append(current_entry)
    # end of for rows

# List All option should output the names of each person, and the total amount they owe, or are owed. First process the transactions to calculate the balance for each account
def process_account_balances():
    for i in range(len(csv_transactions)):
        from_name = csv_transactions[i].from_person
        to_name = csv_transactions[i].to_person
        pence_amount = csv_transactions[i].amount

        # todo - could refactor these as one function, passing in account_name, amount and credit/debit option
        if from_name in dict_accounts:
            current_balance = dict_accounts.get(from_name)
            new_debit_balance = int(current_balance) - pence_amount
            dict_accounts.update({from_name: new_debit_balance})
            # nested second IF as these should be atomic transactions ie either both succeed or both fail
            if to_name in dict_accounts:
                current_balance = dict_accounts.get(to_name)
                new_credit_balance = int(current_balance) + pence_amount
                dict_accounts.update({to_name: new_credit_balance})
    # end of FOR list of transactions

# Print the dictionary of account balances, showing key of name and value of balance as currency
def print_account_balances():
    print("\nShowing all Accounts and Balances")
    for key in dict_accounts:
        pretty_currency = format_pence_as_currency(dict_accounts[key])
        print(key, ': ', pretty_currency)

# formatting needed as currency balance is being stored as an int number of pence
def format_pence_as_currency(pence) -> str:
    pence_float = float(pence / 100)
    currency_str = "£{:,.2f}".format(pence_float)
    return currency_str

# List [Account] option should also print a list of every transaction, with the date and narrative, for that account with that name.
def list_account(account_name):
    print(f"\nTransactions for Account Name: {account_name}")
    # can also use syntax - `for trans in csv_transactions:`
    for i in range(len(csv_transactions)):
        if csv_transactions[i].from_person.lower() == account_name.lower() or csv_transactions[i].to_person.lower()  == account_name.lower():
            print(csv_transactions[i].printme())
            # todo fix bug of `None` being printed after each transaction entry

def print_menu():
    print("\nMenu Options")
    print(" `List All` - output the names of each person, and the total amount they owe, or are owed.")
    print(" `List [Account]` - print a list of every transaction, with the date and narrative, for that account with that name.")
    print(" `Quit`")

def main():
    read_file()
    option = ""
    while option != "Quit":
        print_menu()
        option = input("Type your choice: ")
        if option.lower() == "List All".lower():
            process_account_balances()
            print_account_balances()
        #  caters for second option, but won't run if user wants to quit
        elif len(option)>8:
            # get the customer name after the word 'list '
            cust = option[5:]
            list_account(cust)
    print('Quitting...')

if __name__ == '__main__':
    main()
