import pandas as pd
import statsmodels.api as sm
import numpy as np
import statsmodels

class Lab3(object):

    def create_data(self, snp_lines):
        '''
        Input - the snp_lines parsed at the beginning of the notebook
        Output - You should return the 53 x 3902 dataframe
        '''
        # start code here
        column_names = []
        snp = []
        for i in snp_lines:
            row = i.split()
            snp.append(row)
            column_names.append(str(row[0])+':'+str(row[1]))
        df = np.zeros((53, 3902))
        for i in range(len(snp_lines)):
            for j in range(9, 62):
                if snp[i][j]== '0/0':
                    df[j-9][i] = 0
                elif snp[i][j]== '1/0':
                    df[j-9][i] = 1
                elif snp[i][j]== '0/1':
                    df[j-9][i] = 1
                elif snp[i][j]== '1/1':
                    df[j-9][i] = 2
                else:
                    df[j-9][i] = np.nan
        df = pd.DataFrame(df)
        df.columns = column_names
        return df
        # end code here

    def create_target(self, header_line):
        '''
        Input - the header_line parsed at the beginning of the notebook
        Output - a list of values(either 0 or 1)
        '''
        # start code here
        res = []
        headers = header_line.split("\t")
        for i in range(9, len(headers)):
            if "yellow" in headers[i]:
                res.append(1)
            elif "dark" in headers[i]:
                res.append(0)
        return res
        # end code here

    def logistic_reg_per_snp(self, df):
        '''
        Input - snp_data dataframe
        Output - list of pvalues and list of betavalues
        '''
        # start code here 
        p_values, beta_values = [], []
        ytrain = list(df['target'])
        for i in df.columns[: 3902]:
            xtrain = sm.add_constant(list(df[i]))
            LR = sm.Logit(ytrain, xtrain, missing='drop').fit(method='bfgs', disp=False)
            p_values.append(round(LR.pvalues[1], 9))
            beta_values.append(round(LR.params[1], 5))
        return p_values, beta_values
        # end code here
    

    def get_top_snps(self, snp_data, p_values):
        '''
        Input - snp dataframe with target column and p_values calculated previously
        Output - list of 5 tuples, each with chromosome and position
        '''
        # start code here
        res = []
        top_snps_p_values = np.argsort(p_values)[: 5]
        for i in top_snps_p_values:
            label = snp_data.columns[i]
            res.append(tuple(label.split(":")))
        return res