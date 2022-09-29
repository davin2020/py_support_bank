class Account:

    def __init__(self, account_name):
        self.account_name = account_name
        self.balance = 0
        self.history = []

    def printme(self):
        print("-heres my account")
        print(self.account_name)
        print(self.balance)
        print(self.history)
        for i in range(len(self.history)):
            print(self.history[i].printme())
        # todo how to print array in py and see nested values?
