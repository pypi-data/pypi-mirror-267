import os

import joblib
import pandas as pd
import numpy as np
from sklearn import preprocessing
from kolibri.core.component import Component

##
class MultiColomnOneHotEncoder(Component):
    defaults = {
        "fixed":{
            "dummies":[],
            "handle_unknown": 'ignore'
        }
    }
    def __init__(self, configs={}):

        super().__init__(configs)
        self.__catColumns = self.get_parameter("dummies")
        self.__MultiOHE = {}
        self.encoded_dict={}
    ##


    ##
    def fit(self, data, y=None):


        for col in self.__catColumns:
            OneHotEncoder = preprocessing.OneHotEncoder(sparse=False, handle_unknown=self.get_parameter("handle_unknown"))
            OneHotEncoder.fit(np.array(data.loc[:, col]).reshape(-1, 1))
            self.__MultiOHE[col] = OneHotEncoder
            self.encoded_dict[col]=self.grt_new_col_names(col, OneHotEncoder)
        return self


    def grt_new_col_names(self, col,  ohe):
        return [str(col) + '_' + str(c) for c in ohe.get_feature_names_out()]
    def transform(self, data):

        ##

        if self.__catColumns==[]:
            return data
        catData = data[self.__catColumns]
        data = data.drop(self.__catColumns, axis=1)


        ##
        def Transform_Rec(dta=catData):
            ##
            nCol = dta.shape[1]
            ##
            if nCol == 1:
                ##
                col = dta.columns[0]
                OneHotEncoder = self.__MultiOHE[col]
                transformed = OneHotEncoder.transform(np.array(dta.loc[:, col]).reshape(-1, 1))
                transformed = pd.DataFrame(transformed)
#                transformed.columns = OneHotEncoder.get_feature_names()

                transformed.columns = self.grt_new_col_names(col, OneHotEncoder)
                ##
                return transformed

            else:
                ##
                if (nCol % 2 == 0):
                    middle_index = int(nCol / 2)
                else:
                    middle_index = int(nCol / 2 - 0.5)
                ##
                left = dta.iloc[:, :middle_index]
                right = dta.iloc[:, middle_index:]
                ##
                return pd.concat([Transform_Rec(dta=left), Transform_Rec(dta=right)], axis=1)

        ##
        transformedCatData = Transform_Rec(dta=catData)
        transformedCatData.set_index(data.index, inplace=True)

        ##
        return pd.concat([data, transformedCatData], axis=1)

