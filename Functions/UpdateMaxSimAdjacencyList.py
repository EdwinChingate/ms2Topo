def UpdateMaxSimAdjacencyList(MaxSimAdjacencyList,
                              AllNeighbors):
    for neighbor in AllNeighbors:
        MaxSimAdjacencyList[neighbor][0] = AllNeighbors
    return MaxSimAdjacencyList
