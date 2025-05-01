from math import log2, ceil

def int_to_bin_list(i: int):
    return list(reversed(list(map(lambda x:int(x),str(bin(i))[2:]))))

def single_error_hamming_validation(s: str):
    l = list(map(lambda x:int(x), s))
    b = ceil(log2(len(l)))
    e = [0 for _ in range(b)] # Expected parity bits. If the parity was to be set on even (1 = even, 0 = edd), we'd prefill with 1s instead
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
    if sum(d):
        if x > len(l):
            l += [0] * (x - len(l))
        l[x-1] = l[x-1] ^ 1
    return "".join(map(lambda x:str(x),l))


def single_error_hamming_validation_verbose(s: str, even_parity = False):
    # convert to binary list
    l = list(map(lambda x:int(x), s))
    # num parity bits
    b = ceil(log2(len(l)))
    print("Num parity bits:",b)
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
        print(single_error_hamming_validation_verbose("".join(list(filter(lambda x:x!=" ", s))), parity))
