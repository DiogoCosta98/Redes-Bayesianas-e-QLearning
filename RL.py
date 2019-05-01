# G 084    86971   Diogo António Da Silva Costa   82374   Luana Ascensão de Jesus Marques

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:31:54 2017

@author: mlopes
"""
import numpy as np
import random

from tempfile import TemporaryFile
outfile = TemporaryFile()
	
class finiteMDP:

    def __init__(self, nS, nA, gamma, P=[], R=[], absorv=[]):
        self.nS = nS
        self.nA = nA
        self.gamma = gamma
        self.Q = np.zeros((self.nS,self.nA))
        self.occurence = np.zeros((self.nS,self.nA,self.nS))
        if len(P) == 0:#
            self.occurence = np.zeros((self.nS,self.nA,self.nS))#
            self.P = np.zeros((self.nS,self.nA,self.nS))
        else:#
            self.P = P
        if len(R) == 0:#
            self.R = np.zeros((self.nS,self.nA))#
        else:#
            self.R = R
        '''lista de nos finais para voltar ao inicio'''
        self.absorv = absorv 
        # completar se necessario
        
            
    def runPolicy(self, n, x0,  poltype = 'greedy', polpar=[]):
        #nao alterar
        traj = np.zeros((n,4))
        x = x0
        J = 0
        for ii in range(0,n):
            a = self.policy(x,poltype,polpar)
            r = self.R[x,a]
            y = np.nonzero(np.random.multinomial( 1, self.P[x,a,:]))[0][0]
            traj[ii,:] = np.array([x, a, y, r])
            J = J + r * self.gamma**ii
            if self.absorv[x]:
                y = x0
            x = y
        
        return J,traj


    def VI(self):
        #nao alterar
        nQ = np.zeros((self.nS,self.nA))
        while True:
            self.V = np.max(self.Q,axis=1)
            for a in range(0,self.nA):
                nQ[:,a] = self.R[:,a] + self.gamma * np.dot(self.P[:,a,:],self.V)
            err = np.linalg.norm(self.Q-nQ)
            self.Q = np.copy(nQ)
            if err<1e-7:
                break
            
        #update policy
        self.V = np.max(self.Q,axis=1) 
        #correct for 2 equal actions
        self.Pol = np.argmax(self.Q, axis=1)
                    
        return self.Q,  self.Q2pol(self.Q)

            
    def traces2Q(self, trace):
        for var in trace:
            self.R[int(var[0]),int(var[1])]=int(var[3])
            self.occurence[int(var[0]),int(var[1]),int(var[2])]+=1
            for final_state in range(0,self.nS):
                self.P[int(var[0]),int(var[1]),int(final_state)]=self.occurence[int(var[0]),int(var[1]),int(final_state)]/sum(self.occurence[int(var[0]),int(var[1])])
            self.VI()

        return self.Q
    
    def policy(self, x, poltype = 'exploration', par = []):
        # implementar esta funcao
        if poltype == 'exploitation':
            a = self.Pol[x]
            
        elif poltype == 'exploration':
            '''choose a random action'''
            a = random.randint(0,self.nA-1)  
        return a
    
    def Q2pol(self, Q, eta=5):
        # implementar esta funcao
        return 0


            