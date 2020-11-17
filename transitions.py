### Calculates the total number of transitions between letters in a word in xy.

def transitions(words):

    transitions = []

    for w in words:

        count,i = 0,1    

        while i % len(w) != 0:

            if w[i] != w[i-1]: count += 1

            i += 1

        if w[-1] != w[0]: count += 1

        transitions.append(count)

    return transitions