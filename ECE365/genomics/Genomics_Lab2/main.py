import numpy as np
from collections import OrderedDict


class Lab2(object):

    def smith_waterman_alignment(self, s1, s2, penalties):
        '''
        Input - two sequences and a dictionary with penalities for match, mismatch and gap
        Output - an integer value which is the maximum smith waterman alignment score
        '''
        # start code here
        dim_x, dim_y = len(s1), len(s2)
        # dp = np.zeros((dim_x+1, dim_y+1))
        dp = [[0 for _ in range(dim_y+1)] for _ in range(dim_x+1)]
        max_score = 0

        for i in range(dim_x):
            for j in range(dim_y):
                if s1[i] == s2[j]:
                    update = dp[i][j]+penalties['match']
                else:
                    update = dp[i][j]+penalties['mismatch']
                new_H = max(update, dp[i][j+1]+penalties['gap'],
                            dp[i+1][j]+penalties['gap'], 0)

                dp[i+1][j+1] = new_H
                if max_score < new_H:
                    max_score = new_H

        return int(max_score)
        # end code here

    def print_smith_waterman_alignment(self, s1, s2, penalties):
        '''
        Input - two sequences and a dictionary with penalities for match, mismatch and gap
        Output - a tuple with two strings showing the two sequences with '-' representing the gaps
        '''
        # start code here
        dim_x, dim_y = len(s1), len(s2)
        dp = np.zeros((dim_x+1, dim_y+1))
        max_score = 0
        max_x, max_y = 0, 0
        s1_out, s2_out = '', ''

        for i in range(dim_x):
            for j in range(dim_y):
                if s1[i] == s2[j]:
                    update = dp[i][j]+penalties['match']
                else:
                    update = dp[i][j]+penalties['mismatch']
                new_H = max(update, dp[i][j+1]+penalties['gap'],
                            dp[i+1][j]+penalties['gap'], 0)

                dp[i+1][j+1] = new_H
                if max_score < new_H:
                    max_score = new_H
                    max_x, max_y = i+1, j+1

        # print(dp)
        while dp[max_x][max_y] != 0:
            # print(max_x, max_y)
            # print(dp[max_x][max_y])
            if s1[max_x-1] == s2[max_y-1]:
                s1_out += s1[max_x-1]
                s2_out += s2[max_y-1]
                max_x -= 1
                max_y -= 1
            elif dp[max_x][max_y] == dp[max_x-1][max_y] + penalties['gap']:
                s1_out += s1[max_x-1]
                s2_out += '-'
                max_x -= 1
            elif dp[max_x][max_y] == dp[max_x][max_y-1] + penalties['gap']:
                s1_out += '-'
                s2_out += s2[max_y-1]
                max_y -= 1
            else:
                s1_out += s1[max_x-1]
                s2_out += s2[max_y-1]
                max_x -= 1
                max_y -= 1

        return (s1_out[::-1], s2_out[::-1])
        # end code here

    def find_exact_matches(self, list_of_reads, genome):
        '''
        Input - list of reads of the same length and a genome fasta file (converted into a single string)
        Output - a list with the same length as list_of_reads, where the ith element is a list of all locations (starting positions) in the genome where the ith read appears. The starting positions should be specified using the "chr2:120000" format
        '''

        # start code here
        hash_function = OrderedDict()

        dna_list = []
        read_strs = genome.split(">")[1:]
        for i in read_strs:
            lines_to_concat = i.split("\n")[1:]
            dna_list.append("".join(lines_to_concat))

        L = len(list_of_reads[0])
        for i in range(len(dna_list)):
            dna = dna_list[i]
            if L < len(dna):
                for j in range(len(dna) - L + 1):
                    segment = dna[j: j+L]
                    index = 'chr%d:%d' %(i+1, j+1)

                    if segment not in hash_function:
                        hash_function[segment] = [index]
                    else:
                        hash_function[segment].append(index)
                    
        output = []
        for read in list_of_reads:
            if read in hash_function:
                output.append(hash_function[read])
            else:
                output.append([])
        return output
        # end code here

    def find_approximate_matches(self, list_of_reads, genome):
        '''
        Input - list of reads of the same length and a genome fasta file (converted into a single string)
        Output -  a list with the same length as list_of_reads, where the ith element is a list of all locations (starting positions) in the genome which have the highest smith waterman alignment score with ith read in list_of_reads
        '''

        # start code here
        hash_function = OrderedDict()

        dna_list = []
        read_strs = genome.split(">")[1:]
        for i in read_strs:
            lines_to_concat = i.split("\n")[1:]
            dna_list.append("".join(lines_to_concat))

        L = len(list_of_reads[0])
        k = L // 4
        for i in range(len(dna_list)):
            dna = dna_list[i]
            for j in range(len(dna) - k + 1):
                segment, index = dna[j: j+k], (i, j)

                if segment not in hash_function:
                    hash_function[segment] = [index]
                else:
                    hash_function[segment].append(index)
                    
        output = []
        penalties = {'match': 1, 'mismatch': -1, 'gap': -1}
        for read in list_of_reads:
            max_score = 0
            partial_res = []
            for index in range(len(read) - k + 1):
                segment = read[index: index+k]
                if segment in hash_function:
                    tuple_list = hash_function[segment]
                    for _tuple in tuple_list: 
                        i, j = _tuple
                        dna = dna_list[i]
                        if len(dna) >= len(read):
                            start, end = max(0, j-L), min(len(dna)-L, j+L)
                            for s in range(start, end+1):
                                new_score = self.smith_waterman_alignment(read, dna[s: s+L], penalties)
                                orig_index = 'chr%d:%d' %(i+1, s+1)
                                if max_score < new_score:
                                    max_score = new_score
                                    partial_res = [orig_index]
                                elif (orig_index not in partial_res) and (max_score == new_score):
                                    partial_res.append(orig_index)
            output.append(partial_res)

        return output
        # end code here
