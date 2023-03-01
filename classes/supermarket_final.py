#%%
import numpy as np
import pandas as pd
import random

#%%
prob = pd.read_csv('probabilities.csv')
prob
#%%
new_customer = 1.6 # lambda of poisson distribution
states = ['checkout', 'diary', 'drinks','fruit', 'spices']

#%%
class Customer:
    """
    a single customer that moves through the supermarket
    in a MCMC simulation
    """

    def __init__(self, id):
        self.id = id
        #self.name = name
        self.location = 'entrance'

    def next_location(self):
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        self.location = random.choices(states, list(prob.loc[self.location]))
        
   
    def is_active(self):
        """Returns True if the customer has not reached the checkout yet."""
        if self.location != 'checkout':
            return True
        else:
            return False

    def __repr__(self):
        return f'<Customer {self.id} is in/at the {self.location}>'

#Instantiate the class
cust1 = Customer(1)
cust2 = Customer(2) 


print(cust1)

#%%
class Supermarket:
    """Customer instances that are currently 
    in the supermarket"""

    def __init__(self, name):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.name = name

    def is_open(self):
        return self.get_time() != "22:00"
    
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
        """New customer added in every minute 
        calulated with the lamda=1.6"""
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
        self.customers = [cust for cust in self.customers if cust.is_active()]

    def print_customer(self, customer):
        """Prints one row of CSV"""
        row = str(self) + ', ' + str(customer)
        print(customer)

    def __repr__(self):
        """formats as CSV"""
        return f"{self.get_time}, {self.name}"

if __name__ == "__main__":
    NonStopShopper = Supermarket("NonStopShopper")
    print(NonStopShopper.get_time())


# %%
