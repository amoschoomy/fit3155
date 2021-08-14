import random
import string
from modkmp import kmp_mod
def naive_test(string, pat):
    out = []
    for i in range(len(string)-len(pat)+1):
        if string[i:i+len(pat)] == pat:
            out.append(i)
    return out

def test_algo(algo_name, times, max_str_len, charset):
    random.seed()
    modified_cs = charset*(0--max_str_len//len(charset)*2)
    for i in range(times):
        str_len = random.randint(1,max_str_len)
        pat_len = random.randint(1,5)
        
        str1 = "".join(random.sample(modified_cs, str_len))
        pat1 = "".join(random.sample(modified_cs, pat_len))
        naive_sol = naive_test(str1, pat1)
        your_sol = algo_name(pat1, str1)
        if naive_sol != your_sol:
            print("Solutions does not match")
            print("String: "+str1)
            print("Pattern: "+pat1)
            print(f"Correct solution: {naive_sol}")
            print(f"Your solution: {your_sol}")
            print(i)
            return

    print("All test passed")

test_algo(kmp_mod, 100000, 100, string.ascii_lowercase[:6])
