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

# Import all required packages
import random
import numpy as np
import pandas as pd

# Read the transition probabilities
transition_pro = pd.read_csv('./input_data/probabilities.csv')

# size of a tile (32*32 pixels = 1 tile)
TILE_SIZE = 32

#Define the first class
class Customer:
    """
    A single customer that moves through the supermarket
    in a MCMC simulation

    Args:
        cust_id(int): id of the Customer
        name(str): Name of the Customer
        budget(int): Budget of the Customer
    """

    def __init__(self, cust_id, name, budget, avatar):#Write a constructor

        """
        Instantiates a number of objects required in the Customer class.

        """
        self.id = cust_id
        self.name = name  # Customer name
        self.state = "entrance"  # Default initial state (location) as entrance
        self.budget = budget  # Budget of the customer
        self.avatar = avatar  # Avatar for the Customer
    
    def __repr__(self):  #The method __repr__() is called whenever an object is converted to a string (e.g. by print).
        return f'<Customer {self.name} in {self.state}>'

    def draw(self, frame):
        """
        Places the customer-object onto the map

        """

        x = 11 * TILE_SIZE
        y = random.randint(12,15) * TILE_SIZE
        frame[x:x+TILE_SIZE, y:y+TILE_SIZE] = self.avatar

    def next_state(self, frame):
        """
        Propagates the customer to the next state based on the probabilities defined in transition_pro.

        Args:
            frame(matrix): Background image.

        Returns:
            state(str) : State (location) is the next state (location) of the customer.

        """
        
        print(f"Initial state of the {self.name} {self.state}")

        # Extract the probabilites defined for the initial state (locaiton)
        prob = transition_pro.loc[transition_pro["location"] == self.state].loc[:, transition_pro.columns != 'location'].values

        # Reassign the class state with the probabilites
        self.state = np.random.choice(['checkout', 'dairy', 'drinks', 'fruit', 'spices'], p = prob[0])
        print(f"Next State of the {self.name} {self.state}")

        if self.state == 'fruit':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(14,15)
        elif self.state == 'spices':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(10,11) 
        elif self.state == 'dairy':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(6,7)
        elif self.state == 'drinks':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(2,3)
        else:
            x = TILE_SIZE * random.randint(8,9)
            y = TILE_SIZE * random.randint(4,7)
        frame[x:x+TILE_SIZE, y:y+TILE_SIZE] = self.avatar
        
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
