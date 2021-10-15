import sys
from string import ascii_lowercase

"""
Amos Choo Jia Shern
31164998

"""

def generate_all_strings(a:int,length:int):
    """
    Recursive generate all string

    """
    words=[] 
    n=0
    s=""
    aux_gen(a,length,n,s,words)
    return words


def aux_gen(a,length,n,s:str,words):
    if n==length:
        words.append(s)
        return
    for i in range(a):
        new_s=s+ascii_lowercase[i]
        aux_gen(a,length,n+1,new_s,words)

def cycles(s:str):
    """
    Brute force generate cyclic rotations
    
    """
    n=len(s)
    cr=set() #hash table for simpler code
    new_s=""
    for i in range(n):
        for k in range(i,n):
            new_s+=s[k]
        for j in range(i):
            new_s+=s[j]
        cr.add(new_s)   
        new_s=""
    return cr

def solution(all_strings,a,p):
    n_times=0
    for j in all_strings:
        if len(cycles(j))==p: # p distinct cycles
            n_times+=1
    two=pow(a,p)-a # a times of 1 distinct rotation so 2 distinct rotations == pow(a,p)-a
    if two%p:
        boolean="false"
    else:
        boolean="true"
    print(two,n_times,a,boolean) 
    


if __name__=="__main__":
    a,p=int(sys.argv[1]),int(sys.argv[2])
    x=generate_all_strings(a,p)
    solution(x,a,p)


