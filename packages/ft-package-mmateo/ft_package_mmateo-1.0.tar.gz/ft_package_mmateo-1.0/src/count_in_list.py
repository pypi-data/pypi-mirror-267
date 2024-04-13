def count_in_list(lst: list, item: any) -> int:
    """
    Counts the number of occurrences of a specific item in a list.

    Args:
        lst (list): The list in which to search for the item.
        item (any): The item to count occurrences of in the list.

    Returns:
        int: The number of occurrences of the item in the list.
    """
    return lst.count(item)
