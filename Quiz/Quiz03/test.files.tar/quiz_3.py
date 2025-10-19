# Written by Hongyin Zhou for COMP9021
import unicodedata

while True:
    try:
        print("Please input two integers a and b with 0 <= a <= b <= 1114111,")
        print("       both integers being separated by ~, with possibly")
        print("       spaces and tabs before and after the numbers:")
        integers = input("       ")
        integers = "".join(integers.split()).split("~")
        if len(integers) != 2:
            raise ValueError
        a, b = int(integers[0]), int(integers[1])
        if not (0 <= a <= b <= 1114111):
            raise ValueError
        break
    except ValueError:
        print("\nIncorrect input, try again!")

str_count = b - a + 1
vstr_count = 0
s_dict = {}

for i in range(a, b + 1):
    try:
        s = chr(i)
        name = unicodedata.name(s)
        vstr_count += 1
        s_dict[name] = s
    except ValueError:
        pass
print()

if str_count == 1:
    print(f'{a} is {"not " if vstr_count == 0 else ""}the code point of a named character.')

elif str_count > 1:
    if vstr_count == 0:
        print(f'No number between {a} and {b}\n  is the code point of a named character.')
    elif str_count == vstr_count:
        print(f'All numbers between {a} and {b}\n  are code points of named characters.')
    elif str_count > vstr_count:
        print(f'Amongst the numbers between {a} and {b},')
        print(f'  {(vstr_count / str_count) * 100:.2f}% are code points of named characters.')

print()
start = input("Enter a string: ")
print()

filtered = {name: char for name, char in s_dict.items() if name.startswith(start)}

if filtered:
    print('Here are those of the characters under consideration')
    print(f'  whose name starts with {start}:')
    max_len = max(len(name) for name in filtered)
    for name, char in sorted(filtered.items()):
        print(f'{name:<{max_len}}: {char}')
else:
    print('None of the characters you want me to consider')
    print(f'  has a name that starts with {start}.')
