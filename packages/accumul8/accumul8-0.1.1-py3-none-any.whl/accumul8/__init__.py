# This is a placeholder package for reserving the namespace. A simple hello_world function is included.

def hello_world(name=None):
    """Prints a personalized greeting to the console.

    Args:
        name (str, optional): The name of the user. If not provided, defaults to None.

    Returns:
        None
    """
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, World!")
