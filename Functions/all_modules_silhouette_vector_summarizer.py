from __future__ import annotations
from module_silhouette_vector_summarizer import *
import numpy as np
from silhouette_vector_calculator import *

def all_modules_silhouette_vector_summarizer(CosineMat,
                                             modules,
                                             percentile = 10):
    
    silhouette_vector = silhouette_vector_calculator(CosineMat = CosineMat,
                                                     modules = modules) 
    
    modules_silhouette_summary_table = []
    for module in modules:
        module_silhouette_summary = module_silhouette_vector_summarizer(silhouette_vector = silhouette_vector,
                                                                        module = module,
                                                                        percentile = percentile)
        modules_silhouette_summary_table.append(module_silhouette_summary)
    
    return np.array(modules_silhouette_summary_table)