"""
Mapping functions
"""
import math

def binary_to_interval(data : "list[int]", lower_bound : list, upper_bound : list):
    """
    Binary -> <lower_bound, upper_bound> real number mapping
    """
    assert all([((item==0 or item==1)) for item in data])
    assert len(lower_bound) == len(upper_bound)
    assert len(data) % len(lower_bound) == 0

    cell_size = len(data)//len(lower_bound)
    denominator = math.pow(2, cell_size) - 1
    result = [0] * len(lower_bound)
    for pos, value in enumerate(lower_bound):
        numerator = binary_to_decimal(data[pos*cell_size : (pos+1)*cell_size])
        numerator *= abs(upper_bound[pos] - value)
        result[pos] = numerator / denominator + value
    return result

def binary_to_decimal(binary : "list[int]"):
    """
    Maps binary chromosome to decimal number
    """
    assert all([((item==0 or item==1)) for item in binary])

    decimal = 0
    for position, value in enumerate(binary):
        decimal += value * 2**(len(binary)-1-position)
    return decimal

def test_binary_to_interval():
    """
    Run tests for binary to interval mapping
    """
    print("Testing binary to interval mapping")
    assert binary_to_interval([1,0], [0], [1]) == [0.6666666666666666]
    assert binary_to_interval([0,1], [0], [1]) == [0.3333333333333333]
    assert binary_to_interval([0,0,0], [0,0,0], [1,1,1]) == [0.0, 0.0, 0.0]
    assert binary_to_interval([0,1,1], [0,0,0], [1,1,1]) == [0.0, 1.0, 1.0]
    assert (binary_to_interval([0,1,0,1,0,1,0,1,0,1,0,1], [0,-4,-4,-8], [7,3,4,0])
        == [2.0, 1.0, -1.7142857142857144, -2.2857142857142856])
    assert (binary_to_interval([1,1,0,1,1,0,1,1,0,1,1,0], [0,1,2,3,4,5], [2,4,6,8,10,12])
        == [2.0, 2.0, 4.666666666666666, 8.0, 6.0, 9.666666666666668])
    assert (binary_to_interval([1,1,1,1,1,1,1,1,1,1,1,1], [0,1,2,3,4,5], [2,4,6,8,10,12])
        == [2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
    assert (binary_to_interval([0,1,0,1,0,1,0,1,0,1,0,1], [0,1,2,3,4,5], [2,4,6,8,10,12])
        == [0.6666666666666666, 2.0, 3.333333333333333, 4.666666666666667, 6.0, 7.333333333333334])
    assert (binary_to_interval([1,1,0,1,1,0,1,1,0,1,1,0], [0,-4,-4,-8], [7,3,4,0])
        == [6.0, 2.0, 2.8571428571428568, -1.1428571428571432])

def test_binary_to_decimal():
    """
    Run tests for binary to decimal mapping
    """
    print("Testing binary to decimal mapping")
    assert binary_to_decimal([0]) == 0
    assert binary_to_decimal([1]) == 1
    assert binary_to_decimal([0,0,0]) == 0
    assert binary_to_decimal([0,1,1]) == 3
    assert binary_to_decimal([1,1,1]) == 7
    assert binary_to_decimal([1,1,0,0,1,1,0,0,1,1]) == 819
    assert binary_to_decimal([1,1,1,1,1,1,1,1,1,1]) == 1023
    assert binary_to_decimal([0,1,0,1,0,1,0,1,0,1]) == 341
    assert binary_to_decimal([0,0,0,0,0,1,1,1,1,1]) == 31

def run_tests():
    """
    Run tests for mapping
    """
    print("Running tests...")
    print("================")
    test_binary_to_decimal()
    test_binary_to_interval()
    print("================")
    print("Tests were succesfull")

if __name__ == "__main__":
    run_tests()
