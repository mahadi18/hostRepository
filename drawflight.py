import pandas
import networkx as net
import scipy as sci
import numpy as np
import matplotlib.pyplot as plt
import os

file_root="F:\Semester 3 UPB\Information Retrieval\openflightdata"
routes_data=os.path.join(file_root,"routes.txt")
airports_data=os.path.join(file_root,"airports.txt")
##### Read the data file.########

with open(airports_data) as airports:
    for line in airports:
        print line


