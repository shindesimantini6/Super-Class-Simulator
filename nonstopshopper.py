# TO DO:
# 1. Add a row to with location 'entrance'
# 2. Recalculate the probabilities
# 2. Class --> Customers
    # 2.1 initiate --> random name
                #  --> id
# 3. Class --> Supermarket Class

# 4. Image of the Supermarket with icograms
# 5. Combined with image of customers (Download images of customers)
# 6. Time vs Customers entry probabilities (additional probability in the movement)

#%%
import pandas as pd
transition_pro = pd.read_csv('./probability/probabilities.csv')

#%%

import random
import numpy as np

#%%
#Define the first class
class Customer:
    """
    a single customer that moves through the supermarket
    in a MCMC simulation
    """
    def __init__(self, name, state, transition_pro, budget=100):#Write a constructor
        self.name = name
        self.state = state
        self.transition_pro = transition_pro
        self.budget = budget
    
    def __repr__(self):#The method __repr__() is called whenever an object is converted to a string (e.g. by print).
        return f'<Customer {self.name} in {self.state}>'

    def next_state(self):
        '''
         Propagates the customer to the next state.
         Returns nothing.
         '''
        print(f"Initial state of the Customer {self.state}")
        prob = self.transition_pro.loc[transition_pro["location"] == self.state].loc[:, transition_pro.columns != 'location'].values[0]
        self.state = np.random.choice(['checkout', 'dairy', 'drinks', 'fruits', 'spices'], p = prob)
        print(f"Next State of the customer {self.state}")

    def is_active(self):
        """
        Returns True if the customer has not reached the checkout yet.
        """
        
        if self.state != "checkout":
            is_active = True  

#Instantiate the class
cust1 = Customer("Jake", "drinks", transition_pro, 50) #provide values for all non-default parameters except self
# cust2 = Customer("Margaret", "spices")
cust1.next_state()
cust1.is_active()

#Access attributes
#print(cust1.name, cust1.state)
#print(cust2.name, cust2.budget)

print(cust1)
# %%
