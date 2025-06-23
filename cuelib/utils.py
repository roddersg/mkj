def get_input_yn(prompt: str, default="Y") -> str:
    """Returns Y by default e,g, RET or Y, else N."""
    ans = input(prompt)
    if ans == "":
        return default
    if ans.upper() == "Y":
        return "Y"
    # any other answer is a NO
    return "N"


def get_input_with_default(prompt: str, default_result: any) -> any:
    """
    Prompt the user for input, returning the default if they press Enter.

    The return type matches the type of the default value.
    Args:
        prompt (str): The prompt to display to the user
        default_result (any): The default return value if user presses Enter

    Returns:
        any: Either the user's input (converted to default's type) or the default value

    """
    full_prompt = f"{prompt} (default: {default_result}): "
    user_input = input(full_prompt).strip()

    if user_input == "":
        return default_result

    # Convert input to match the default's type
    default_type = type(default_result)

    try:
        if default_type is bool:
            # Handle boolean conversion (accept 'true', 'false', 'yes', 'no', etc.)
            return user_input.lower() in ("y", "yes", "true", "t", "1")
        elif default_type is int:
            return int(user_input)
        elif default_type is float:
            return float(user_input)
        elif default_type is str:
            return user_input
        else:
            # For other types, try to construct using the type
            return default_type(user_input)
    except (ValueError, TypeError):
        print(f"Invalid input. Using default value {default_result}.")
        return default_result


# Example usage:
if __name__ == "__main__":
    # String example
    # name = get_input_with_default("Enter your name", "Anonymous")
    # print(f"Hello, {name} (type: {type(name)})")

    # # Integer example
    # age = get_input_with_default("Enter your age", 30)
    # print(f"Age: {age} (type: {type(age)})")

    # # Float example
    # price = get_input_with_default("Enter price", 9.99)
    # print(f"Price: {price} (type: {type(price)})")

    # # Boolean example
    # active = get_input_with_default("Enable feature? (Y/N)", True)
    # print(f"Feature enabled: {active} (type: {type(active)})")

    # # List example (note: input should look like a list, e.g., "[1, 2, 3]")
    # items = get_input_with_default("Enter items", [1, 2, 3])
    # print(f"Items: {items} (type: {type(items)})")

    ans: str = get_input_yn("Do you want to continue? (Y/n)", default="Y")
    if ans == "Y":
        print("Continuing...")
    else:
        print("Aborting...")
