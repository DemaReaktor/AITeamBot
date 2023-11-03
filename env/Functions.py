# Define Fibonacci sequence
def fibonacci_sequence():
    """
    This function defines the Fibonacci sequence.
    
    Returns:
        list: The Fibonacci sequence.
    """
    sequence = [0, 1]
    while len(sequence) < 9:
        next_number = sequence[-1] + sequence[-2]
        sequence.append(next_number)
    return sequence

# Find the 9th Fibonacci number
def find_nth_fibonacci_number():
    """
    This function calls the Fibonacci sequence function and finds the 9th number in the sequence.
    
    Returns:
        int: The 9th Fibonacci number.
    """
    sequence = fibonacci_sequence()
    return sequence[8]

#------------------
