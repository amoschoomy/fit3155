from bitarray import bitarray
import sys

def retrieve_bitstring(bin_file):
    with open(bin_file,"rb") as f:
        x=bitarray()
        bitarray.fromfile(x,f)
    return x



if __name__=="__main__":
    bf=sys.argv[1]
    retrieve_bitstring(bf)