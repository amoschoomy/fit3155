import sys
from string import ascii_lowercase
def generate_all_strings(a:int,length:int):
    """
    a== how many characters in alphabet
    length= length of generated string from these alphabets

    """
    words=[] #list of words
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

def all_cyclic_no_slice(s:str):
    n=len(s)
    cr=set()
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
        if len(all_cyclic_no_slice(j))==p:
            n_times+=1
    two=pow(a,p)-a
    if two%p:
        boolean="false"
    else:
        boolean="true"
    print(pow(a,p)-a,n_times,a,boolean)
    


if __name__=="__main__":
    a,p=int(sys.argv[1]),int(sys.argv[2])
    x=generate_all_strings(a,p)
    solution(x,a,p)


