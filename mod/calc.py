from collections import OrderedDict
 
# data = [["team29", "190219_5fA_5falarm", 1550555079, 19.0], ["team28", "190219_5fA_5falarm", 1550555111, 100.0], ["team08", "190219_5fA_5falarm", 1550555313, 100.0], ["team09", "190219_5fA_5falarm", 1550555333, 100.0], ["team18", "190219_5fA_5falarm", 1550555350, 100.0], ["team15", "190219_5fA_5falarm", 1550555384, 100.0], ["team14", "190219_5fA_5falarm", 1550555465, 100.0], ["team12", "190219_5fA_5falarm", 1550555482, 100.0], ["team29", "190219_5fA_5falarm", 1550555541, 100.0], ["team31", "190219_5fA_5falarm", 1550555669, 100.0], ["team05", "190219_5fA_5falarm", 1550555772, 19.0], ["team19", "190219_5fA_5falarm", 1550555797, 100.0], ["team01", "190219_5fA_5falarm", 1550555947, 100.0], ["team26", "190219_5fA_5falarm", 1550555981, 100.0], ["team15", "190219_5fC_5fbubblebass", 1550556142, 5.0], ["team29", "190219_5fC_5fbubblebass", 1550556150, 5.0], ["team13", "190219_5fA_5falarm", 1550556259, 100.0], ["team25", "190219_5fA_5falarm", 1550556263, 100.0], ["team21", "190219_5fA_5falarm", 1550556316, 100.0], ["team07", "190219_5fA_5falarm", 1550556342, 100.0], ["team02", "190219_5fC_5fbubblebass", 1550556944, 5.0], ["team29", "190219_5fC_5fbubblebass", 1550556945, 10.0], ["team28", "190219_5fC_5fbubblebass", 1550556976, 5.0], ["team28", "190219_5fC_5fbubblebass", 1550557094, 10.0], ["team22", "190219_5fC_5fbubblebass", 1550557329, 5.0], ["team02", "190219_5fA_5falarm", 1550557402, 100.0], ["team10", "190219_5fA_5falarm", 1550557691, 100.0], ["team34", "190219_5fD_5ffun", 1550557793, 10.0], ["team11", "190219_5fA_5falarm", 1550557817, 100.0], ["team01", "190219_5fD_5ffun", 1550558057, 10.0], ["team28", "190219_5fC_5fbubblebass", 1550558217, 58.0], ["team31", "190219_5fF_5felevator", 1550558365, 7.0], ["team12", "190219_5fE_5fironbutt", 1550558506, 8.0], ["team34", "190219_5fA_5falarm", 1550558565, 100.0], ["team22", "190219_5fC_5fbubblebass", 1550558639, 10.0], ["team16", "190219_5fA_5falarm", 1550558686, 100.0], ["team25", "190219_5fF_5felevator", 1550559313, 25.0], ["team31", "190219_5fF_5felevator", 1550559495, 42.0], ["team24", "190219_5fC_5fbubblebass", 1550559645, 5.0], ["team15", "190219_5fC_5fbubblebass", 1550559698, 26.0], ["team31", "190219_5fF_5felevator", 1550559722, 49.0], ["team05", "190219_5fA_5falarm", 1550559755, 100.0], ["team18", "190219_5fC_5fbubblebass", 1550559829, 8.0], ["team27", "190219_5fA_5falarm", 1550559831, 19.0], ["team18", "190219_5fC_5fbubblebass", 1550559924, 26.0], ["team31", "190219_5fF_5felevator", 1550559949, 57.0], ["team25", "190219_5fF_5felevator", 1550560020, 100.0], ["team28", "190219_5fD_5ffun", 1550560118, 100.0], ["team18", "190219_5fC_5fbubblebass", 1550560181, 31.0], ["team16", "190219_5fC_5fbubblebass", 1550560260, 58.0], ["team29", "190219_5fE_5fironbutt", 1550560500, 8.0], ["team01", "190219_5fC_5fbubblebass", 1550560557, 5.0], ["team31", "190219_5fD_5ffun", 1550560699, 10.0], ["team15", "190219_5fC_5fbubblebass", 1550560789, 40.0], ["team27", "190219_5fF_5felevator", 1550560806, 7.0], ["team29", "190219_5fE_5fironbutt", 1550560891, 45.0], ["team18", "190219_5fF_5felevator", 1550560927, 7.0], ["team02", "190219_5fC_5fbubblebass", 1550560986, 10.0], ["team23", "190219_5fA_5falarm", 1550561110, 19.0], ["team15", "190219_5fC_5fbubblebass", 1550561110, 58.0], ["team04", "190219_5fA_5falarm", 1550561214, 100.0], ["team23", "190219_5fA_5falarm", 1550561217, 100.0], ["team27", "190219_5fF_5felevator", 1550561235, 15.0], ["team07", "190219_5fC_5fbubblebass", 1550561576, 5.0], ["team19", "190219_5fF_5felevator", 1550561884, 8.0], ["team09", "190219_5fE_5fironbutt", 1550561934, 8.0], ["team34", "190219_5fC_5fbubblebass", 1550562007, 8.0], ["team29", "190219_5fD_5ffun", 1550562077, 10.0], ["team02", "190219_5fD_5ffun", 1550562124, 10.0], ["team22", "190219_5fA_5falarm", 1550562146, 19.0], ["team02", "190219_5fE_5fironbutt", 1550562395, 8.0], ["team27", "190219_5fF_5felevator", 1550562486, 22.0], ["team01", "190219_5fE_5fironbutt", 1550562511, 8.0], ["team34", "190219_5fC_5fbubblebass", 1550562716, 13.0], ["team15", "190219_5fD_5ffun", 1550562809, 10.0], ["team14", "190219_5fC_5fbubblebass", 1550562904, 5.0], ["team23", "190219_5fC_5fbubblebass", 1550563169, 5.0], ["team09", "190219_5fD_5ffun", 1550563470, 10.0], ["team29", "190219_5fD_5ffun", 1550563634, 15.0], ["team15", "190219_5fD_5ffun", 1550563693, 100.0], ["team31", "190219_5fC_5fbubblebass", 1550563751, 5.0], ["team10", "190219_5fC_5fbubblebass", 1550563958, 18.0], ["team34", "190219_5fC_5fbubblebass", 1550564078, 26.0], ["team25", "190219_5fD_5ffun", 1550564096, 10.0], ["team28", "190219_5fB_5fjellyfish", 1550564382, 10.0], ["team25", "190219_5fC_5fbubblebass", 1550564722, 5.0], ["team11", "190219_5fD_5ffun", 1550564999, 5.0], ["team15", "190219_5fC_5fbubblebass", 1550565283, 63.0], ["team15", "190219_5fE_5fironbutt", 1550565556, 25.0], ["team01", "190219_5fC_5fbubblebass", 1550565894, 26.0], ["team14", "190219_5fD_5ffun", 1550566037, 10.0], ["team01", "190219_5fD_5ffun", 1550566108, 15.0], ["team15", "190219_5fF_5felevator", 1550566199, 8.0], ["team29", "190219_5fC_5fbubblebass", 1550566480, 13.0], ["team27", "190219_5fD_5ffun", 1550566527, 10.0], ["team23", "190219_5fE_5fironbutt", 1550566554, 8.0], ["team18", "190219_5fC_5fbubblebass", 1550566582, 58.0], ["team28", "190219_5fE_5fironbutt", 1550566851, 17.0], ["team15", "190219_5fB_5fjellyfish", 1550567008, 10.0], ["team02", "190219_5fF_5felevator", 1550567077, 7.0]]
 
