#%%
# import all required packages and libraries
from supermarket import Supermarket
import csv
import cv2
import numpy as np
from supermarketmap import SupermarketMap
import time
from PIL import Image
from create_charts import create_charts
from create_charts import create_folder
import imageio
#%%

def add_element_and_get_index(element, element_list):
    """
    Checks if an element is in a list and adds it to the list if not.
    Returns the index of the element in the list.
    Args:
        element (str):
            Element to be added to the list
        element_list (list):
            List to add the element to
    Returns:
         Index of inserted element in the list
    """
    if element not in element_list:
        element_list.append(element)
    return element_list.index(element)


time_list = []

# represantation of the market with one symbol '#', '.', 'b' or similar for each tile on the png-file
MARKET ="""
##################
##..............##
#D..DS..SZ..ZV..V#
#D..DS..SZ..ZV..V#
#D..DS..SZ..ZV..V#
#D..DS..SZ..ZV..V#
#D..DS..SZ..ZV..V#
##...............#
##..CC..CC..CC...#
##..CC..CC..CC...#
##...............#
##########XX##EE##
""".strip()

# Path where the file has to be saved
parent_directory =  './images'
chart_directory = 'charts_customers'
charts_filepath = create_folder(parent_directory, chart_directory)

# Path for animation images
parent_directory =  './images'
chart_directory = 'charts_gif'
charts_filepath = create_folder(parent_directory, chart_directory)

# Define the background of the gif
background = np.ones((1000, 930, 3), np.uint8)
background = 255 * background

# Read the tiles png
tiles = cv2.imread("./images/tiles_new.png")

# TEXT DESIGN: Write some Text for the title
font                   = cv2.FONT_HERSHEY_TRIPLEX
bottomLeftCornerOfText = (5,450)
fontScale              = 1
fontColor              = (255, 0, 127)
thickness              = 1
lineType               = 2

# Write some Text for the data
font2                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText2 = (5,490)
fontScale2              = 0.5
fontColor2              = (0, 0, 0)
thickness2              = 1
lineType2               = 2

# Instantiating a TilesMap object 
supermarket_map = SupermarketMap(MARKET, tiles)

# Instantiate the Supermarket object
Tahini_supermarket = Supermarket("NonStopShopper!", 7, "08:08:00", 1.6) # Can change the time based on user
print(Tahini_supermarket.name)

# Size of a tile (32*32 pixels = 1 tile)
TILE_SIZE = 32    

# Create function to read images from the folder based on the time

# Open a CSV file
with open (f"final_shoppers.csv", "w", encoding = 'UTF8', newline="") as f:
    writer = csv.writer(f)

    # Store the headers in a list
    headers = ['time','id_', 'name', 'location', 'no_customer_at_timestamp']
    
    # Write the headers into the CSV
    writer.writerow(headers) # Maybe this can be written outside the loop 

    # Find the avatar of in the tiles png
    avatar = tiles[3*TILE_SIZE:4*TILE_SIZE,1*TILE_SIZE:2*TILE_SIZE] # pacman = client
    
    # Run a loop to checking if the supermarket is open or not
    while Tahini_supermarket.is_open():
        frame = background.copy()
        supermarket_map.draw(frame) 
        Tahini_supermarket.add_new_customers(avatar)
        Tahini_supermarket.next_minute(frame)
        final_customers = Tahini_supermarket.print_customers() 
        for n in final_customers:
            if n != None:
               print(f"{n[0]},{n[1]},{n[2]}, {n[3]}")
               # Write the data into the CSV
               writer.writerow(n)
            else:
                continue
        print(final_customers)
        Tahini_supermarket.remove_exitsting_customers()
        Tahini_supermarket.get_text(frame, bottomLeftCornerOfText2, font2, fontScale2, fontColor2,thickness2, lineType2)
        current_time = Tahini_supermarket.get_time()
        print(current_time)
        add_element_and_get_index(current_time, time_list)
        time.sleep(0.5)

        if len(final_customers) != 0:
            # Create chart for current time
            create_charts(final_customers, headers, current_time)

            # TO DO: Need comments here
            key = cv2.waitKey(1)
            if key == 113: # 'q' key
                break
            
            cv2.putText(frame,'NonStopShopper!', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType) 
            
            smallImage = cv2.imread(f"./images/charts_customers/customer_{current_time}.png") #50x50 for you
            height, width, channels = smallImage.shape
            image_x = (700 - width) // 2
            image_y = 480 + 20  # Add some space between the text and the GIF
            offset = np.array((image_y, 40))  # Top-left point from which to insert the smallest image. height first, from the top of the window
            frame[offset[0]:offset[0] + height, offset[1]:offset[1]+width] = smallImage

            def rescale_frame(frame, percent=200):
                width = int(frame.shape[1] * percent/ 100)
                height = int(frame.shape[0] * percent/ 100)
                dim = (width, height)
                return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

            # Display the frame
            frame_rescaled = rescale_frame(frame)
            cv2.imshow("frame", frame_rescaled)
            cv2.imwrite(f'./images/charts_gif/final_{current_time}.png',frame_rescaled)

        else:
            continue
    cv2.destroyAllWindows()
    
    # TO DO:Need comment here
    supermarket_map.write_image("NonStopShopper.png")
    f.close

#Generate the GIF


images = []

for value_time in time_list:
    filename = './images/charts_gif/final_{}.png'.format(value_time)
    images.append(imageio.imread(filename))

imageio.mimsave('output_final.gif', images, fps=1)
# %%
