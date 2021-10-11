def fibonacci(max_val):
    fl=[1,2]
    i=2
    while fl[-1]<=max_val:
        fl.append(fl[i-1]+fl[i-2])
        i+=1
    return fl

def fib_encode(n):
    fl=fibonacci(n)
    encoding=["0"]*len(fl)
    encoding[-1]="1"
    encoding[-2]="1"
    curr_max=n-fl[-2]
    for i in range(len(fl)-3,-1,-1):
        if curr_max-fl[i]>=0:
            encoding[i]="1"
            curr_max-=fl[i]
            i-=1
    return "".join(encoding)
