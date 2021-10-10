import sys

def fibonacci(max_val):
    fl=[1,2]
    i=2
    while fl[-1]<=max_val:
        fl.append(fl[i-1]+fl[i-2])
        i+=1
    return fl

def fib_encode(max_n):
    fl=[1,2]
    k=2
    for i in range(1,max_n+1):
        while fl[-1]<=i:
            fl.append(fl[k-1]+fl[k-2])
            k+=1
        encode=["0"]*len(fl)
        encode[-1]="1"
        encode[-2]="1"
        curr_max=i-fl[-2]
        for j in range(len(fl)-3,-1,-1):
            if curr_max-fl[j]>=0:
                encode[j]="1"
                curr_max-=fl[j]
                j+=1 #skip no conescutive 1    
        print(i,"".join(encode))



if __name__=="__main__":
    max_n=int(sys.argv[1])
    fib_encode(max_n)
