def UpdateModulesAfterClustering(New_Modules,
                                 Modules):
    if len(Modules) == len(New_Modules):
        return Modules
    UpdatedModules = []
    for new_module in New_Modules:
        updatedModule = []
        for module in new_module:
            updatedModule += Modules[module]
        UpdatedModules.append(updatedModule)
    return UpdatedModules
