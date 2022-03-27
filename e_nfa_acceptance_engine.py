def acceptance(state, i):
    if (i==len(input)) and (state in F):
        exit("VALID INPUT")
    elif i==len(input):
        return
    for x in states:
        if ((state, x) in transitions):
            for cost in transitions[(state, x)]:
                if cost==input[i]:
                    acceptance(x, i+1)
                elif cost=='*':
                    acceptance(x, i)
import sys
f=open(sys.argv[1], 'r')
states=[]
alphabet=[]
S=0
F=[]
transitions={}
while line:=f.readline():   #cat timp mai sunt linii de citit
    if "Sigma" in line:    #daca pe linie e Sigma atunci incepe citirea alfabetului
        while "End" not in (line:=f.readline()):
            alphabet.append(line.split('letter')[1].split('\n')[0])
    elif "States" in line:    #daca pe linie e States atunci incepe citirea starilor
        while "End" not in (line:=f.readline()):
            if ("S" in line) and ("F" in line):    #trateaza cazul cand pe linie e si S si F
                S=line.split('state')[1].split(' ,S ,F')[0]
                F.append(S)
                states.append(S)
            elif "S" in line:   #trateaza cazul cand starea e cea initiala
                S=line.split('state')[1].split(' ,S')[0]
                states.append(S)
            elif "F" in line:   #trateaza cazul cand starea e finala
                F.append(line.split('state')[1].split(' ,F')[0])
                states.append(F[len(F)-1])
            else:
                states.append(line.split('state')[1].split('\n')[0])
    elif "Transitions" in line:   #daca pe linie e Transitions, incepe citirea tranzitiilor de la linia urmatoare
        while "End" not in (line:=f.readline()):    #citim pana dam de End pe linie
            line=line.split(' ,')
            t=[]
            t.append(line[0].split('state')[1])
            t.append(line[1].split('letter')[1])
            t.append(line[2].split('state')[1].split('\n')[0])
            if (t[0], t[2]) in transitions:
                transitions[(t[0], t[2])].append(t[1])    
            else:
                transitions[(t[0], t[2])]=[t[1]]    #pentru formatul din pdf, t[0] si t[2] sunt stari, iar t[1] e litera din alfabet
input=sys.argv[2]
acceptance(S, 0)
exit("INVALID INPUT")