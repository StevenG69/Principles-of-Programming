# Written by Hongyin Zhou for COMP9021
import unicodedata

while True:
    try:
        print("Please input two integers a and b with 0 <= a <= b <= 1114111,")
        print("       both integers being separated by ~, with possibly")
        print("       spaces and tabs before and after the numbers:")
        integers = input("       ")
        # Remove all spaces/tabs and split by '~'
        integers = "".join(integers.split()).split("~")
        if len(integers) != 2:
            raise ValueError
        a, b = int(integers[0]), int(integers[1])
        # Check if a and b are within the valid Unicode range
        if not (0 <= a <= b <= 1114111):
            raise ValueError
        break
    except ValueError:
        print("\nIncorrect input, try again!")

# Calculate the number of characters in the range
str_count = b - a + 1
vstr_count = 0
s_dict = {}

# Find all named characters between a and b
for i in range(a, b + 1):
    try:
        s = chr(i)
        name = unicodedata.name(s)
        vstr_count += 1
        s_dict[name] = s
    except ValueError:
        pass  # Character has no name
print()
# Output results
if str_count == 1:
    if vstr_count == 1:
        print(f'{a} is the code point of a named character.')
    else:
        print(f'{a} is not the code point of a named character.')

elif str_count > 1:
    if vstr_count == 0:
        print(f'No number between {a} and {b}\n  is the code point of a named character.')
    elif str_count == vstr_count:
        print(f'All numbers between {a} and {b}\n  are code points of named characters.')
    elif str_count > vstr_count:
        print(f'Amongst the numbers between {a} and {b},')
        print(f'  {(vstr_count / str_count) * 100:.2f}% are code points of named characters.')

    # Allow user to filter by the start of the Unicode character names
    print()
    start = input("Enter a string: ")
    print()

    filtered = {name: char for name, char in s_dict.items() if name.startswith(start)}

    if filtered:
        print('Here are those of the characters under consideration')
        print(f'  whose name starts with {start}:')
        # Get the length of the longest name in the filtered dictionary
        max_len = max(len(name) for name in filtered)
        # Sorting filtered dictionary by the keys (names)
        # Iterate through the sorted dictionary and print left-aligned names with automatic spacing
        for name, char in sorted(filtered.items()):
            print(f'{name:<{max_len}}: {char}')
    else:
        print('None of the characters you want me to consider')
        print(f'  has a name that starts with {start}.')