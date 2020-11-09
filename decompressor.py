import csv, sys, os, numpy, math, decimal
"""
@author     Arjun Albert
@email      aalbert@mit.edu
@modified   11/9/2020
@notes      COSI 175 PA1 LZ77 Decompressor
"""

"""
Read file name as a path relative to where the program was run.
Returns a list containing each line of the file as a string element of the list. 
"""
def get_file_as_text(fname):
    flines = []
    f = open(os.path.join(sys.path[0], fname), 'r')
    for x in f:
        flines.append(x)
    return flines


"""
Read file name and take as input text.
Writes the input text to the file.
"""
def write_to_text_file(fname, formatted_text):
    write_file = open(os.path.join(sys.path[0], fname), 'w') 
    write_file.write(formatted_text)
    write_file.close()

"""
Input a list of strings representing the file to be compressed.
Returns a single list of all the characters in the file. 
"""
def file_as_chars(lines):
    chars = []
    for line in lines:
        for char in line:
            chars.append(char)
    return chars


"""
Joins a list of characters into a single string.
The performance of this greatly affects the overall performance of the algorithmn.
"""
def list_to_str(l):
    return ''.join([str(i) for i in l])


"""
Convert an integer into binary with length = base.
"""
def get_bits(decimal, base):
    f_string = '{:0' + str(base) + 'b}'
    return f_string.format(decimal)


"""
Convert a binary string with base = base to an integer.
"""
def get_decimal(bits, base):
    return int(bits, base)


"""
Iterates through the compressed string checking each flag bit for a match or character encoding.
For each match we decode the match from the sliding dictionary using the offset and length of the match from the start index of the dictionary.
For each next character we simply decode the bits as an ascii number and convert it to a character.
Regardless of if we have a match or a character we add it to the sliding dictionary and add it to the decompressed string. 
Repeat this until the whole compressed string has been decompressed. 
"""
def decompress(s):
    decompressed_str = ''
    cursor = 0
    while cursor < len(s):
        flag_bit = s[cursor]
        if flag_bit == '0':
            """
            compressed representation = [flag bit][next char bits]
            compressed representation = [1 flag bit][8 bits for the next character]
            """
            char_bits = s[cursor + 1: cursor + 9]
            parsed_str = decompress_char(char_bits)
            cursor += 9
        else:
            """
            compressed representation = [flag bit][offset bits][length bits][next char bits]
            compressed representation = [1 flag bit][12 bits for offset in dictionary of match][4 bits for length of match in dictionary][8 bits for the next character]
            """
            offset_bits = s[cursor + 1: cursor + 17]
            length_bits = s[cursor + 17: cursor + 21]
            next_char_bits = s[cursor + 21: cursor + 29]
            next_char = chr(get_decimal(next_char_bits, 2))
            parsed_str = decompress_match(offset_bits, length_bits, decompressed_str) + next_char
            cursor += 29
        decompressed_str += parsed_str
    return decompressed_str


"""
Convert an 8 bit character ascii integer into a character.
"""
def decompress_char(c):
    ascii_val = get_decimal(c, 2)
    return chr(ascii_val)


"""
Get the integer representation of the offset and length bits.
Get the character for the ascii next character bits.
Grab the match from the sliding dictionary using the length and offset.
"""
def decompress_match(offset, length, dict_str):
    sized_dict = dict_str[-DICT_SIZE:]
    offset_val = get_decimal(offset, 2)
    length_val = get_decimal(length, 2)
    match_str = sized_dict[offset_val: offset_val + length_val]
    return match_str


"""
Convert each file into a list of strings for each line in the file.
Convert the list of strings into a list of characters for the whole file.
Convert the list of characters into a single string.
Run the decompression algorithm on the string.
Print the decompressed file to the command line.
"""
def decompress_file(fname):
    lines = get_file_as_text(fname)
    chars = file_as_chars(lines)
    compressed_format = list_to_str(chars)
    decompressed_str = decompress(compressed_format)
    log(decompressed_str)


"""
Decompress each file that has been passed as a command line argument.
"""
def run():
    for arg in sys.argv[1:]:
        decompress_file(arg)


"""
Use for pretty logging.
"""
def log(msg):
    print(msg)


"""
Dictionary size and window size parameters.
"""
WINDOW_SIZE = 12
DICT_SIZE = 2 ** WINDOW_SIZE


"""
Run the decompression method.
"""
run()