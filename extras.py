from collections import Counter

def find_majority_element(strings):
    """
    Finds the string with the most occurrences in the array that is greater than 50% of the total.

    Parameters:
        strings (list): List of strings.

    Returns:
        str or None: The string that appears more than 50% of the time, or None if no such string exists.
    """
    n = len(strings)
    if n == 0:
        return None

    # Count occurrences of each string
    counts = Counter(strings)

    # Check for the majority element
    for string, count in counts.items():
        if count > n / 2:
            return string

    return None