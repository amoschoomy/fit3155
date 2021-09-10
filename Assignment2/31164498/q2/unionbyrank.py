
from typing import List


def init_set(n:int):
    parent=[-1]*n
    return parent

def find(a:int,parent:List[int]):
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



