#%%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%%

def create_charts(data, headers, current_time):
    # Read csv into a pandas dataframe
    final_shopper_list = pd.DataFrame(data,columns=headers)

    # Group by dataframe for each minute
    customer_section_minute = pd.DataFrame(final_shopper_list.groupby(['location', 'time'])['id_'].count().reset_index())
    customer_section_minute

    sns.barplot(data=customer_section_minute.loc[customer_section_minute['time']== current_time] , x= 'location', y= 'id_')
    plt.title(f'Customers in each section in the minute: {current_time}')
    plt.ylim(top=12)
    plt.ylabel('Customer count')
    plt.xlabel('Supermarket section')
    plt.savefig(f'./Images/charts_customers/customer_{current_time}.png') 
    # plt.show();

# # %%

# headers = ['time','id_', 'name', 'location', 'no_customer_at_timestamp']
# data = [['07:08:00', 2, 'Bonnie Richards', 'drinks', 10], ['07:08:00', 4, 'Derek Hernandez', 'checkout', 10], ['07:08:00', 5, 'Ariel Edwards', 'drinks', 10], ['07:08:00', 6, 'Dr. Luke Ochoa', 'dairy', 10], ['07:08:00', 7, 'Sarah Williamson', 'fruit', 10], ['07:08:00', 9, 'Monica Ballard', 'checkout', 10], ['07:08:00', 11, 'Terry Young', 'checkout', 10], ['07:08:00', 13, 'Kristine Smith', 'fruit', 10], ['07:08:00', 14, 'Marcus Ferguson', 'dairy', 10], ['07:08:00', 15, 'Joshua Durham', 'drinks', 10]]

# pd.DataFrame(data,columns=headers)
# %%
