
### Algorithm to give the Dowker-Thistlethwaite code for a link. The link involves a trefoil knot 
### and any number of knots on the Lorenz template. The knots on the Lorenz template are specified
### by a set of words generated by <x,y>. We use the convention that an even under-crossing is 
### assigned a negative value.

import sys
import os
from functools import cmp_to_key


### This method generates all cyclic permutations of a string
def permute(string):
    l= []
    l.append(string)
    string1 = ''
    for i in range(0,len(string)-1,1):
        string1 = string[1:len(string)] + string[:1]
        l.append(string1)
        string = string1
    return l


### This method compares words using O(1) space. It is much better than its previous version, which used
### O(lcm(length of all words)) space.
def comp(s,t):

    ### Strip off the index from the words
    s,t = s[0],t[0]

    i = 0
    
    while s[i % len(s)] == t[i % len(t)]: i += 1

    ### Post condition: s[i] != t[i]

    if s[i % len(s)] > t[i % len(t)]: return 1
    else: return -1

############################## Dtcode Algorithm #################################################


def dtcode(strings):

    numx = sum([s.count('x') for s in strings])

    permutations = [permute(s) for s in strings]
  
    ### Attach to each permutation the number of the word it came from
    indexedPermutations=[]
    for i in range(0,len(permutations)):
        temp=[]
        for j in range (0,len(permutations[i])): temp.append([permutations[i][j], i])
        indexedPermutations.append(temp)


    ### Merge all permutations into a single list
    allPermutations = [p for x in indexedPermutations for p in x]

    #print(allPermutations)
    #print()

    ### Sort list of all permutations with our custom sorting key
    sortedPermutations = sorted(allPermutations, key=cmp_to_key(comp))

    #t=sortedPermutations[6]
    #sortedPermutations[6] = sortedPermutations[7]
    #sortedPermutations[7] = t

    #print(sortedPermutations)
    #print()

    ### Declare empty matrix
    nodelist=[[None for i in range(0)] for j in range(len(strings))]


    ### Extract index of each permutation in sorted list and store in a new list. These numbers represent nodes
    ### on the branch line.
    for p in allPermutations: 
        nodelist[p[1]].append(sortedPermutations.index(p)+1)

    #print(nodelist)


    ### Rearrange list so that the smallest node is first. This is not necessary, but it makes the algorithm
    ### easier to follow.
    for i in range(0,len(nodelist)):
        m = min(nodelist[i])
        j = nodelist[i].index(m)
        nodelist[i] = nodelist[i][j:] + nodelist[i][:j]

    nodelist = sorted(nodelist)

    ### Declare empty matrix
    segments = [[None for i in range(0)] for j in range(len(strings))]


    ### Divide nodelist into individual segments, ie paths connecting pairs of nodes on the branch line.
    for i in range(0,len(nodelist)):
        for j in range(0, len(nodelist[i])-1):
            segments[i].append([nodelist[i][j],nodelist[i][j+1]])
        segments[i].append([nodelist[i][len(nodelist[i])-1],nodelist[i][0]])

    xx,xy,yx,yy = [],[],[],[]

    ### Sort segments according to start/destination
    for segmentGroup in segments:
        for s in segmentGroup:
            if s[0] <= numx:
                if s[1] <= numx: 
                    xx.append(s)

                else: xy.append(s)
            else:
                if s[1] <= numx: yx.append(s)
                else: yy.append(s)

    ### We sort each class of segments in lexicographical order (and subsequently reverse lexicographical 
    ### order). Segments are sorted by the node they start at. Note that sorting by the end-node of the
    ### segments would produce the same result since for any segments s and t in the same class, s has a 
    ### bigger start point than t if and only if s has a bigger end point than t.

    xx = sorted(xx)          
    xy = sorted(xy) 
    yx = sorted(yx) 
    yy = sorted(yy)

    ### Reverse order
    xxr = sorted(xx, reverse=True)          
    xyr = sorted(xy, reverse=True) 
    yxr = sorted(yx, reverse=True) 
    yyr = sorted(yy, reverse=True)
    

    ###########################################################################
    ### Now we enter the main phase of the algorithm, where we document all the crossings that occur. We begin
    ### by traversing the trefoil. We do the trefoil first because it makes it easier to switch link components
    ### with respect to parity. An object of type crossing looks like this: [number, [start,dest], [start,dest]].
    ### Number is a signed integer, the first [start, dest] pair is the path we are traveling along, and the
    ### second [start, dest] pair is the path we are crossing. We start our trefoil journey at the point where 
    ### [1,_] meets the trefoil for the second time. This happens in the upper left part of the trefoil, above the
    ### hole on the x side.
    ###
    ### The collection of crossings is implemented with a dictionary. This allows a crossing [_,[s1,t1],[s2,t2]] to
    ### be matched with [_,[s2,t2],[s1,t1]] in O(1) time later on. The key for a crossing [_,[s1,t1],[s2,t2]] is
    ### str([s2,t2])+str([s1,t1]).

    crossings={}

    ### numCrossings keeps track of the number of crossings in each link component
    numCrossings=[]

    ### Crossings of upper left trefoil. Segments with smaller endpoints are crossed first. The trefoil crosses
    ### over all these segments, so we don't worry about negative signs.
    for s in xx: crossings[str(s)+str(['T','UL'])] = [len(crossings)+1,['T','UL'],s]
    for s in xy: crossings[str(s)+str(['T','UL'])] = [len(crossings)+1,['T','UL'],s]

    ### First set of 3 crossings of the trefoil with itself. The codes [X1,X1],[Y1,Y1], etc are arbitrarily
    ### named and are used to match pairs of crossings.
    crossings[str(['Y1','Y1'])+str(['X1','X1'])] =[pow(-1,len(crossings))*(len(crossings)+1),['X1','X1'],['Y1','Y1']]
    crossings[str(['Y2','Y2'])+str(['X2','X2'])] =[len(crossings)+1,['X2','X2'],['Y2','Y2']]
    crossings[str(['Y3','Y3'])+str(['X3','X3'])] =[pow(-1,len(crossings))*(len(crossings)+1),['X3','X3'],['Y3','Y3']]

    ### Crossings of lower right trefoil. Segments with smaller endpoints are crossed first. The trefoil crosses 
    ### under every segment here. 
    for s in yx: crossings[str(s)+str(['T','LR'])] = [pow(-1,len(crossings))*(len(crossings)+1),['T','LR'],s]
    for s in yy: crossings[str(s)+str(['T','LR'])] = [pow(-1,len(crossings))*(len(crossings)+1),['T','LR'],s]

    ### Crossings of upper right trefoil. Segments with larger endpoints are crossed first. The trefoil crosses
    ### over every segment here.
    for s in yyr: crossings[str(s)+str(['T','UR'])] = [len(crossings)+1,['T','UR'],s]
    for s in yxr: crossings[str(s)+str(['T','UR'])] = [len(crossings)+1,['T','UR'],s]

    ### Second set of 3 crossings of the trefoil with itself.
    crossings[str(['X1','X1'])+str(['Y1','Y1'])] = [len(crossings)+1,['Y1','Y1'],['X1','X1']]
    crossings[str(['X2','X2'])+str(['Y2','Y2'])] = [pow(-1,len(crossings))*(len(crossings)+1),['Y2','Y2'],['X2','X2']]
    crossings[str(['X3','X3'])+str(['Y3','Y3'])] = [len(crossings)+1,['Y3','Y3'],['X3','X3']]

    ### Crossings of lower left trefoil. Segments with larger endpoints are crossed first. The trefoil crosses
    ### under every segment here.
    for s in xyr: crossings[str(s)+str(['T','LL'])] = [pow(-1,len(crossings))*(len(crossings)+1),['T','LL'],s]
    for s in xxr: crossings[str(s)+str(['T','LL'])] = [pow(-1,len(crossings))*(len(crossings)+1),['T','LL'],s]

    numCrossings.append(len(crossings))


    ##############################################################################
    ### Now we must traverse the knots on the template one by one. We start with the knot with the leftmost endpoint.
    ### First we extact the value of the first crossing of the knot with the upper left trefoil, say n. We assume all 
    ### words contain at least one x, so this always happens. Our next crossing will be assigned an even number. If n
    ### is odd, we can start our knot traversal here. Otherwise, we start our traversal at the first crossing of the
    ### knot with the LOWER left trefoil. This crossing will always have opposite parity to n.

    for segmentGroup in segments:

        ### Find crossing number of the first segment with upper left trefoil
        firstCrossing = crossings[str(segmentGroup[0])+str(['T','UL'])][0]

        for s in segmentGroup:
            if s in xx or s in xy: 

                ### When we are traversing the first segment, we start at the lower left trefoil if the upper left
                ### trefoil is marked with an odd number. Otherwise we skip this crossing and add it on at the end.
                if s == segmentGroup[0]:
                    if firstCrossing % 2 == 1: crossings[str(['T','LL'])+str(s)] = [len(crossings)+1,s,['T','LL']]
                else: crossings[str(['T','LL'])+str(s)] = [len(crossings)+1,s,['T','LL']]

                ### We always cross the upper left trefoil
                crossings[str(['T','UL'])+str(s)] = [pow(-1,len(crossings))*(len(crossings)+1),s,['T','UL']]
    
                if s in xx:
                    for t in yx: ### Segments with smaller endpoints are crossed first
                        if t[1] < s[1]: crossings[str(t)+str(s)] = [len(crossings)+1,s,t]

                elif s in xy:
                    for t in yx: crossings[str(t)+str(s)] = [len(crossings)+1,s,t]
                    for t in yy:
                        if t[1] < s[1]: crossings[str(t)+str(s)] = [len(crossings)+1,s,t]

            elif s in yx or s in yy:
        
                ### Trefoil crossings
                crossings[str(['T','LR'])+str(s)] = [len(crossings)+1,s,['T','LR']]
                crossings[str(['T','UR'])+str(s)] = [pow(-1,len(crossings))*(len(crossings)+1),s,['T','UR']]
        
                if s in yx:
                    for t in xyr: crossings[str(t)+str(s)] = [pow(-1,len(crossings))*(len(crossings)+1),s,t] 
                    for t in xxr:                                                                  
                        if s[1] < t[1]: crossings[str(t)+str(s)] = [pow(-1,len(crossings))*(len(crossings)+1),s,t]
        
                elif s in yy:
                    for t in xyr:
                        if s[1] < t[1]: crossings[str(t)+str(s)] = [pow(-1,len(crossings))*(len(crossings)+1),s,t]
        
            else: print("ERROR: UNCLASSIFIED SEGMENT")

        if firstCrossing % 2 == 0: 
            crossings[str(['T','LL'])+str(segmentGroup[0])] = [len(crossings)+1,segmentGroup[0],['T','LL']]

        numCrossings.append(len(crossings))

    ############################################################################
    ### At this point we have traversed all crossings in the link twice. We must now cut our list of crossings
    ### in half to obtain the DT code. To do this, we match crossings [_,A,B] and [_,B,A]. Then we extract the
    ### odd and even numbers corresponding to each pair. We store the even number in a list at an index 
    ### determined by the odd number. If n is the odd number, the corresponding even number will be stored at
    ### index (n-1)/2. The length of the DT code will be precisely half that of the list of crossings.

    lencross = int(len(crossings)/2)

    ### Declares an empty array of the appropriate size
    dtcode = [''] * lencross 

    ### We loop through the dictionary of crossings, removing pairs of crossings as they are matched.
    while crossings != {}:
    
        a = crossings.popitem()
        akey = str(a[1][2])+str(a[1][1])
        bkey = str(a[1][1])+str(a[1][2])
        b = [bkey,crossings[bkey]]

        if str(b[1][1])+str(b[1][2]) != akey or str(b[1][2])+str(b[1][1]) != bkey: print("KEY ERROR")

        if a[1][0] % 2 == 1 and b[1][0] % 2 == 0: dtcode[int((a[1][0]-1)/2)] = b[1][0]
        
        elif a[1][0] % 2 == 0 and b[1][0] % 2 == 1: dtcode[int((b[1][0]-1)/2)] = a[1][0]
        
        else: 
            print("ERROR: PARITY MATCH BETWEEN CROSSINGS ", a[1][0], " AND ", b[1][0])

        crossings.pop(b[0]) ### Remove b from dictionary once it has been matched. Note: a is already removed
  

    ### Now we partition the dtcode into lists corresponding to each link component.
    for i in range(0,len(numCrossings)): numCrossings[i] = numCrossings[i]/2

    dtcode2=[]
    dtcode2.append(dtcode[:int (numCrossings[0])])

    for i in range(1,len(numCrossings)):
        dtcode2.append(dtcode[int(numCrossings[i-1]):int(numCrossings[i])])


    ### Finally, we format the output so that it can be read by snappy. We replace interior square brackets
    ### with round brackets.

    dtcode = str(dtcode2)
    dtcode = dtcode[1:-1]
    dtcode = str(dtcode)
    dtcode = dtcode.replace('[','(')
    dtcode = dtcode.replace(']',')')
    dtcode = '[' + dtcode + ']'

    return [dtcode, lencross]