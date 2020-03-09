"""
Contains all functions used to implement grover's algorithm
"""

import operations as op
import state as st
import quantum_states as qs
import numpy as np

def Oracle(nq, s):
    """ Returns the oracle gate for mode s, with # of qubits nq """
    Tr = bin(s)[2:].zfill(nq)
    Neg = ""       #Stores the code for the Left and Rightmost layers (i.e. for |0> we get all 'XX')
    for i in Tr:
        if i == '0':
            Neg+="X"
        else:
            Neg+="I"
    L = op.constructGate(Neg)   #Constructs the matrices representing the leftmost and rightmost operations
    Z = op.constructGate(f"{nq}Z")  #Constructs the nq-dimansional CNOT gate (middle layer)
    return op.matrixProduct(op.matrixProduct(L, Z), L)


def Hadamard(nq):
    """Constructs the Hadamard gate (that is to be applied to all qubits)"""
    H = op.constructGate('H'*nq)
    return H


def Diffuser(nq):
    L = op.constructGate("X"*nq)   #Constructs the matrices representing the leftmost and rightmost operations
    Z = op.constructGate(f"{nq}Z")  #Constructs the nq-dimansional CNOT gate (middle layer)
    return op.matrixProduct(op.matrixProduct(L,Z), L)


""" ----------------------------Tests for Grover's and Quantum Error---------------------------"""
s = int(input('\n' + "which state are you looking for?: "))
nq = int(input("number of qubits: "))

print('\n'+"Making gates" + '\n')

print("Making Hadamard")
H = Hadamard(nq)
print("Making Oracle")
Orac = Oracle(nq, s)
print("Making Diffuser" + '\n')
Diff = Diffuser(nq)

print("Initialising State" + '\n')
S = st.state(qs.Register((0,nq)))
S.applyGate(H)
print(S)

it = 4*int(round(np.pi/(4*np.arcsin(1/np.sqrt(nq)))))
print('\n'+ f"Running Grover's, {it} times:")
for i in range(it):
    S.applyGate(Orac)
    S.applyGate(H)
    S.applyGate(Diff)
    S.applyGate(H)
    print('\n' + f"State after iteration no. {i+1}")
    print(S)

Obs = []
States = [f"|{bin(i)[2:].zfill(nq)}>" for i in range(2**nq)]
freq = []

n = 10000
for i in range(n):
    Obs.append(S.observe())

for s in States:
    freq.append(Obs.count(s))

print(f"# of Occurances of each state after observing the system {n} times:")
for i in range(len(freq)):
    print(f"{States[i]}: {freq[i]}")



"""
##___________________________________Demonstration______________________________##
s = int(input("which state are you looking for?: "))
nq = int(input("number of qubits: "))

#Make gates
H = Hadamard(nq)
Orac = Oracle(nq, s)
Diff = Diffuser(nq)

#Show them for the eyes of the world
print("Hadamard: ")
print(H)
print("Oracle: ")
print(Orac)

#Make state and apply gates
S = st.state(qs.Register((0,nq)))
S.applyGate(H)
print(f"Starting with state {qs.Register((0,nq))} and applying Hadamard's gate to all qubits once we obtain: ")
print(S)

print(f"Then as specified we are looking for state {qs.Register((s,nq))}. After applying the Oracle we have: ")
S.applyGate(Orac)
print(S)
"""
