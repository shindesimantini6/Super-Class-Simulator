# TO DO:
# 1. Add a row to with location 'entrance' --> DONE
# 2. Recalculate the probabilities --> DONE
# 2. Class --> Customers --> DONE
    # 2.1 initiate --> random name --> DONE
                #  --> id --> DONE
# 3. Class --> Supermarket Class --> DONE

# 4. Image of the Supermarket with icograms
# 5. Combined with image of customers (Download images of customers)
# 6. Time vs Customers entry probabilities (additional probability in the movement)

#%%
# import pandas as pd
# transition_pro = pd.read_csv('./probabilities.csv')

#%%

# Import all required packages
import random
import numpy as np
import pandas as pd

# Read the transition probabilities
transition_pro = pd.read_csv('./probabilities.csv')


#Define the first class
class Customer:
    """
    A single customer that moves through the supermarket
    in a MCMC simulation
    """
    def __init__(self, cust_id, name, budget):#Write a constructor

        """
        Instantiates a number of objects required in the Customer class.

        """
        self.id = cust_id
        self.name = name  # Customer name
        self.state = "entrance"  # Default initial state (location) as entrance
        self.budget = budget  # Budget of the customer
    
    def __repr__(self):  #The method __repr__() is called whenever an object is converted to a string (e.g. by print).
        return f'<Customer {self.name} in {self.state}>'

    def next_state(self):
        '''
        Propagates the customer to the next state based on the probabilities defined in transition_pro.

        Returns:
            state(str) : State (location) is the next state (location) of the customer.

        '''
        
        print(f"Initial state of the {self.name} {self.state}")

        # Extract the probabilites defined for the initial state (locaiton)
        prob = transition_pro.loc[transition_pro["location"] == self.state].loc[:, transition_pro.columns != 'location'].values
        # print(prob)

        # Reassign the class state with the probabilites
        self.state = np.random.choice(['checkout', 'dairy', 'drinks', 'fruit', 'spices'], p = prob[0])
        print(f"Next State of the {self.name} {self.state}")
        return self.state

    def is_active(self):
        """
        Returns True if the customer has not reached the checkout yet.

        Returns:
            True or False (Boolean): True if customer not checked out else False.
        """
        
        if self.state != "checkout":
            return True  
        else:
            return False 


# # #Instantiate the class
# cust1 = Customer("Jake", transition_pro, 50) #provide values for all non-default parameters except self
# # cust2 = Customer("Margaret", "spices")
# cust1.next_state()
# cust1.is_active()

# #Access attributes
# #print(cust1.name, cust1.state)
# #print(cust2.name, cust2.budget)

# # print(cust1)
# # %%

# %%
