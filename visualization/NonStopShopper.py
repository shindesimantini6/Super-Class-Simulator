#%%
import numpy as np
import pandas as pd
import cv2
import random
import time
#%%
minutes_simulation = 60 * 15
new_customer = 1.6 # lambda of poisson distribution
states = ['fruit', 'spices', 'dairy', 'drinks', 'checkout']
prob = pd.read_csv('probabilities.csv', index_col=0)

# size of a tile (32*32 pixels = 1 tile)
TILE_SIZE = 32               

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
##XX##########EE##
""".strip()


class SupermarketMap:
    """Constructor for the map, visualizes the supermarket layout(MARKET) with extracting the icons from the tiles"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "Z":
            return self.extract_tile(0, 4)
        elif char == "C":
            return self.extract_tile(5, 3)
        elif char == "D":
            return self.extract_tile(3, 13)
        elif char == "E":
            return self.extract_tile(7, 3)
        elif char == "S":
            return self.extract_tile(5, 8)     
        elif char == "V":
            return self.extract_tile(2, 11)        
        elif char == "X":
            return self.extract_tile(6, 10)
        else:
            return self.extract_tile(1, 2)
        
    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


class Customer: 
    """
    Customer class that models the customer behavior in a supermarket.
    """

    def __init__(self, id, map, avatar):
        """
        supermarket: A SuperMarketMap object
        avatar : a numpy array containing a 32x32 tile image
        row: the starting row
        col: the starting column
        """
        self.id = id
        self.location = 'entrance'
        self.map =map
        self.avatar = avatar

    def draw(self, frame):
        '''# places the customer-object onto the map'''
        x = 11 * TILE_SIZE
        y = random.randint(12,15) * TILE_SIZE
        frame[x:x+TILE_SIZE, y:y+TILE_SIZE] = self.avatar

    def next_location(self):
        '''Calculates the next location with the weighted probabilities of the transition matrix'''
        ''' places the customer-object onto the map'''
        self.location = random.choices(states, list(prob.loc[self.location]))[0]

        if self.location == 'fruit':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(14,15)
        elif self.location == 'spices':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(10,11) 
        elif self.location == 'dairy':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(6,7)
        elif self.location == 'drinks':
            x = TILE_SIZE * random.randint(2,6)
            y = TILE_SIZE * random.randint(2,3)
        else:
            x = TILE_SIZE * random.randint(8,9)
            y = TILE_SIZE * random.randint(4,7)
        frame[x:x+TILE_SIZE, y:y+TILE_SIZE] = self.avatar

    @property    
    def is_active(self):
        """Returns False if the customer is at the checkout location, and True at all other location"""
        if self.location != 'checkout':
            return True
        else:
            return False

    def __repr__(self):
        """formats as CSV"""
        return f"{self.id}, {self.location}"


class Supermarket:
    """This class controls the list of Customer instances that are currently in the supermarket (customer.active = True)."""

    def __init__(self, name):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.name = name

    @property
    def get_time(self):
        '''Current time in HH:MM format'''
        hour = 7  + self.minutes // 60
        min = self.minutes % 60
        return f"{hour:02}:{min:02}:00"

    @property
    def n_customers(self):
        '''Returns the number of customers in the supermarket'''
        return len(self.customers)


    def next_minute(self):
        """It sets one minute and moves all customers to the next location"""
        self.minutes += 1
        for c in self.customers:
            c.next_location()
            self.print_row(c)

    def add_new_customers(self):
        """New customer added in every minute calulated with the lamda=1.6"""
        n = np.random.poisson(new_customer)
        for i in range(n):
            self.last_id += 1
            c = Customer(self.last_id, map, avatar)
            c.draw(frame)
            self.customers.append(c)
            self.print_row(c)

    def remove_existing_customers(self):
        """
        Recreates customers list from active customer (who are not at the checkout), 
        in this way, it removes customers that are at the checkout
        """
        self.customers = [c for c in self.customers if c.is_active]

    def print_row(self, customer):
        """Prints one row of CSV"""
        row = str(self) + ', ' + str(customer)
        print(row)

    def __repr__(self):
        """formats as CSV"""
        return f"{self.get_time}, {self.name}, {self.n_customers}"


if __name__ == "__main__":

    background = np.zeros((500, 700, 3), np.uint8)
    tiles = cv2.imread("tiles.png")
    
    # Instantiating a TilesMap object 
    map = SupermarketMap(MARKET, tiles)

    avatar = tiles[3*TILE_SIZE:4*TILE_SIZE,1*TILE_SIZE:2*TILE_SIZE] # pacman = client
     
    # Instantiating a Customer and Supermarket object 
    supermarket = Supermarket("NonStopShopper") 

    for i in range(minutes_simulation):
        frame = background.copy()
        map.draw(frame) 


        supermarket.next_minute()
        supermarket.add_new_customers()
        supermarket.remove_existing_customers()
        time.sleep(0.5)


        # https://www.ascii-code.com/
        key = cv2.waitKey(1)
        if key == 113: # 'q' key
            break
    
        cv2.imshow("frame", frame)

    cv2.destroyAllWindows()
    
    supermarket.write_image("NonStopShopper.png")
# %%
