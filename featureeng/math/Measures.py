import pandas as pd

def correlation(pandas_frame, column1, column2, method='pearson'):
    '''
    :param pandas_frame:
    :param column1:
    :param column2:
    :param method:
        pearson : standard correlation coefficient
            +1 : Total positive linear correlation
            0  : No linear correlation
            -1 : Total negative linear correlation

        kendall : Kendall Tau correlation coefficient
        spearman : Spearman rank correlation

    :return:
    '''
    return pandas_frame[column1].corr(pandas_frame[column2], method=method)
