# G 084    86971   Diogo António Da Silva Costa   82374   Luana Ascensão de Jesus Marques
import copy
import numpy as np


def change_to_truefalse(index,evid):
    '''changes the var in index to true(1) and false(0)'''
    evid_true_list = list(evid)
    evid_false_list = list(evid)
        
    evid_true_list[index] = 1
    evid_false_list[index] = 0

    return tuple(evid_true_list), tuple(evid_false_list)


class Node():
    def __init__(self, prob, parents = []):
        self.parents = copy.deepcopy(parents)
        
        if len(self.parents)>=1:
            self.prob = np.copy(prob)
        else:
            self.prob = prob[0]
    
    def computeProb(self, evid):
        if len(self.parents)>=1:
            array = np.copy(self.prob)
            for parent in self.parents:
                array = array[evid[parent]]
        else:
            array = self.prob

        return [1-array, array]
    
class BN():
    def __init__(self, gra, prob):
        '''gra -> list of links between nodes; prob --> list of nodes'''
        self.gra = copy.deepcopy(gra)
        self.prob = copy.deepcopy(prob)
        self.prob_list = []  

    def computePostProb(self, evid):
        for index in range(len(evid)):
            if evid[index] == -1:
                break

        evid_true, evid_false = change_to_truefalse(index,evid)
        
        self.check_unknown(evid_true)
        x = sum(self.prob_list)
        self.prob_list[:] = []

        self.check_unknown(evid_false)
        y = sum(self.prob_list)
        self.prob_list[:] = []

        return x/(x+y)
        
    def check_unknown(self,evid):
        no_unknown = 1
        for index in range(len(evid)):
            if type(evid[index]) != int:
                no_unknown = 0
                break

        if no_unknown == 0:
            evid_true, evid_false = change_to_truefalse(index,evid)
            self.check_unknown(evid_true)
            self.check_unknown(evid_false)
        else:
            self.prob_list.append(self.computeJointProb(evid))

    def computeJointProb(self, evid):
        jointProb = 1
        for index in range(len(self.prob)):
            node = self.prob[index]
            jointProb = jointProb*node.computeProb(evid)[evid[index]]
        return jointProb

