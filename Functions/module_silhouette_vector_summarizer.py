from __future__ import annotations
import numpy as np
def module_silhouette_vector_summarizer(silhouette_vector,
                                        module,
                                        percentile = 10):

    module_list = list(module)      
    silhouette_coefficients_module = silhouette_vector[module_list]
    n = len(module_list)

    median_silhouette_coefficient = np.median(silhouette_coefficients_module)         
    min_silhouette_coefficient = np.percentile(silhouette_coefficients_module,
                                               percentile)
    max_silhouette_coefficient = np.percentile(silhouette_coefficients_module,
                                               100 - percentile)
    Q1_silhouette_coefficient = np.percentile(silhouette_coefficients_module,
                                              25)
    Q3_silhouette_coefficient = np.percentile(silhouette_coefficients_module,
                                              75)           
 
    module_silhouette_summary = [n,
                                 min_silhouette_coefficient,
                                 Q1_silhouette_coefficient,
                                 median_silhouette_coefficient,
                                 Q3_silhouette_coefficient,
                                 max_silhouette_coefficient]
    
    return module_silhouette_summary
