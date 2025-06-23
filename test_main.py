# %%

# Testing of routines of mkj

import re


album = "My Music Album CD12 Absolute"
album = re.sub(r" CD[0-9]*", "", album)
print(album)


# %%
