
def fib_encode(n,fl):

    """
    Given n and fibonacci list
    encode it

    precomputed fibonacci list is passed into
    """

    while fl[-1]<=n: #not reached the value, keep computing fibonacci number, since list is by reference, it will also update outside
        fl.append(fl[-1]+fl[-2])

    #Rest of the code similar as q2 fibonacciencode.py
    encoding=["0"]*len(fl)
    encoding[-1]="1"
    encoding[-2]="1"
    curr_max=n-fl[-2]
    for i in range(len(fl)-3,-1,-1):
        if curr_max-fl[i]>=0:
            encoding[i]="1"
            curr_max-=fl[i]
            if curr_max==0:
                break
            i-=1
    return "".join(encoding)


def fib_decode(bits,ptr,fl:list):
    """
    given bitarray, ptr to the bitarray
    and the pre computed fibonacci
    decode fibencode
    
    """
    val=0
    fb_ptr=0
    one_found=False
    for i in range(ptr,len(bits)):
        if bits[i]==1 and one_found: #if consecutive ones, means end of fib encoding
            ptr=i+1
            break

        elif bits[i]==1:

            val+=fl[fb_ptr] #add to the val
            one_found=True
        else:
            one_found=False

        fb_ptr+=1
        if fb_ptr>=len(fl): #not enough add more fib numbers
            fl.append(fl[-1]+fl[-2])
    return val,ptr