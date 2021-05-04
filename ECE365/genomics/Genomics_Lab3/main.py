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
        df = np.zeros((53, 3902))
        column_name = []
        for i in range(len(snp_lines)):
            line = snp_lines[i].split("\t")
            line[-1] = line[-1][:-3]
            column_name.append(line[2])
            for j in range(9, 62):
                # print(line[j])
                if '.' in line[j]:
                    df[j-9][i] = np.nan
                elif '1' == line[j]:
                    df[j-9][i] = 1
                elif '0' == line[j]:
                    df[j-9][i] = 0
                else:
                    df[j-9][i] = (int(line[j][0]) + int(line[j][2]))
        df = pd.DataFrame(df)
        df.columns = column_name
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
        ytrain = df[['target']]
        columns = df.columns
        for i in range(len(columns)):
            xtrain = df[[columns[i]]]
            xtrain = sm.add_constant(xtrain)
            log_reg = sm.Logit(ytrain, xtrain).fit(method='bfgs', disp=False)

        # end code here

    def get_top_snps(self, snp_data, p_values):
        '''
        Input - snp dataframe with target column and p_values calculated previously
        Output - list of 5 tuples, each with chromosome and position
        '''
        # start code here

        # end code here
