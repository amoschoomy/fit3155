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

def fib_decode(bits,ptr,fl:list):
    val=0
    fb_ptr=0
    one_found=False
    for i in range(ptr,len(bits)):
        if bits[i]==1 and one_found:
            ptr=i+1
            break
        elif bits[i]==1:

            val+=fl[fb_ptr]
            one_found=True
        else:
            one_found=False
        fb_ptr+=1
        if fb_ptr>=len(fl):
            fl.append(fl[-1]+fl[-2])
    return val,ptr