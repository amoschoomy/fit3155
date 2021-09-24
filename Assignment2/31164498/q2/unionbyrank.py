"""
Name: Amos Choo Jia Shern
ID: 31164498

"""


#Code referenced from Lecture slides week 4 with slight modifcation
def init_set(n):
    parent=[-1]*n
    return parent

def find(a,parent):
    if parent[a]<0:
        return a
    else:
        parent[a]=find(parent[a],parent)
        return parent[a]

def union(a,b,parent):
    root_a=find(a,parent)
    root_b=find(b,parent)
    height_a=-parent[root_a]
    height_b=-parent[root_b]
    if height_a>height_b:
        parent[root_b]=root_a
        return root_a,root_b
    elif height_a<height_b:
        parent[root_a]=root_b
        return root_b,root_a

    else:
        parent[root_a]=root_b
        parent[root_b]=-(height_b+1)
        return root_b,root_a



