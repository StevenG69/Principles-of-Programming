# Written by Eric Martin for COMP9021

import unicodedata

while True:
    try:
        a, b = input('Please input two integers a and b with 0 <= a <= b <= 1114111,'
                     '\n       both integers being separated by ~, with possibly'
                     '\n       spaces and tabs before and after the numbers:'
                     '\n       '
                    ).split('~')
        a, b = int(a), int(b)
        if not (0 <= a <= b <= 1114111):
            raise ValueError
        break
    except ValueError:
        print('\nIncorrect input, try again!')
n = b - a + 1
names_to_codes = {}
nb_of_named_characters = 0
for i in range(a, b + 1):
    try:
        name = unicodedata.name(chr(i))
        names_to_codes[name] = i
        nb_of_named_characters += 1
    except ValueError:
        pass
names = list(names_to_codes)
names.sort()
if a == b:
    if not nb_of_named_characters:
        print(f'\n{a} is not the code point of a named character.')
    else:
        print(f'\n{a} is the code point of a named character.')
else:
    if not nb_of_named_characters:
        print(f'\nNo number between {a} and {b}'
              '\n  is the code point of a named character.'
             )
    elif nb_of_named_characters == n:
        print(f'\nAll numbers between {a} and {b}'
              '\n  are code points of named characters.'
)
    else:
         print(f'\nAmongst the numbers between {a} and {b},'
               f'\n  {nb_of_named_characters * 100 / n:.2f}% '
               'are code points of named characters.'
             )
if nb_of_named_characters:
    initial_segment = input('\nEnter a string: ')
    selected_names = [name for name in names if name.startswith(initial_segment)]
    if not selected_names:
        print('\nNone of the characters you want me to consider'
              f'\n  has a name that starts with {initial_segment}.'
             )
    else:
        print('\nHere are those of the characters under consideration'
              f'\n  whose name starts with {initial_segment}:'
             )
        width = max(len(w) for w in selected_names)
        for name in selected_names:
            print(f'{name:{width}}:', chr(names_to_codes[name]))