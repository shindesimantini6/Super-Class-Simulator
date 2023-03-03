#%%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#%%
# path_name = 'charts_customers'
# os.mkdir(path_name)

#%%

def create_folder(parent_directory, chart_directory):
    """
    Creates a folder in the desired filepath. 

    Args: 
        path_name(str): Filepath of the to be created folder.

    """
    
    # Create a empty directory to store the images if it doesn't exist
    charts_path = os.path.join(parent_directory, chart_directory)
    if not os.path.exists(charts_path):
        os.makedirs(charts_path)

#%%

def create_charts(data, headers, current_time):
    """
    Creates charts for each timestamp and saves them in a folder created.

    Args:
        data(list): List of all values for timestamp, customer id, customer name, location
            and customer numbers for that timestamp.
        current_time(str): Current time of the Customers movement

    """
    
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
    plt.savefig(f'./images/charts_customers/customer_{current_time}.png') 
