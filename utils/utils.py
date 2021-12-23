def str_to_bool(value):
    """

    Args:
        value: the boolean string to convert

    Returns:
        bool: True if the given value os 'true' or 'yes', False otherwise

    """
    return value.lower() == 'true' or value.lower() == 'yes'
