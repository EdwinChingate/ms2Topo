from __future__ import annotations
def remove_contained_modules(sorted_size_indices,
                             full_overlapping_loc):
    
    sorted_size_indices_cleaning = sorted_size_indices.copy()
    
    for module_id in full_overlapping_loc:  
        sorted_size_indices_cleaning = sorted_size_indices_cleaning[sorted_size_indices_cleaning != module_id]
        
    return sorted_size_indices_cleaning