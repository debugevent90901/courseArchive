import numpy as np
from collections import OrderedDict


class Lab1(object):
    def parse_reads_illumina(self, reads):
        '''
        Input - Illumina reads file as a string
        Output - list of DNA reads
        '''
        # start code here
        dnaSequenceList = []
        lines = reads.split("\n")
        for i in range(len(lines)):
            if (i % 4 == 1):
                dnaSequenceList.append(lines[i])
        return dnaSequenceList
        # end code here

    def unique_lengths(self, dna_reads):
        '''
        Input - list of dna reads
        Output - set of counts of reads
        '''
        # start code here
        lengthList = []
        for i in dna_reads:
            lengthList.append(len(i))
        return set(lengthList)
        # end code here

    def check_impurity(self, dna_reads):
        '''
        Input - list of dna reads
        Output - list of reads which have impurities, a set of impure chars 
        '''
        # start code here
        standardCharSet = set(["A", "C", "G", "T"])
        impurityList = []
        impureCharList = []
        for i in dna_reads:
            caseSensitive = i.replace("a", "A").replace("c", "C").replace("g", "G").replace("t", "T")
            charSet = set(list(caseSensitive))
            if charSet - standardCharSet != set():
                impurityList.append(i)
                impureCharList.extend(list(charSet - standardCharSet))
        return impurityList, set(impureCharList)
        # end code here

    def get_read_counts(self, dna_reads):
        '''
        Input - list of dna reads
        Output - dictionary with key as read and value as the no. of times it occurs
        '''
        # start code here
        countDictionary = OrderedDict()
        for i in dna_reads:
            if i in countDictionary:
                countDictionary[i] += 1
            else:
                countDictionary[i] = 1
        return countDictionary
        # end code here

    def parse_reads_pac(self, reads_pac):
        '''
        Input - pac bio reads file as a string
        Output - list of dna reads
        '''
        # start code here
        dnaReadsList = []
        readStrs = reads_pac.split(">")[1:]
        for i in readStrs:
            linesToConcat = i.split("\n")[1:]
            dnaReadsList.append("".join(linesToConcat))
        return dnaReadsList
        # end code here
