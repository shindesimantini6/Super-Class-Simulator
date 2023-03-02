#%%
from PIL import Image
import numpy as np
#%%
#Market image
im = Image.open('images/supermarket.png')
market = np.array(im)
print(market.shape, market.dtype)
#%%
#Market image
im = Image.open('images/resized_market.png')
market = np.array(im)
print(market.shape, market.dtype)

#%%
#Tiles image
im = Image.open('tiles.png')
tiles = np.array(im)
print(tiles.shape, tiles.dtype)


#%%
#extract
x = 4 * 32   # 5th column starting from 0
y = 1 * 32   # 2nd row
apple = tiles[y:y+32, x:x+32]
# %%

#insert
tx = 13 * 32
ty = 2 * 32
market[ty:ty+32, tx:tx+32] = apple

#%%
#extract second icon
x = 4 * 32   
y = 3 * 32   
watermelon= tiles[y:y+32, x:x+32]
#%%
#insert watermelon
#insert
tx = 13 * 32
ty = 3 * 32
market[ty:ty+32, tx:tx+32] = watermelon

#%%
#extract drink
x = 13 * 32   
y = 3 * 32  
drink= tiles[y:y+32, x:x+32]
#%%
#insert drink
tx = 5 * 32
ty = 2 * 32
market[ty:ty+32, tx:tx+32] = drink
#%%
#extract a pacman
x = 0 * 32   
y = 4 * 32  
pacman= tiles[y:y+32, x:x+32]
#%%
#insert a pacman
tx = 14 * 32
ty = 7 * 32
market[ty:ty+32, tx:tx+32] = pacman
# %%
im = Image.fromarray(market)
im.save('supermarket_filled.png')
# %%
