#%%
import numpy as np
import pandas as pd
import random

#%%
minutes_simulation = 60 * 15
new_customer = 1.6 # lambda of poisson distribution
states = ['fruit', 'spices', 'dairy', 'drinks', 'checkout']
prob = pd.read_csv('probabilities.csv', index_col=0)


class Customer:
    ''' Customer that moves through
      the supermarket'''
    
    def __init__(self, id):
        self.id = id
        self.location = 'entrance'

    def next_location(self):
        '''Calculates the next location with the weighted probabilities of the transition matrix'''
        self.location = random.choices(states, list(prob.loc[self.location]))[0]

       
    def is_active(self):
        """Returns False if the customer is at the checkout location, and True at all other location"""
        if self.location != 'checkout':
            return True
        else:
            return False

    def __repr__(self):
        """formats as CSV"""
        return f"{self.id}, {self.location}"

#%%
class Supermarket:
    """Customer instances that are 
    currently in the supermarket"""

    def __init__(self, name):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.name = name

    @property
    def get_time(self):
        '''Current time in HH:MM format'''
        hour = 7  + self.minutes // 60
        min = self.minutes % 60
        return f"{hour:02}:{min:02}:00"


    def next_minute(self):
        """It sets one minute and moves all customers to the next location"""
        self.minutes += 1
        for c in self.customers:
            c.next_location()
            self.print_customer(c)

    def add_new_customers(self):
        """New customer added in every minute calulated with the lamda=1.6"""
        n = np.random.poisson(new_customer)
        for i in range(n):
            self.last_id += 1
            cust = Customer(self.last_id)
            self.customers.append(cust)
            self.print_customer(cust)

    def remove_existing_customers(self):
        """
        Recreates customers list from active customer (who are not at the checkout), 
        in this way, it removes customers that are at the checkout
        """
        self.customers = [cust for cust in self.customers if cust.is_active]

    def print_customer(self, customer):
        """Prints one row of CSV"""
        row = str(self) + ', ' + str(customer)
        print(row)

    def __repr__(self):
        """formats as CSV"""
        return f"{self.get_time}, {self.name}"

#%%
if __name__ == '__main__':

    supermarket = Supermarket("NonStopShopper")

    for i in range(minutes_simulation):
        supermarket.next_minute()
        supermarket.add_new_customers()
        #supermarket.print_customer()
        supermarket.remove_existing_customers()
# %%
