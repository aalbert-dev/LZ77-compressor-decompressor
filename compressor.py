import csv, sys, os, numpy, math, decimal
"""
@author     Arjun Albert
@email      aalbert@mit.edu
@modified   11/9/2020
@notes      COSI 175 PA1 LZ77 Compressor
"""

"""
Read file name as a path relative to where the program was run.
Returns a list containing each line of the file as a string element of the list. 
"""
def get_file_as_text(fname):
    flines = []
    f = open(os.path.join(sys.path[0], fname),'r')
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
    [[chars.append(char) for char in line] for line in lines]
    return chars


"""
Joins a list of characters into a single string.
The performance of this greatly affects the overall performance of the algorithmn.
"""
def list_to_str(l):
    return ''.join(l)


"""
Search for a match to a string in the sliding dictionary.
Returns the offset of the match in the dictionary and the length of the match.
"""
def find_in_dict(substring, dict_window):
    dict_as_string = list_to_str(dict_window)
    string_for_search = list_to_str(substring)
    substring_index = dict_as_string.find(string_for_search)
    if substring_index > -1:
        return (substring_index, len(string_for_search))
    return None


"""
For each prefix in the buffer window search for a match in the dictionary window.
Finds the longest length prefix match by searching for each string in increasing order of length.
Returns in the match offset and length if a match is found.
"""
def find_longest_match(buffer_window, dict_window):
    longest_match = ''
    for i in range(0, len(buffer_window)):
        current_substring = buffer_window[0: i + 1]
        str_dict_pos = find_in_dict(current_substring, dict_window)
        if str_dict_pos:
            longest_match = str_dict_pos
    return longest_match


"""
Keep track of a cursor in the list of characters of the input string.
Set a buffer window and dictionary window based on the cursor position.
Search for the longest prefix in the buffer window that is a match in the dictionary window.
If there is a match we encode it using the offset and length in dictionary and otherwise we 
encode the character ascii as bits. Repeat this until we have compressed the entire input string.
"""
def apply_sliding_window_compression(chars):
    compressed_string = ''
    cursor_start = 0
    while cursor_start < len(chars):
        """
        Log the current precent of progress on compression the file.
        """
        percent = 100.0 * cursor_start / len(chars)
        log(str(round(percent, 2)) + '%')
        """
        Set the buffer and dictionary window based on the current cursor position.
        Ensure the windows do not wrap around the list or get null pointer refs.
        """
        buffer_cursor_end = min(cursor_start + WINDOW_SIZE, len(chars) - 1)
        dict_window_start = max(cursor_start - DICT_SIZE, 0)
        buffer_window = chars[cursor_start: buffer_cursor_end]
        dict_window = chars[dict_window_start: cursor_start]
        """
        Search for the longest prefix match in the dictionary from the buffer. 
        Return match as a tuple of offset and length of the match in the dictionary window.
        """
        match = find_longest_match(buffer_window, dict_window)
        next_match_or_char = ''
        if match:
            """
            If there was a match we encode it as an offset, length, and next character.
            Add the encoded match to the compressed string.
            """
            match_string = chars[dict_window_start + match[0]: dict_window_start + match[0] + match[1]]
            next_char = chars[cursor_start + len(match_string)]
            cursor_start += len(match_string) + 1
            next_match_or_char = get_match_compressed_form(match, next_char)
        else:
            """
            If there was no match we encode the next character as ascii bits.
            Add the encoded character to the compressed string.
            """
            next_match_or_char = get_char_compressed_form(chars[cursor_start])
            cursor_start += 1
        compressed_string += next_match_or_char
    return compressed_string


"""
Convert a match (offset, length) and next character into 25 bits.
Return the binary string.
"""
def get_match_compressed_form(match, next_char):
    return '1' + get_bits(match[0], WINDOW_SIZE) + get_bits(match[1], 4) + get_bits(ord(next_char), 8)


"""
Convert a character into 8 bit string.
Return the binary string.
"""
def get_char_compressed_form(char):
    return '0' + get_bits(ord(char), 8)


"""
Convert an integer into binary with length = base.
"""
def get_bits(decimal, base):
    f = '{:0' + str(base) + 'b}'
    return f.format(decimal)


"""
Convert a binary string with base = base to an integer.
"""
def get_decimal(bits, base):
    return int(bits, base)


"""
Compress a file given a filename.
Convert the file into a single string and then run the sliding window compression algorithmn.
Write the compressed format to a file called compressed_<FILE_NAME>.txt.
"""
def compress(fname):
    lines = get_file_as_text(fname)
    chars = file_as_chars(lines)
    compressed_format = apply_sliding_window_compression(chars)
    write_to_text_file('good_compressed_' + fname, compressed_format)


"""
Compress each file that has been passed as a command line argument.
"""
def run():
    for arg in sys.argv[1:]:
        compress(arg)


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
Run the compression method.
"""
run()