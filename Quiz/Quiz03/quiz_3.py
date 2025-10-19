# Written by Hongyin Zhou for COMP9021
import unicodedata

while True:
    try:
        print("Please input two integers a and b with 0 <= a <= b <= 1114111,")
        print("       both integers being separated by ~, with possibly")
        print("       spaces and tabs before and after the numbers:")
        integers = input("   ")
        integers = "".join(integers.split()).split("~")
        if len(integers) != 2:
            raise ValueError
        a, b = int(integers[0]), int(integers[1])
        if not (0 <= a <= b <= 1114111):
            raise ValueError
        break
    except ValueError:
        print("Incorrect input, try again!")

string = b - a + 1
vs = 0
dict = {}
for i in range(a, b + 1):
    try:
        s = chr(i)
        name = unicodedata.name(s)
        vs += 1
        dict[name] = s
    except ValueError:
        pass

print()
if string == 1:
    if vs == 1:
        print(f'{a} is the code point of a named character.')
    else:
        print(f'{a} is not the code point of a named character.')
elif string > 1:
    if vs == 0:
        print(f'No number between {a} and {b}\n is the code point of a named character.')
    elif string == vs:
        print(f'All number between {a} and {b}\n are code points of a named character.')
    elif string > vs:
        print(f'Amongst the numbers between {a} and {b},')
        print(f'  {(vs / string) * 100:.2f}% are code points of a named character.')

print()
start = input("Enter a string: ")
print()

filtered = {name: char for name, char in dict.items() if name.startswith(start)}

if filtered:
    print('Here are those of the characters under consideration')
    print(f'  whose name starts with {start}:')
    for name, char in sorted(filtered.items()):
        print(f'{name}: {char}')
else:
    print('None of the characters you want me to consider')
    print(f'  has a name that starts with {start}.')
