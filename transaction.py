class Transaction:

    def __init__(self, date, from_person, to_person, narrative, amount):
        self.date = date
        self.from_person = from_person
        self.to_person = to_person
        self.narrative = narrative
        self.amount = amount    #should be ints as pence amount

    def __eq__(self, other):
        print("_checking transaction obj equaltiy_")
        return self.date == other.date and self.from_person == other.from_person and self.to_person == other.to_person and self.narrative == other.narrative and self.amount == other.amount

    def printme(self):)
        print(f"Date: {self.date},  Payment From: {self.from_person}, Payment To: {self.to_person}, Narrative: {self.narrative}, Amount: {self.amount}")
