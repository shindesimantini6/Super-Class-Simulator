#%%
# import all required packages
from supermarket import Supermarket
import csv
import time

# Instantiate the Supermarket clas
Tahini_supermarket = Supermarket("Amazing Tahini", 7, "22:00")
print(Tahini_supermarket.name)

# Open a csv file
with open (f"final_shoppers.csv", "w", encoding = 'UTF8', newline="") as f:
    writer = csv.writer(f)

    # Store the headers in a list
    headers = ['time','id_', 'name', 'location']
    
    # Write the headers into the CSV
    writer.writerow(headers) # Maybe this can be written outside the loop

    # Run a loop to checking if the supermarket is open or not
    while Tahini_supermarket.is_open():
        Tahini_supermarket.add_new_customers()
        Tahini_supermarket.next_minute()
        #print (Tahini_supermarket.print_customers())
        final_customers = Tahini_supermarket.print_customers() 
        for n in final_customers:
            if n != None:
               print(f"{n[0]},{n[1]},{n[2]}, {n[3]}")
               row = n
               # Write the data into the CSV
               writer.writerow(row)
            else:
                continue
        Tahini_supermarket.remove_exitsting_customers()
    f.close

# %%
