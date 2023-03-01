# Import all required packages
from nonstopshopper import Customer
import pandas as pd
from faker import Faker
import pandas as pd

# Read the state transition probabilities
transition_pro = pd.read_csv('./probabilities.csv')

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
        print(self.customers)        
        # Loop through the customers list to extract the name, id, state (location) and timestamp of the customer
        for customer in self.customers:
            name = customer.name
            id_ =   self.last_id
            time = self.get_time()
            location = customer.state
            
            print(f"Customer name {name} with {id_} came to the store at {time} at {location}")

            # Store the headers in a list
            headers = ['time','id_', 'name', 'location']  # Should we not hard code this ?
            print(headers)

            # Store the customer attributes in a list
            row = [time, id_, name, location]
            print(row)

            return headers, row

    def next_minute(self):
        """
        Propagates all customers to the next state.
        Extends the minutes by 1 and runs the next_state function from Customer class to 
        define the next state of the customer.
        
        """

        print(self.customers)

        # Increase the minute by 1
        self.minutes = self.minutes + 1

        # Loop through the existing customers and find their next state (location)
        for customer in self.customers:
            customer.next_state()
            
    def add_new_customers(self):
        """
        Randomly creates new customers and gives them a fake name and adds to their id in an increading order of one.
        
        """

        # Instantiate faker
        f = Faker()

        # Create a variable with fake names
        cust_name = f.name()

        # Hard code a budget 
        budget = 100 # maybe we don't need this

        # Increase the id by one for each customer added
        self.last_id += 1

        # Instantiate the Customer class
        customer = Customer(cust_name, budget)

        # Get the timestamp of the Customer
        self.time = self.get_time()

        # Append the customers list with the customer
        self.customers.append(customer)
        print(self.customers)

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
