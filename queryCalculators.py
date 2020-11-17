### Here we query two online calculators and parse their outputs. If the outputs are too large,
### an error report is stored in error.txt.


import html2text
import requests
from time import sleep
from ast import literal_eval
from mpmath import mpf, mp
mp.dps = 1000


def queryCalculators(i):

    url = "http://www.numbertheory.org/php/classnopos.php"
    url2 = "http://www.numbertheory.org/php/unit.php"

 
    ############## Calculate and parse class group ######################
   
    classGroup = []

    payload = {'M1value':i}

    success = False

    while success == False:

        try:

            r = requests.post(url, params=payload)
            success = True
 
        except requests.exceptions.ConnectionError:

            print("Internet Connection Error. Trying again")
            sleep(1)

    s=html2text.html2text(str(r.content))[40:-97]

    j = 1
    flag = '['+str(j)+']:'

    while flag in s:

        s = s[s.index(flag):]

        c = '[' + s[s.index('(')+1:s.index(')')] + ']'
        
        c = literal_eval(c)

        for k in range(0,3): c[k] = mpf(str(c[k]))

        classGroup.append(c)
        
        j += 1
        flag = '['+str(j)+']:'


    ############## Calculate and parse fundamental unit ################

    payload2 = {'Mvalue':i}


    success = False

    while success == False:

        try:

            q = requests.post(url2,params=payload2)
            success = True
 
        except requests.exceptions.ConnectionError:

            print("Internet Connection Error. Trying again")
            sleep(1)

    s = str(q.content)
    s = s[s.index('omega')+6:s.index('norm')+8]

    if i % 4 == 1:

        if 'x' in s and 'y' in s:
            
            temp = s[s.index('x=')+2:s.index(',')]
            if len(temp) > mp.dps/2 - 10: print("WARNING: potential loss of precision in fundamental unit")
            x = mpf(temp)

            s = s[s.index('x=')+2:]

            temp = s[s.index('y=')+2:s.index('<')]
            if len(temp) > mp.dps/2 - 10: print("WARNING: potential loss of precision in fundamental unit")
            y = mpf(temp)

            x += y/2
            y /= 2

        else: x,y = mpf(str(0.5)),mpf(str(0.5))

    else:

        temp = s[s.index('x=')+2:s.index(',')]
        if len(temp) > mp.dps/2 - 10: print("WARNING: potential loss of precision in fundamental unit")
        x = mpf(temp)

        s = s[s.index('x=')+2:]

        temp = s[s.index('y=')+2:s.index('<')]
        if len(temp) > mp.dps/2 - 10: print("WARNING: potential loss of precision in fundamental unit")
        y = mpf(temp)

        y /= 2 ### TO account for the fact that we are using root d and not root i

    s = s[s.index('norm='):]
    norm = int(s[s.index('norm=')+5:s.index('<')])

    if i % 4 != 1: i *= 4

    if x*x-y*y*i != norm: 

        print("ERROR: corrupt fundamental unit")
        f=open('C:/error.txt','w')
        f.write("The fundamental unit was too big to be stored which resulted in abs(norm) != 1.\n") 
        f.write("The output for the field with discriminant "+str(i)+" is likely garbage.\n")
        f.write("Thank you and have a nice day.")
        f.write("\n\n\nfundamental unit:  "+str(x)+" + "+str(y)+'*'+'root('+str(i)+')')
        f.close()
    
    return [i,x,y,norm,classGroup,len(classGroup)]
    