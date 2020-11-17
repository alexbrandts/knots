
### Function definitions for creating an xy word from a matrix in SL2Z. All known bugs have been fixed.
### No unknown bugs have been fixed.

from mpmath import mpf, mp
mp.dps = 1000


def leftS(m): return [-m[2], -m[3], m[0], m[1]]

def leftT(m,n): return [m[0] + n*m[2], m[1] + n*m[3], m[2], m[3]]
    
def appendS(word):

    l = len(word)
    if l == 0 or word[l-1] != 'S': word += 'S'
    else: word = word[:-1]
    return word

def appendV(word):

    l = len(word)
    if l <= 1 or word[l-1] != 'V' or word[l-2] != 'V': word += 'V'
    else: word = word[:-2]
    return word

##################SL2Z_reduction()############

def matrixToSTtWord(m): ### Input: matrix of mpfs


    STtWord=[]
 
    if abs(m[2]) > abs(m[0]): 
        m = leftS(m)
        STtWord += 'S'

    while m[2] != 0:

        q = (int) (m[0]/m[2]) 
        m = leftT(m,-q)

        if q > 0: 
            for i in range(0,q): STtWord += 'T'
        elif q < 0: 
            for i in range(0,-q): STtWord += 't'
        else: print("ERROR")

        m = leftS(m)
        STtWord += 'S'

    ### Now either a==d==1 or a==d==-1


    err = m[0]*m[1] - mpf(str(round(m[0]*m[1])))
    if err > 0.01: print("WARNING: Dangerous rounding in matrixToWord. Rounded by ", err)

    q = int(m[0]*m[1])

    if q > 0: 
        for i in range(0,q): STtWord += 'T'
    elif q < 0: 
        for i in range(0,-q): STtWord += 't'

    return STtWord


#########End of SL2Z_redution()#################################
### Now we make a word in S and V

def makeSVWord(STtWord):

    SVWord=[]
    for c in STtWord:

        if c == 'S': SVWord = appendS(SVWord)
        elif c == 'T':
            SVWord = appendS(SVWord)
            SVWord = appendV(SVWord)
        elif c == 't':
            SVWord = appendV(SVWord)
            SVWord = appendV(SVWord)
            SVWord = appendS(SVWord)
    
    return SVWord


### Now we cyclically reduce the SV word ###########


def cycRed(w):

    i,j,lenprev = 0,len(w)-1,0

    while i-j != lenprev and i < len(w):
        
        ir,jl,lenprev = 0,0,i-j

        
        while ir < j-i+1 and w[i+ir] == w[i]: ir += 1
        while j-jl > i+ir and w[j-jl] == w[j]: jl += 1  ## something weird here
        if w[i] == w[j]:
            if w[i] == 'S':
                if (ir + jl) % 2 == 0: i,j = i+ir,j-jl
                else: i,j = i+ir-1,j-jl

            else:
                total = ir + jl
                if total > 2:
                    keep = total % 3
                    if keep == 0: i,j = i+ir,j-jl
                    else:
                        removed = 0
                        while removed < total - keep and w[i] == 'V':
                            i += 1
                            removed += 1
                        j -= total - keep - removed

        elif w[i] == 'S' and w[j] == 'V': i,j = i+ir - ir%2, j-jl + jl%3

        else: i,j = i+ir - ir%3, j-jl + jl%2
  
    w = w[i:j+1]

    if 'S' in w: i = w.index('S')
    else: i = 0

    return w[i:]+w[:i]



### Now we make an xy word from the cyclically reduced SV word ######

def xyWord(SVWord):

    xyWord,l = [],len(SVWord)

    if l == 0 or SVWord[0] != 'S': return []

    ### Loop invariant: SVWord[i] = 'S'
    ### i+1 != l since the word cannot begin and end with 'S'
    ### SVWord[i+1] = 'V' since we can't have 'SS'

    i = 0
    while i < l:
        i+=2

        ### Seeing 'SV'
        if i == l or SVWord[i] == 'S': xyWord += 'x' 


        ### Seeing 'SVV'
        else: 
            xyWord += 'y'
            i+=1

    return ''.join(xyWord)