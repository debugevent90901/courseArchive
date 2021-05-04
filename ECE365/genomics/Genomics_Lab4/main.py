import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


class Lab4(object):

    def expectation_maximization(self, read_mapping, tr_lengths, n_iterations):
        # start code here
        history = [[1/len(tr_lengths)] for _ in range(len(tr_lengths))]
        Z = np.zeros((len(read_mapping), len(tr_lengths)))
        for _ in range(n_iterations):
            for i in range(len(read_mapping)):
                for j in range(len(tr_lengths)):
                    if j in read_mapping[i]:
                        _sum = 0
                        for k in read_mapping[i]:
                            _sum += history[k][-1]
                        Z[i][j] = history[j][-1] / _sum
            theta = np.array(Z.sum(axis=0) / len(read_mapping))
            for i in range(len(tr_lengths)):
                history[i].append(theta[i] / tr_lengths[i] /
                                sum(theta/np.array(tr_lengths)))
        return history
        # end code here

    def prepare_data(self, lines_genes):
        '''
        Input - list of strings where each string corresponds to expression levels of a gene across 3005 cells
        Output - gene expression dataframe
        '''
        # start code here
        dict = {}
        column_names = ["Gene_"+str(i) for i in range(len(lines_genes))]
        for i in range(len(lines_genes)):
            dict[column_names[i]] = np.round(np.log([float(j)+1 for j in lines_genes[i].split(' ')]), 5)
        df =  pd.DataFrame(dict)
        return df
        # end code here

    def identify_less_expressive_genes(self, df):
        '''
        Input - gene expression dataframe
        Output - list of column names which are expressed in less than 25 cells
        '''
        # start code here
        is_ok = (df.values > 0).sum(axis=0) < 25
        return df.columns[is_ok]
        # end code here

    def perform_pca(self, df):
        '''
        Input - df_new
        Output - numpy array containing the top 50 principal components of the data.
        '''
        # start code here
        return np.round(PCA(n_components=50, random_state=365).fit_transform(df.values), 5)
        # end code here

    def perform_tsne(self, pca_data):
        '''
        Input - pca_data
        Output - numpy array containing the top 2 tsne components of the data.
        '''
        # start code here
        return TSNE(n_components=2, perplexity=50, random_state=1000).fit_transform(pca_data)
        # end code here
