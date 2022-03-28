from operator import le
from os import stat
import sys
f=open(sys.argv[1], 'r')
nfa_states=[]
alphabet=[]
S=0
nfa_F=[]
nfa_transitions={}
while line:=f.readline():   #cat timp mai sunt linii de citit
    if "Sigma" in line:    #daca pe linie e Sigma atunci incepe citirea alfabetului
        while "End" not in (line:=f.readline()):
            alphabet.append(line.split('letter')[1].split('\n')[0])
    elif "States" in line:    #daca pe linie e States atunci incepe citirea starilor
        while "End" not in (line:=f.readline()):
            if ("S" in line) and ("F" in line):    #trateaza cazul cand pe linie e si S si F
                S=line.split('state')[1].split(' ,S ,F')[0]
                nfa_F.append(S)
                nfa_states.append(S)
            elif "S" in line:   #trateaza cazul cand starea e cea initiala
                S=line.split('state')[1].split(' ,S')[0]
                nfa_states.append(S)
            elif "F" in line:   #trateaza cazul cand starea e finala
                nfa_F.append(line.split('state')[1].split(' ,F')[0])
                nfa_states.append(nfa_F[len(nfa_F)-1])
            else:
                nfa_states.append(line.split('state')[1].split('\n')[0])
    elif "Transitions" in line:   #daca pe linie e Transitions, incepe citirea tranzitiilor de la linia urmatoare
        while "End" not in (line:=f.readline()):    #citim pana dam de End pe linie
            line=line.split(' ,')
            t=[]
            t.append(line[0].split('state')[1])
            t.append(line[1].split('letter')[1])
            t.append(line[2].split('state')[1].split('\n')[0])
            if (t[0], t[1]) in nfa_transitions:
                nfa_transitions[(t[0], t[1])].append(t[2]) 
            else:
                nfa_transitions[(t[0], t[1])]=[t[2]]    #pentru formatul din pdf, t[0] si t[2] sunt stari, iar t[1] e litera din alfabet
print("Sigma:")
for letter in alphabet:
    print("\tletter", letter, sep='')
print("End")
dfa_states=[]
dfa_F=[]
dfa_transitions={}
for letter in alphabet:
    if (S, letter) in nfa_transitions:
        temp=''
        for state in nfa_transitions[(S, letter)]:
            temp=temp+'/'+state
        if temp not in dfa_states:
            dfa_states.append(temp)
            for x in alphabet:
                if (S, x) in nfa_transitions:
                    dfa_transitions[(temp, x)]=''
        dfa_transitions[('/'+S, letter)]=temp
while '' in dfa_transitions.values():
    unfinished={}
    unfinished=unfinished.fromkeys((state, letter)for (state, letter) in dfa_transitions if dfa_transitions[(state, letter)]=='')
    for (state, letter) in unfinished:
        temp=state.split('/')
        del temp[0]
        for x in temp:
            if (x, letter) in nfa_transitions.keys():
                for y in nfa_transitions[(x, letter)]:
                    dfa_transitions[(state, letter)]=dfa_transitions[(state, letter)]+'/'+y
        if dfa_transitions[(state, letter)] not in dfa_states:
            dfa_states.append(dfa_transitions[(state, letter)])
            for x in nfa_F:
                if x in dfa_transitions[(state, letter)]:
                    dfa_F.append(dfa_transitions[(state, letter)])
            for x in alphabet:
                dfa_transitions[(dfa_transitions[(state, letter)], x)]=''
table={}
nr=0
for state in dfa_states:
    table[state]='q'+str(nr)
    nr=nr+1
print("States:")
for state in dfa_states:
    print("\tstate", table[state], sep='', end='')
    if state.split('/')[1]==S and len(state.split('/'))==2:
        print(" ,S", end='')
    if state in dfa_F:
        print(" ,F", end='')
    print()
print("End")
print("Transitions:")
for (state, letter) in dfa_transitions:
    print("\tstate", table[state], " ,letter", letter, " ,state", table[dfa_transitions[(state, letter)]], sep='')
print("End")