def filter_digits(input_array: list) -> list:
    
    """
    The function iterates over each string in the input_array, filters out the digits, converts them into integers,
    and appends them to a new list called filtered_array.


    Example:
    input_array = ["abc123", "def456", "ghi789"]
    result = filter_digits(input_array)
    print(result)  # Output: [123, 456, 789]

    Arguments
    ----------
    input_array: list
        the input list of strings which will have alphanumeric characters 
        
    Returned Values
    ----------
    filtered_array: list
        the filtered list of intergers with only numeric data

    """
    filtered_array = []

    for string in input_array:
        filtered_string =  int(''.join(char for char in string if char.isdigit()))
        filtered_array.append(filtered_string)

    return filtered_array