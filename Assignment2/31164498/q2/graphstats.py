from typing import List, Tuple
from unionbyrank import find,union,init_set

def read_file(graph_file):
    with open(graph_file,"r",encoding="UTF-8") as f:
        lst=[x.rstrip() for x in f]
    return lst


lst=['meads', 'turns', 'burns', 'meats', 'witch', 'means', 
'catch', 'meals', 'snafu', 'burnt', 'meant', 'truck', 'hatch']

def all_hamming_distance(lst):
    lst_of_edges=[]
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i!=j:
                lst_of_edges.append((i,j,hamming_distance(lst[i],lst[j])))
    return lst_of_edges



def kruskal(lst):
    lst.sort(key=lambda x:x[2])
    parent=init_set(len(lst))
    for edge in lst:
        if find(edge[0],parent)!=find(edge[1],parent):
            union(edge[0],edge[1],parent)
    return parent




    



def hamming_distance(string1, string2):
	distance=0
	for i in range(len(string1)):
		if string1[i] != string2[i]:
			distance += 1
	return distance

l=all_hamming_distance(lst)
print(l)
print("\n")
kruskal(l)


# import sys
# graph=sys.argv[1]

# print(read_file(graph))