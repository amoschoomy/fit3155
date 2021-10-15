import sys


"""
Amos Choo Jia Shern
31164998

"""

def fib_encode(max_n):
    """
    Given max_n, generate fib code from 1-> max n
    
    """
    fl=[1,2]
    k=2
    for i in range(1,max_n+1):


        while fl[-1]<=i:
            fl.append(fl[k-1]+fl[k-2]) #generate fibonacci numbers if not available
            k+=1

        encode=["0"]*len(fl)
        encode[-1]="1"
        encode[-2]="1"
        curr_max=i-fl[-2]

        for j in range(len(fl)-3,-1,-1):
            if curr_max-fl[j]>=0: #check for which fib bit activate
                encode[j]="1"
                curr_max-=fl[j]
                if curr_max==0: #done substracting stop
                    break
                j-=1 #skip no conescutive 1    
        print(i,"".join(encode)) 



if __name__=="__main__":
    max_n=int(sys.argv[1])
    fib_encode(max_n)
