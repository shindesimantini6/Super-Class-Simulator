#%%
# import all required packages and libraries
from supermarket import Supermarket
import csv
import cv2
import numpy as np
from SupermarketMap import SupermarketMap
import time
from PIL import Image
from create_charts import create_charts

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

# Define the background of the gif
background = np.ones((1000, 730, 3), np.uint8)
background = 255 * background

# Read the tiles png
tiles = cv2.imread("./Images/tiles_new.png")

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
Tahini_supermarket = Supermarket("Amazing Tahini", 7, "08:08:00", 1.6) # Can change the time based on user
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

        if final_customers != None:
            # Create chart for current time
            create_charts(final_customers, headers, current_time)

            time.sleep(0.5)

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
            
            smallImage = cv2.imread(f"./Images/charts_customers/customer_{current_time}.png") #50x50 for you
            height, width, channels = smallImage.shape
            image_x = (700 - width) // 2
            image_y = 480 + 20  # Add some space between the text and the GIF
            offset = np.array((image_y, 40))  # Top-left point from which to insert the smallest image. height first, from the top of the window
            frame[offset[0]:offset[0] + height, offset[1]:offset[1]+width] = smallImage

            # Display the frame
            cv2.imshow("frame", frame)

        else:
            continue
    cv2.destroyAllWindows()
    
    # TO DO:Need comment here
    supermarket_map.write_image("NonStopShopper.png")
    f.close
