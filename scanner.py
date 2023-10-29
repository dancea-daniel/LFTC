from LFTC.symb_table import SymbolTable
import re, sys

separator = ['(', ')', '[', ']', '{', '}', ' ', ';']
operator = ['+', '-', '/', '*', '=', '<=', '>=', '>', '<', '==', '!=', '->', '%']
reserved_words = ['big_numbers', 'many_letters', 'long_things', 'loop', 'assuming', 'otherwise', 'show', 'input', 'accurate', 'erroneous', 'if', 'else']

PIF = []
st = SymbolTable(size=5)


def is_valid_identifier(input_string):
    pattern = r'^[a-z][a-zA-Z_1-9]*$'
    return bool(re.match(pattern, input_string))


def is_valid_string(input_string):
    pattern = r'^[a-zA-Z_0-9\s]*$'
    return bool(re.match(pattern, input_string))


def is_valid_number(input_string):
    pattern = r'^[+-]?\d+?$'
    return bool(re.match(pattern, input_string))


def check_lexical():
    with open('p3err.txt', 'r') as file:
        my_word = ''
        line_nr = 1
        char_nr = 0

        while True:
            char = file.read(1)
            char_nr += 1
            if not char:
                break

            # string constant
            if char == "'":
                char = file.read(1)
                while char != "'":
                    if not char:
                        # error
                        raise Exception(f"Lexical error: {my_word}  at line: {line_nr} nr: {char_nr}")
                    my_word += char
                    char = file.read(1)

                if is_valid_string(my_word):
                    index, value = st.insert(my_word)
                    if index is None:
                        index, value = st.lookup(my_word)
                    PIF.append(("CONSTANT", (index, value)))

                my_word = ''
                char = file.read(1)

            if char in operator:
                # work with word
                if my_word in reserved_words:
                    PIF.append((my_word, -1))

                elif is_valid_identifier(my_word):
                    index, value = st.insert(my_word)
                    if index is None:
                        index, value = st.lookup(my_word)
                    PIF.append(("IDENTIFIER", (index, value)))
                elif is_valid_number(my_word):
                    index, value = st.insert(my_word)
                    if index is None:
                        index, value = st.lookup(my_word)
                    PIF.append(("CONSTANT", (index, value)))
                elif my_word != '':
                    raise Exception(f"Lexical error: {my_word}  at line: {line_nr} nr: {char_nr}")

                my_word = char
                char = file.read(1)
                char_nr += 1

                # possible complex operator such as ==
                if char in operator:
                    my_word += char
                    # complex operator
                    if my_word in operator:
                        PIF.append((my_word, -1))
                        my_word = ''
                    # case of >-1
                    elif char == '+' or char == '-':
                        char = file.read(1)
                        if not char:
                            raise Exception(f"Lexical error: {my_word}  at line: {line_nr} nr: {char_nr}")

                        char_nr += 1
                        # if number then continue
                        if char.isdigit():
                            PIF.append((my_word[0], -1))
                            new_word = my_word[1] + char
                            my_word = new_word
                        elif my_word[1] == '-' and char == '>':
                            PIF.append((my_word[0], -1))
                            new_word = my_word[1] + char
                            my_word = new_word
                        # error
                        else:
                            raise Exception(f"Lexical error: {my_word}  at line: {line_nr} nr: {char_nr}")

                    else:
                        raise Exception(f"Lexical error: {my_word}  at line: {line_nr} nr: {char_nr}")

                    char = ''
                elif char.isdigit():
                    my_word += char
                    char = ''

                # possible end of file
                elif not char:
                    PIF.append((my_word, -1))
                    # work with word
                    break
                else:
                    PIF.append((my_word, -1))
                    my_word = ''

            if char in separator:
                if my_word in reserved_words:
                    PIF.append((my_word, -1))

                elif is_valid_identifier(my_word):
                    index, value = st.insert(my_word)
                    if index is None:
                        index, value = st.lookup(my_word)
                    PIF.append(("IDENTIFIER", (index, value)))
                elif is_valid_number(my_word):
                    index, value = st.insert(my_word)
                    if index is None:
                        index, value = st.lookup(my_word)
                    PIF.append(("CONSTANT", (index, value)))
                elif my_word in operator:
                    PIF.append((my_word, -1))
                elif my_word != '':
                    raise Exception(f"Lexical error: {my_word}  at line: {line_nr} nr: {char_nr}")

                PIF.append((char, -1))
                my_word = ''

            elif char == '\n':
                line_nr += 1
                char_nr = 0
            elif char:
                my_word += char

    print("lexically correct")


if __name__ == "__main__":
    try:
        with open("p3_err_out.txt", "w") as file:
            check_lexical()
            print(f"the PIF: {PIF}", file=file)
            print(f"the ST: {st}", file=file)
    except Exception as e:
        with open("p3_err_out.txt", "a") as file:
            print(e, file=file)


