from overlapping2modules import *
def overlapping_modules_vector_crafter(module_1,
                                       AdjacencyList_Features):
    overlapping_modules = lambda module: overlapping2modules(module_1 = module_1,
                                                             module_2 = module)
    overlapping_modules_vector = list(map(overlapping_modules,
                                          AdjacencyList_Features))
    return overlapping_modules_vector
