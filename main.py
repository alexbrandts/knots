from dtcode import dtcode
from matrixToWord import *
from buildMatrices import *
from queryCalculators import *
from squarefree import *
from transitions import *
from math import log
import sys
from time import time

times = [time(),0,0,0]

if len(sys.argv) > 3: f = open(sys.argv[3],'w')
else: f = open('C:/snappyinput.txt','w')

a,b = int(sys.argv[1]), int(sys.argv[2])

fields = squarefree(a,b) 

for i in fields:

    print(i)

    t = time()
    temp = queryCalculators(i) 
    times[1] += time() - t
 
    d,x,y,norm,cgroup,cnum = temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]
    
    reg = round(abs(log(x+y*(d**0.5))),2)

    matrices = buildMatrices(d,x,y,norm,cgroup)

    t = time()
    words = [xyWord(cycRed(makeSVWord(matrixToSTtWord(m)))) for m in matrices]
    times[3] += time() - t

    trans = transitions(words)

    lens = [len(w) for w in words]

    t = time()
    dt = dtcode(words)   
    times[2] += time() - t

    f.write(str([i,d,cnum,str(x),str(y),norm,reg,words,lens,trans,dt[0],dt[1]])+'\n') 
   
f.close()

print('\nTotal fields:',len(fields))
print('Total time:', round(time() - times[0],3), 'seconds\n')
print('Average query time:', round(times[1]/len(fields),3), 'seconds')
print('Average dtcode time:', round(times[2]/len(fields),3), 'seconds')
print('Average word time:', round(times[3]/len(fields),3), 'seconds')
print('Average other time:', round((time()-times[0] - sum(times[1:]))/len(fields),3), 'seconds')