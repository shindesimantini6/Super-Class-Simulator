# Import all required packages
from nonstopshopper import Customer
import pandas as pd
from faker import Faker
import random
import pandas as pd
import numpy as np 

# Read the state transition probabilities
transition_pro = pd.read_csv('./probabilities.csv')

new_customer = 1.6 # lambda of poisson distribution

# # Create a DataFrame for time probabilities
# # initialize list of lists
# data = [['7:01', 2], ['7:03', 15], ['juli', 14]]
  
# # Create the pandas DataFrame
# df = pd.DataFrame(data, columns=['Name', 'Age'])

class Supermarket:
    """
    Manages multiple Customer instances that are currently in the market.
    Args:
        name (str): Name of the Supermarket

    """

    def __init__(self, supermarket_name, opening_time, closing_time):
        """
        Instantiates a number of objects required in the Supermarket class.

        """        
        
        # A list of Customer objects
        self.customers = []
        self.minutes = 0  # Opening of the Supermarket with no customers
        self.last_id = 0  # Id of the customers
        self.name = supermarket_name  # Name of the Supermarket
        self.opening_time = opening_time # Opening time of the store
        self.closing_time = closing_time # Closing time of the store

    def __repr__(self):
        """
        Returns a print statement for the start of the Day!!
        """
        return 'The day in the Supermarket has started'

    def is_open(self):
        """
        Check if the supermarket is open. Runs the get_time() function to return the 
        current time. 

        Args: 
            closing_time(str):Closing time as defined by the user
        
        Returns:
            True or False (Boolean): True is Supermarket is open, False if Supermarket is closed.
        """

        # Print the current time
        print(self.get_time())

        return self.get_time() != self.closing_time

    def n_customers(self):
        '''Returns the number of customers in the supermarket'''
        return len(self.customers)

    def get_time(self):
        """
        Current time in HH:MM format.

        Args: 
            opening_time (int): Opening time of the store

        Returns:
            timestamp (str): Timestamp in HH:MM format
        
        """

        # Define the hour from the minutes
        hour = self.opening_time + self.minutes // 60

        # Define the minutes from the minutes
        minutes = self.minutes % 60

        # Create a string formatted timestamp from the hour and minutes
        timestamp = f"{hour:02d}:{minutes:02d}"
        print(timestamp)
        return timestamp

    def print_customers(self):
        """
        Print all customers with the current time, id, location.

        Returns:
            headers (list): List of headers for the CSV file
            row (list): List of values of timestamp, customer id, customer name, and customer state (location)
        
        """

        # Create an empty list to store all values
        final_states = []
        # fruits_state = []
        # spices_state = []
        # checkout_state = []
        # drinks_state = []
        # dairy_state = []

        print(self.customers)        
        # Loop through the customers list to extract the name, id, state (location) and timestamp of the customer
        for customer in self.customers:
            print (customer)
            name = customer.name
            id_ =   customer.id
            time = self.get_time()
            location = customer.state
            no_cust = self.n_customers()
            
            print(f"Customer name {name} with {id_} came to the store at {time} at {location}")

            # Store the customer attributes in a list
            row = [time, id_, name, location, no_cust]
            print(row)


            # Append the customers to the list
            final_states.append(row)
        return final_states
        #     if location == "fruit":
        #         fruits_state.append(location)
        #     elif location == "spices":
        #         spices_state.append(location)
        #     elif location == "dairy":
        #         dairy_state.append(location)
        #     elif location == "checkout":
        #         checkout_state.append(location)
        #     else:
        #         drinks_state.append(location)
            
        #     # Append the customers to the list
        #     final_states.append(row)
            
        # return final_states, fruits_state, spices_state, checkout_state, dairy_state, drinks_state

    def next_minute(self):
        """
        Propagates all customers to the next state.
        Extends the minutes by 1 and runs the next_state function from Customer class to 
        define the next state of the customer.
        
        """

        #print(self.customers)

        # Increase the minute by 1
        self.minutes = self.minutes + 1

        # Loop through the existing customers and find their next state (location)
        for customer in self.customers:
            customer.next_state()
            
    def add_new_customers(self):
        """
        Randomly creates new customers and gives them a fake name and adds to their id in an increading order of one.
        
        """
        # Get the timestamp of the Customer
        self.time = self.get_time()

        # Randomly decide number of customers per timestamp 
        number_per_timestamp = np.random.poisson(new_customer)
        print(number_per_timestamp)

        # Instantiate faker
        f = Faker()

        # Hard code a budget 
        budget = 100 # maybe we don't need this

        for n in range(number_per_timestamp):
            print(n)

            # Increase the id by one for each customer added
            self.last_id += 1

            # Create a variable with fake names
            cust_name = f.name()

            # Instantiate the Customer class
            customer = Customer(self.last_id, cust_name, budget)
            print(customer)

            # Append the customers list with the customer
            self.customers.append(customer)
        
        # print(self.customers)

    def remove_exitsting_customers(self):
        """
        Removes every customer that is not active any more.

        """
        
        # Loop through the customers list to find the active and inactive customers.
        for customer in self.customers:
            if not customer.is_active():
                self.customers.remove(customer)
                print(self.customers)
            else:
                print(self.customers)
                continue


# TEST:
# if __name__ == "__main__":
#     oCustomer = Customer("Jake", transition_pro, 100)
#     print(oCustomer)
#     oSupermarket = Supermarket("Aldi")
#     oSupermarket.add_new_customers()
#     print(oCustomer.state)

#     with open (f"final_shoppers.csv", "w", encoding = 'UTF8') as f:
#         writer = csv.writer(f)
#         while oSupermarket.is_open():
#             oSupermarket.next_minute()
#             print (oSupermarket.print_customers())
#             if oSupermarket.remove_exitsting_customers() != None:
#                 headers, row = oSupermarket.remove_exitsting_customers()
#                 print(headers, row)
#             # Write the headers
#                 writer.writerow(headers)

#                 # Write the data
#                 writer.writerow(row)
#             else:
#                 continue
