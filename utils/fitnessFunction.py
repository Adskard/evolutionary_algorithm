
def oneMax(data : list):
    try:
        assert all([(isinstance(item, int) and (item==0 or item==1)) for item in data])
    except:
        raise AssertionError("Incorrect input, takes only list of 0 and 1s")

    return sum(data)
    

def labs(data : list):
    try:
        assert all([(isinstance(item, int) and (item==0 or item==1)) for item in data])
    except:
        raise AssertionError("Incorrect input, takes only list of 0 and 1s")

    list = [-1 if x==0 else x for x in data ]
    energy = 0
    n = len(list)

    for k in range(1,n): 
        corr = 0
        for i in range(0, n - k):
            corr += list[i] * list[i+ k] 
        energy += corr*corr
    return energy
    

def sphere(data : list, offset : list):
    try:
        assert all([(isinstance(item, float) or isinstance(item, int))   for item in data])
        assert all([(isinstance(item, float) or isinstance(item, int)) for item in offset])
    except:
        raise AssertionError("Incorrect input, takes only numbers")
    try:
        assert len(data)==len(offset)
    except:
        raise AssertionError("Incorrect input, argument list lenghts must be equal")

    sum = 0
    for i in range(len(data)):
        sum += (data[i]-offset[i])*(data[i]-offset[i])
    return sum

def rosebrock(data : list):
    try:
        assert all([(isinstance(item, float) or isinstance(item, int))   for item in data])
    except:
        raise AssertionError("Incorrect input, takes only numbers")

    sum = 0
    for i in range(len(data)-1):
        sum+= 100*(data[i+1] - data[i]*data[i])*(data[i+1] - data[i]*data[i]) + (1-data[i])*(1-data[i])
    return sum