def CheckReScore(data):
    for key in data.keys():
        print(key)
        for User in data[key].keys():
            print("    {}:{}".format(User, data[key][User]))
 
def CheckSortData(data):
    for Key in data.keys():
        print(Key)
        for Score in data[Key].keys():
            print('    {}'.format(Score))
            for User in data[Key][Score]:
                print('        {}'.format(User))
 
def CheckFinalData(data):
    for Key in data.keys():
        print(Key)
        for Rank in data[Key].keys():
            print('    {}'.format(Rank))
            for User in data[Key][Rank]:
                print('        {}'.format(User))
 
def GetRank(data, time, n):
    NewData    = []
    ReScore    = {}
    SortData   = {}
    SortedData = {}
    FinalData  = {}
 
    # remove time after target time
 
    for i in range(0, len(data)):
        if data[i][2] < time:
            NewData.append(data[i])
 
    # create map
 
    for each in NewData:
        UserName = each[0]
        ProName  = each[1]
        Score    = each[3]
        if ProName not in ReScore:
            ReScore[ProName] = {}
        if UserName not in ReScore[ProName]:
            ReScore[ProName][UserName] = Score
        else:
            if Score > ReScore[ProName][UserName]:
                ReScore[ProName][UserName] = Score
    # CheckReScore(ReScore)
 
    # creat sort map
 
    for Key in ReScore.keys():
        SortData[Key]   = {}
        SortedData[Key] = {}
        for User in ReScore[Key].keys():
            Score = ReScore[Key][User]
            if Score not in SortData[Key]:
                SortData[Key][Score] = [User]
            else:
                SortData[Key][Score].append(User)
        SortedData[Key] = OrderedDict(sorted(SortData[Key].items()))
    # CheckSortData(SortData)
    # CheckSortData(SortedData)
 
    # create final score map
 
    for Key in ReScore.keys():
        FinalData[Key] = OrderedDict()
        Rank           = 1
        for i in range(1, n+1):
            FinalData[Key][str(i)] = []
        for Score in list(reversed(SortedData[Key].keys())):
            while Rank < n:
                RankTemp = 0
                for User in SortedData[Key][Score]:
                    FinalData[Key][str(Rank)].append(User)
                    RankTemp += 1
                Rank += RankTemp
                break
    # CheckFinalData(FinalData)
 
    return FinalData