# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:15:44 2020

@author: Greeshma
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors

def disp(data,size,thresh):
    xval = range(size)
    yval = range(size)
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['k','palegreen', 'tomato',])
    im = ax.imshow(data, cmap, interpolation='none', vmin = thresh* -3,vmax=thresh*3)

    ax.set_xticks(np.arange(len(yval)))
    ax.set_yticks(np.arange(len(xval)))

    ax.set_xticklabels(yval)
    ax.set_yticklabels(xval)
    
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
             rotation_mode="anchor")
    
    for i in range(len(xval)):
        for j in range(len(yval)):
            text = ax.text(j, i, data[i, j],
                           ha="center", va="center", color="midnightblue")
    
    ax.set_title("Safe Path")
    fig.tight_layout()
    fig.set_size_inches(18.5, 10.5, forward=True)
    plt.show()