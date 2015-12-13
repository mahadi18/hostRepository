######################Description#######################3
# Author: Bishnu Sarker, DMKM, UPMC, UPB Email: bishnukuet@gmail.com
# This program populates the graph from the given raw text. and Save in binary format.
# this also finds Out degree each node and save fro future use.
############################

import pandas
import scipy as sci
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

#print os.curdir
file_root=os.path.join("C:\Users\Acer PC\PycharmProjects\OpenFlightRanking","Data")
routes_data=open(os.path.join(file_root,"routes.txt"))
airports_data=open(os.path.join(file_root,"airports.txt"))
##### Read the data file.########
airport_headers=["Id","Name","City","Country","IATA","ICAO","Longitude","Latitude","U"]
route_headers="AirlineID FlightID SRC_ID CODE DEST_ID CODE YES STOPS U".split()

#1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U"
#2B,410,AER,2965,ASF,2966,,0,CR2

Airports=dict()
Graph=dict()
ID=0
Outdeg=dict()
AirportNames=dict()

for line in airports_data:
    info=line.split(',')[1:5]
    node=info[3].strip('""')
    name=info[0].strip('""')
    if not node=='':
        Airports.__setitem__(node,ID)
        AirportNames.__setitem__(ID,name)
        #print node
        Graph.setdefault(ID)
        Outdeg[ID]=0
        ID=ID+1

for line in routes_data:
    seg=line.split(',')[2:5]
    src=seg[0]
    dst=seg[2]
    try:
        src_id=Airports[src]

        dst_id=Airports[dst]

    except KeyError:
        if Airports.__contains__(src):

            print 'log:source exist:', tuple([src,src_id]),'\n'
        else:
            print 'log: Source  is not a recognized Airport\n'

        if Airports.__contains__(dst):

            print 'log:destination exist:', tuple([dst,dst_id]),'\n'
        else:
            print 'log: destination  is not a recognized Airport\n'
        continue
    #print tuple([src_id,src]), tuple([dst,dst_id]),'\n'
    Outdeg[src_id]+=1
    if Graph[dst_id] is None:

        newitem=dict()
        newitem.__setitem__(src_id,1)
        Graph[dst_id]=newitem


    else:
        if Graph[dst_id].__contains__(src_id):
            w=Graph[dst_id][src_id]
            Graph[dst_id][src_id]=w+1

        else:
            Graph[dst_id][src_id]=1


def save_object(obj,filename):
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','wb') as ObjFile:
        pickle.dump(obj,ObjFile,protocol=2)
def load_object(filename):
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','rb') as ObjFile:
        return pickle.load(ObjFile)



if __name__ == '__main__':
    #print len(Graph)
    #print Graph
    save_object(Graph,"Graph")
    save_object(Airports,"Airports")
    save_object(AirportNames,"AirportName")
    save_object(Outdeg,"Outdeg")
    #print load_object("Outdeg")

    #print len(Airports)
    #print Airports







