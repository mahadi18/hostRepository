############################# Main file#############
# Author: Bishnu Sarker, UPMC, UPB Email: bishnukuet@gmail.com
# Description: This is actually main file to compute and print  Ranking. This the prerequisites data are
# computed with drawflight.py beforehand and saved in .pkl files. There fore it is enough to run this only
# if you already have .pkl files
##############################################################

import pickle
import os
import time
import numpy as np

#### Global variable declaration
Graph=dict()
dangling_nodes=list()


def save_object(obj,filename):
    '''
    this is a special function to save a python object into secondary Disk as a binary file
    :param obj: python object to be saved
    :param filename: .pkl filename to be saved
    :return: nothing
    '''
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','wb') as ObjFile:
        pickle.dump(obj,ObjFile,protocol=2)
def load_object(filename):
    '''
    this is a special function that load the python object into RAM given the filename
    :param filename: .pkl filename from where object to be loaded
    :return: return the saved python object
    '''
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','rb') as ObjFile:
        return pickle.load(ObjFile)


def get_dangling_nodes():
    '''

    :return: returns the list of Dangling Nodes. The nodes that does not have any outgoing links
    '''
    return [item for item in OutDeg.keys() if OutDeg[item]==0]


#print dangling_node
def compute_refs(node,P):
    '''
    this function computes the reference the node gets from other incoming connected links
    :param node: Node for which the rank to be computed
    :param P: Current Probability
    :return: return the total reference it receives from other nodes
    '''
    sum=0
    if Graph[node] is not None:
        for item in Graph[node].keys():
            sum=sum+P[item]*Graph[node][item]/float(OutDeg[item])
                #print OutDeg[item]
    return sum
def handle_dangling_node(NodeSize,P):
    '''

    :param NodeSize: Number of Nodes in the Graph
    :param P: Curent Probability List
    :return: returns the contribution of Dangling nodes to the rank computation for each node
    '''
    dangling_sum=float(0)
    for node in dangling_nodes:
        dangling_sum=dangling_sum+P[node]
    return dangling_sum/float(NodeSize)
def ranking(NodeSize,MaxIter=30,dump_factor=0.8):
    '''
    Main method that computes the ranks
    :param NodeSize: Size of the Graph
    :param MaxIter:Maximum Iteration
    :param dump_factor: Dump Factor
    :return: Return sorted list of index
    '''
    #print dangling_nodes
    P=[float(1)/NodeSize for x in range(NodeSize)]


    #print sum(P)
    iter=0
    constant=(1-dump_factor)/NodeSize

    while iter<MaxIter:
        #print 'Iteration:', iter,'\n'
        Q=[0 for x in range(NodeSize)]
        for node in range(NodeSize):
            Q[node]=dump_factor* (compute_refs(node,P)+handle_dangling_node(NodeSize,P))+constant

        P=Q
        #print P
        #print ' The Ranking Sum is;',sum(P)
        iter+=1
    return np.array(P).argsort(kind='quicksort')

def display_ranking(index,rankfile):
    '''

    :param index: index list
    :param rankfile: Path of the file where the rank, and airport name will be saved
    :return: None
    '''
    #del Graph
    #del OutDeg
    AirportName=load_object("AirportName")
    rank=1
    i=len(index)-1
    with open(rankfile,'w') as out:
        while i>0:
            out.writelines(str(rank)+" "+AirportName[index[i]]+'\n')
            i-=1
            rank+=1

if __name__ == '__main__':
    Graph=load_object("Graph")  #Load the Graph from the Graph.pkl as a Python Dictionary Variable
    OutDeg=load_object("OutDeg") #Load OutDeg Contains  out Degree against node
    #print OutDeg
    Airports=load_object("Airports") # Load Airports IATA code agains ID
    dangling_nodes=get_dangling_nodes() #Compute the Dangling Nodes
    #print Graph
    #print dangling_nodes
    #print 'Number of Dangling Node is:', dangling_nodes.__len__()
    #print 'Dangling Nodes:', dangling_nodes,'\n'
    N=len(Graph)
    #print [key for key in Graph.keys() if Graph[key] is None]


    #print Airports['EGS']
    tr=time.clock()
    f="Rank.txt"
    display_ranking(ranking(N),f)  # Computes the ranking and writes in a file called Rank.txt

    print 'time diference',time.clock()-tr   # Prints the time duration in seconds.