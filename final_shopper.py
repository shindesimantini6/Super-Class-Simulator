#%%
# import all required packages
from supermarket import Supermarket
import csv

# Instantiate the Supermarket clas
Tahini_supermarket = Supermarket("Amazing Tahini", 7, "22:00")
print(Tahini_supermarket.name)

# Open a csv file
with open (f"final_shoppers.csv", "w", encoding = 'UTF8', newline="") as f:
    writer = csv.writer(f)
    
    # Run a loop to checking if the supermarket is open or not
    while Tahini_supermarket.is_open():
        Tahini_supermarket.add_new_customers()
        Tahini_supermarket.next_minute()
        print (Tahini_supermarket.print_customers())
        if Tahini_supermarket.print_customers() != None:
            headers, row = Tahini_supermarket.print_customers()
            print(headers, row)

           # Write the headers into the CSV
            writer.writerow(headers) # Maybe this can be written outside the loop

            # Write the data into the CSV
            writer.writerow(row)
        else:
            continue
        Tahini_supermarket.remove_exitsting_customers()
    f.close

# %%
