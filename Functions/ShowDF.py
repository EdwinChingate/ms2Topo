from IPython.display import HTML, display
from scipy import sparse
import tabulate
import pandas as pd


def ShowDF(DF, col = ''):
    
    if sparse.issparse(DF):
        DF = pd.DataFrame.sparse.from_spmatrix(DF)
        
    elif type(DF) != type(pd.DataFrame()):
        DF = pd.DataFrame(DF)
        
    if col == '':
        col = list(DF.columns)
        
    display(HTML(tabulate.tabulate(DF[col],
                                   headers = col,
                                   tablefmt = 'html')))
