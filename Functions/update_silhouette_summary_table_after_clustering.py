from __future__ import annotations
import numpy as np
def update_silhouette_summary_table_after_clustering(modules,
                                                     modules_silhouette_summary_tables_list):
    
    sampling_modules_silhouette_summary_table = []
    
    for module in modules:
        first_cluster = True
        for module_id in module:
            module_silhouette_summary = modules_silhouette_summary_tables_list[module_id].copy().reshape(-1, 1)
            if first_cluster:
                module_silhouette_summary_mat = module_silhouette_summary
                first_cluster = False
            else:
                module_silhouette_summary_mat = np.hstack((module_silhouette_summary_mat,
                                                           module_silhouette_summary))
        mean_module_silhouette_summary = np.mean(module_silhouette_summary_mat.T,
                                                 axis = 0)        
        sampling_modules_silhouette_summary_table.append(mean_module_silhouette_summary)
        
    sampling_modules_silhouette_summary_table = np.array(sampling_modules_silhouette_summary_table)
    
    return sampling_modules_silhouette_summary_table
