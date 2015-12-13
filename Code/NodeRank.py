import pickle
import os
import time
import numpy as np

#### Global variable declaration
Graph=dict()
dangling_nodes=list()


def save_object(obj,filename):
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','wb') as ObjFile:
        pickle.dump(obj,ObjFile,protocol=2)
def load_object(filename):
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','rb') as ObjFile:
        return pickle.load(ObjFile)


def get_dangling_nodes():
    return [item for item in OutDeg.keys() if OutDeg[item]==0]


#print dangling_node
def compute_refs(node,P):
    sum=0
    if Graph[node] is not None:
        for item in Graph[node].keys():
            sum=sum+P[item]*Graph[node][item]/float(OutDeg[item])
                #print OutDeg[item]
    return sum
def handle_dangling_node(NodeSize,P):
    dangling_sum=float(0)
    for node in dangling_nodes:
        dangling_sum=dangling_sum+P[node]
    return dangling_sum/float(NodeSize)
def ranking(NodeSize,MaxIter=30,dump_factor=0.8):
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
    Graph=load_object("Graph")
    OutDeg=load_object("OutDeg")
    #print OutDeg
    Airports=load_object("Airports")
    dangling_nodes=get_dangling_nodes()
    #print Graph
    #print dangling_nodes
    #print 'Number of Dangling Node is:', dangling_nodes.__len__()
    #print 'Dangling Nodes:', dangling_nodes,'\n'
    N=len(Graph)
    #print [key for key in Graph.keys() if Graph[key] is None]


    #print Airports['EGS']
    tr=time.clock()
    f="Rank.txt"
    display_ranking(ranking(N),f)

    print 'time diference',time.clock()-tr