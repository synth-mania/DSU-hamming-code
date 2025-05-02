from math import log2, ceil, floor

def int_to_bin_list(i: int):
    return list(reversed(list(map(lambda x:int(x),str(bin(i))[2:]))))

def single_error_hamming_validation(s: str, even_parity = False):
    l = list(map(lambda x:int(x), s)) # convert the string to a list of ints
    b = ceil(log2(len(l)+1)) # calculate the number of parity bits present
    e = [{True: 1, False: 0}[even_parity] for _ in range(b)] # Expected parity bits. If the parity was to be set on even (1 = even, 0 = edd), we'd prefill with 1s instead
    r = [l[2**x - 1] for x in range(b)] # real parity bits
    for i in range(len(l)):  # for every list index
        bin_i = int_to_bin_list(i + 1)  # convert index to binary
        if sum(bin_i) == 1:
            continue # skip parity bits
        for j in range(len(bin_i)):
            if bin_i[j]:# for every parity bit that corresponds to this index
                e[j] = e[j] ^ l[i] # flip the expected parity if bit == 1 (bit addition)
    d = [int(r[i]!=e[i]) for i in range(b)] # difference between expected and calculated parity bits
    x = sum(d[i] * 2**(i) for i in range(b)) # converted from binary to an integer is the index of the error (if any)
    if sum(d): # if the sum of errors > 0
        if x > len(l):
            l += [0] * (x - len(l)) # extend in the case that an improperly truncated code needs a bit beyond the end flipped
        l[x-1] = l[x-1] ^ 1 # flip the bit in error
    return "".join(map(lambda x:str(x),l)) # convert the list[int] back to a string


def single_error_hamming_validation_verbose(s: str, even_parity = False):
    # convert to binary list
    l = list(map(lambda x:int(x), s))
    # num parity bits
    b = ceil(log2(len(l)+1))
    print("Num parity bits:",b)
    print(f"This is a Hamming({(2**(floor(log2(len(l))+1))-1)},{(2**(floor(log2(len(l))+1))-1)-(floor(log2(len(l))+1))}) code, with the ", end="")
    if len(l) < (2**(floor(log2(len(l))+1))-1): # if this is not a proper length Hamming code
        print(f"last {(2**(floor(log2(len(l))+1))-1) - len(l)} data bits truncated (assumed set to 0)")
    else:
        print("proper number of data bits.")
    # expected parity bit value (initialized)
    e = [{True: 1, False: 0}[even_parity] for _ in range(b)] # if the parity was to be set on even (1 = even, 0 = odd), we'd prefill with 1s instead
    # real parity bit value
    r = [l[2**x - 1] for x in range(b)]
    print("Parity bit location (0-index):", [2**x - 1 for x in range(b)])
    for i in range(len(l)):  # for every list index
        bin_i = int_to_bin_list(i + 1)  # convert index to binary
        if sum(bin_i) == 1:
            continue # skip parity bits
        # print("checking data bit at index ", i)
        for j in range(len(bin_i)):
            if bin_i[j]:# for every parity bit that corresponds to this index
                e[j] = e[j] ^ l[i] # flip the expected parity if bit == 1 (bit addition)
    d = [int(r[i]!=e[i]) for i in range(b)] # difference between expected and calculated parity bits
    x = sum(d[i] * 2**(i) for i in range(b)) # converted from binary to an integer is the index of the error (if any)

    print("expected parity value: ",e)
    print("real parity value: ",r)
    print("difference: ", d)

    if sum(d):
        print("ERROR in a ", end="")
        if x > len(l):
            l += [0] * (x - len(l))
        l[x-1] = l[x-1] ^ 1
        if sum(d) == 1:
            print("parity bit")
        else:
            print("data bit")
        print("error position (0-index): ",x-1)
        print(f"corrected bit string: {"".join(map(lambda x:str(x),l))}")
    else:
        print("no error")
    
    return "".join(map(lambda x:str(x),l))



if __name__ == "__main__":
    while True:
        parity = not (input("\n(e)ven or (O)dd parity? ") or "o")[0].lower() == "o"
        print({True: "even", False: "odd"}[parity], "parity\n")
        s = input("bitstring: ") or "1000000"
        single_error_hamming_validation_verbose("".join(list(filter(lambda x:x!=" ", s))), parity)
