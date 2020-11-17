### Takes as input the class group, the discriminant d, a fundamental unit, and the norm of the fundamental unit.
### The fundamental unit is x + y*root(d). We store x and y. Matrices are stored as [a,b,c,d]. If the norm is 1, 
### we must consider both matrices [a,b,c,d] and [a,-b,-c,d]. Therefore we have twice as many words when the norm 
### is 1. With norm -1, [a,b,c,d] and [a,-b,-c,d] will yield the same word up to cyclic permutation.


from mpmath import mpf, mp
mp.dps = 1000

def buildMatrices(d,x,y,norm,classGroup):
    
    matrices = []

    if norm == -1: x,y = x*x + d*y*y, 2*x*y

    for g in classGroup:

        a,b,c = g[0],g[1],g[2]

        m = [x+b*y, 2*c*y, -2*a*y, x-b*y]

        for i in range(0,4):

            err = abs(m[i] - mpf(str(int(m[i]))))
            if err > 0.01: 
                print("WARNING: Dangerous rounding in buildMatrices. Rounded by",err, "in entry", i)

            m[i]=mpf(str(int(m[i])))

        matrices.append(m)

        ### If the norm is 1, we must also consider matrices with opposite signs on off-diagonal entries              
        if norm == 1: matrices.append([m[0],-m[1],-m[2],m[3]])
    
    return matrices