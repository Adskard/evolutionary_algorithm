
import math


def binary(data : list, lowerBound : list, upperBound : list):
    try:
        assert all([(isinstance(item, int) and (item==0 or item==1)) for item in data])
    except:
        raise AssertionError("Incorrect input, takes only list of 0 and 1s")
    try:
        assert (len(data) % len(lowerBound) == 0)
    except:
        raise AssertionError("The binary vector length is not divisible by the dimensionality of the target vector space.")
    try:
        assert (len(lowerBound) == len(upperBound))
    except:
        raise AssertionError("Lower bound vector and upper bound vector are not the same lenghts")
    print("BINARY VECTO _________ ", data)
    cellSize = len(data)//len(lowerBound)
    denominator = math.pow(2, cellSize) -1
    result = [0] * len(lowerBound)
    for i in range(len(lowerBound)):
        numerator = binaryToDecimal(data[i*cellSize:(i+1)*cellSize]) * abs(upperBound[i]-lowerBound[i])
        result[i] = numerator / denominator - abs(lowerBound[i])
    return result

def binaryToDecimal(bin : list):
    sum = 0
    for i in range(len(bin)):
        sum += bin[i] * 2**(len(bin)-1-i)
    return sum

