import difflib


def print_differences(str1, str2):
    diff = list(difflib.ndiff(str1.splitlines(), str2.splitlines()))
    for line in diff:
        # Lines that are different will start with a - or + symbol
        if line.startswith("- "):
            print(f"Added:{line}")
        elif line.startswith("+ "):
            print(f"Dropped: {line}")
        else:
            pass
