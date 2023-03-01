#%%
import pandas as pd
import numpy as np
import random
from faker import Faker
prob = pd.read_csv('probabilities.csv')
prob

states = ['fruit', 'spices', 'dairy', 'drinks', 'checkout']

#%%
#Define the first class
class Customer:
    """
    a single customer that moves through the supermarket
    in a MCMC simulation
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.location = 'entrance'


    def next_state(self):
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        self.location = random.choices(states, list(prob.loc[self.location]))[0]
        
    @property 
    def is_active(self):
        """Returns True if the customer has not reached the checkout yet."""
        if self.location != 'checkout':
            return True
        else:
            return False

    def __repr__(self):
        return f'<Customer {self.name} is in/at the {self.location}>'


#Instantiate the class
cust1 = Customer(1, "Jake")
cust2 = Customer(2, "Margaret") 

# access attributes
print(cust1.id, cust1.name, cust1.location)
print(cust2.id, cust2.name, cust2.location)

print(cust1)
# %%

#Creating fake names
def fake_name():
    f = Faker()
    name = f.name()
    return name

cust_fake_name = fake_name()
cust3 = Customer(3, f'{cust_fake_name}')

cust3
cust3.name

# %%
