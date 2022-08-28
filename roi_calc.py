import time
from time import sleep
from rejex import state_rent
import locale

locale.setlocale(locale.LC_ALL, '')

def m(x):
    return locale.currency(x, grouping=True)

def int_(x):
    x = str(x.replace("$", "").replace(" ", "").replace(",", ""))
    for n in x:
        if n not in "0123456789.":
            print("\n. . .\nERROR: Enter a valid number.\n. . .\n")
            return False
        else: 
            return float(x)

def dots(x):
    for z in range(x):
        print('.', end=' ', flush=True)
        time.sleep(0.3)

class ROI():
    def __init__(self, user):
        self.user = user
        self.income = {}
        self.expenses = {}
        self.investment = 0
        self.renters = 0

    def add_income(self):
        while True: 
            print("\nINCOME")
            if self.total_income() != 0:
                print(f"Total income so far: {m(self.total_income())}")
            response = input("\nWhat sort of monthly income would you like to add/adjust? \n\tEnter [R] for Rental, [P] for Parking, [L] for laundry or [O] for other. \n\tEnter [S] to show your total income. \n\tEnter [F] when you're finished:  ").lower()
            
            if response in ('rent'):
                rent = input("\nIf you already know your total rental income, enter it now. Otherwise, enter [C] to calculate.  ").lower()
                if rent != 'c':
                    if int_(rent):
                        self.income['rent'] = int_(rent)
                else:
                    indv_rent = input("\nHow much rent are you charging each renter? If you want to look up the average rent for your state, enter [S] to search: ")
                    if indv_rent.lower() in ('search'):
                        search = input("Enter the whole name of the state to search for: ")
                        if state_rent(search):
                            response = input(f"The average rent in {search.title()} is {m(state_rent(search))}. Would you like to use that amount? ").lower()
                            if response in ("yes"):
                                rent_calc = self.renter_calc('rent', (state_rent(search)))
                            else:
                                indv_rent = input("How much rent are you charging each renter? $")
                                if int_(indv_rent):
                                    rent_calc = self.renter_calc('rent', int_(indv_rent))
                    elif int_(indv_rent):
                        rent_calc = self.renter_calc('rent', int_(indv_rent))
                    self.income['rent'] = rent_calc

            elif response in ('parking'):
                park = input("\nIf you already know your parking income, enter is now. Otherwise, enter [C] to calculate.  ").lower()
                if park == 'c':
                    parking_calc = self.renter_calc("parking", rate=0)
                    self.income['parking'] = parking_calc
                elif int_(park):
                    self.income['parking'] = int_(park)
            
            elif response in ('laundry'):
                laundo = input("\nEnter the estimated amount of income for laundry:  $")
                if int_(laundo):
                    self.income['laundry'] = int_(laundo)

            elif response in ('other'):
                other = input("\nWhat other income do you want to add?  ").lower()
                other_income = input(f"What is your estimated income from {other}?  $")
                if int_(other_income):
                    self.income[other] = int_(other_income)

            elif response in ('show'):
                self.display_info("income")

            elif response in ('finish'):
                break
            
            else:
                print("Sorry, I didn't unserstand that input.")
    
    def total_income(self):
       return sum(self.income.values())

    def total_expenses(self):
       return sum(self.expenses.values())

    def intl_investment(self):
        print("\nINTITIAL INVESTMENT")
        t_inv = input("\nEnter how much your total property investment. If you're not sure, or want to add additional info, enter [C] to calculate:  ").lower()
        if t_inv == "c":
            dp = input("Enter how much you paid for your down payment. If you're not sure, enter [C] to calculate:  ").lower()
            if dp == "c":
                pv = input("Enter the total propety value:  $")
                if int_(pv):
                    dp = int(int(pv) * .2)
                    print(f"A typical down payment (20%) for this property would be {m(dp)}. Adding that to your initial investment.")
                    self.investment += dp
            elif int_(dp):
                self.investment += int_(dp)
            while True:
                o_inv = input("What other initial investments would you like to add? Example: Closing costs, Repairs, etc. When you're finished, enter [F]: " ).lower()
                if o_inv == "f":
                    break
                else: 
                    amount = input(f"how much would you like to add for {o_inv}? ")
                    if int_(amount):
                        self.investment += int_(amount)
        elif int_(t_inv):
            self.investment = int_(t_inv)
        print(f"Total initial investment: {m(self.investment)}")

    def add_expenses(self):
        while True:
            print("\nMONTHLY EXPENSES")
            if self.total_expenses() != 0:
                print(f"Total expenses so far: {m(self.total_expenses())}")
            response = input("\nWhat sort of monthly expenses would you like to add/adjust? \n\tEnter [M] for Mortgage payment, [I] for Insurance, [T] for Taxes or [O] for other. \n\tEnter [S] to show your total Expenses. \n\tEnter [F] when you're finished:  ").lower()
            if response in ("m", "mortgage"):
                mort = input("\nIf you already know your total mortgage, enter it now. Otherwise, enter [C] to calculate.  ").lower()
                if mort == "c":
                    print("Visit this website to calculate your mortgage payment: https://www.calculator.net/mortgage-calculator.html")
                    mort = input("\nEbter your estimated monthly mortgage payment:  $").lower()
                elif int_(mort):
                    self.expenses['rent'] = int_(mort)
            elif response in ("i", "insurance"):
                ins = input("\nEnter estimated monthly insurance:  $")
                if int_(ins):
                    self.expenses['insurance'] = int_(ins)
            elif response in ("t", "taxes"):
                tax = input("\nEnter estimated monthly taxes:  $")
                if int_(tax):
                    self.expenses['taxes'] = int_(tax)
            elif response in ('o', 'other'):
                other = input("\nWhat other expenses do you want to add?  ").lower()
                other_exp = input(f"What is your estimated expenses from {other}?  $").lower()
                if int_(other_exp):
                    self.expenses[other] = int_(other_exp)
            elif response in ('show'):
                self.display_info("expenses")
            elif response in ('finish'):
                break
            else:
                print("Sorry, I didn't unserstand that input.")

    def renter_calc(self, charge, rate=0):
        """calculates the price of something based on number of tenants. If number of thenats not yet known, asks and stores that info"""
        if self.renters != 0:
            renter = self.renters
        else: 
            renter = int_(input("How many renters are in your complex? "))
            self.renters = renter
        if not rate:
            rate = int_(input(f"how much does each renter pay for {charge}? $"))
        result = renter * rate
        print(f"\ntotal {charge} income: {m(result)}")
        return result

    def display_info(self, x):
        print(f"\n{x.upper()} BREAKDOWN")
        if x == "income":
            for key, value in self.income.items():
                print(f"\tIncome from {key}: {m(value)}")
            print(f"Total income: {m(self.total_income())}")
        elif x == "expenses":
            for key, value in self.expenses.items():
                print(f"\t{key.title()}: {m(value)}")
            print(f"Total Expenses: {m(self.total_expenses())}")
        elif x == "investment":
            print(f"Total initial investment: {m(self.investment)}")

    def calc_roi(self):
        while True: 
            print("Let's get started calculating ROI. We'll collect information about your intial investment in your propety and your monthly income and expenses.")
            if not self.total_income():
                self.add_income()
            if not self.total_expenses():
                self.add_expenses()
            if not self.investment: 
                self.intl_investment()
            print(f"\nlet's review {self.user.title()}'s information so far:")
            dots(3)
            self.display_info("income")
            self.display_info("expenses")
            self.display_info("investment")
            while True:
                response = input("\n\nIf you're ready to calculate ROI, enter [N] for next. Other wise, enter [INC] to edit income, [EXP] to edit investmen, or [INV] to edit invesments.\n")
                if response.lower() in "next":
                    break
                elif response.lower() == "exp":
                    self.add_expenses()
                elif response.lower() == "inc":
                    self.add_income()
                elif response.lower() == "inv":
                    self.intl_investment()
            mcashflow = self.total_income() - self.total_expenses()
            acashflow = mcashflow * 12
            dots(5)
            print(f"\nLet's calculate your total montlhy cash flow:\nIncome ({m(self.total_income())}) - Expenses ({m(self.total_expenses())}) = {m(mcashflow)}")
            dots(5)
            print(f"\nYour estimated annual cash flow is {m(acashflow)}")
            dots(5)
            roi = int((acashflow / self.investment) * 100)
            print("\nYour return on investment is ", end = "")
            dots(5)
            print(f"{roi}%!")
            if roi > 20:
                print("That's pretty high... you should consider lowering your rents, ya greedy capatalist!")
            elif roi >= 8:
                print("That's a pretty good ROI!")
            elif roi < 8:
                print("That's a little low. You should consider raising your rent!")
            elif roi < 0:
                print("That's a negative ROI! Please reconsider a career in finance!")
            
            response = input("\n\nIf you're satisifed, enter [Q] to exit. If you'd like to review or edit your information, press any other key\n")
            if response.lower() == "q":
                break

name = input("\n\nwelcome to Julia's Return on Invesment Calculator. Enter you name to begin: ").lower()
user = ROI(name)

user.calc_roi()





