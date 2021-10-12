from bitarray import bitarray
import sys
from fibonaccicodeq3 import fib_decode

def retrieve_bitstring(bin_file):
    with open(bin_file,"rb") as f:
        x=bitarray()
        bitarray.fromfile(x,f)
    return x

def decode_bit(barray):
    bit_ptr=0
    fl=[1,2]
    bwt_length,bit_ptr=fib_decode(barray,bit_ptr,fl)
    uniq_char,bit_ptr=fib_decode(barray,bit_ptr,fl)
    





if __name__=="__main__":
    bf=sys.argv[1]
    x=retrieve_bitstring(bf)
    for i in range(len(x)):
        print(x[i])
        # if i=="1":
        #     print("True")
        # elif i=="0":
        #     print("False")
        # elif i==1:
        #     print("intger")
        # elif i==0:
        #     print("o iteger")
        # else:
        #     print("FUCK")