### Returns a list of all squarefree integers in a given range. This algorithm is essentially a sieve,
### and it is quite fast.


def squarefree(a,b):


    s = set([i for i in range(2,b+1)])

    ### Remove all multiples of squares
    for i in range(2,round(b**0.5) + 2):
    
        j = i*i

        while j <= b:

            if j in s: s.remove(j)
            j += i*i

    ### Return squarefree integers in desired range

    t=[]
    i = a
    while i <=b:
        if i in s: t.append(i)
        i += 1


    return t