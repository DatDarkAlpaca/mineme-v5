def get_number_with_separator(number: float) -> str:
    integer_part, fractional_part = str(float(number)).split(".")

    reversed_integer = integer_part[::-1]

    grouped = [reversed_integer[i : i + 3] for i in range(0, len(reversed_integer), 3)]
    formatted_integer = "'".join(grouped)[::-1]

    if fractional_part == "0":
        return formatted_integer

    else:
        return f"{formatted_integer}.{fractional_part[:2]}"
