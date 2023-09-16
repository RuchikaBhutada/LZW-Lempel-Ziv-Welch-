#Import Libraries
import sys
import struct
import math


#Decoding
def lzw_decode(codes):

    #Initializing dictionary with (ASCII character, ASCII value) as (key,value) pair
    strings = dict((i, chr(i)) for i in range(256))
    code = 256
    prev_code = codes[0]
    string = strings[prev_code]
    result = string
    prev_string = string
    for curr_code in codes[1:]:
        if curr_code in strings:
            string = strings[curr_code]
        elif curr_code == code:
            string = prev_string + prev_string[0]
        else:
            raise ValueError("Bad compressed code: {}".format(curr_code))

        result += string
        strings[code] = prev_string + string[0]
        code += 1
        prev_string = string

    return result

#Reading filename and fixed length bit from command line
input_file, n_bits = sys.argv[1:3]

#Reading data from the encoded input file
f = open(input_file, "rb")
encoded_data = []

#Unpacking the data from 2 bytes (16 bits) to 1 byte(8 bits)
while True:
    input_data = f.read(2)
    if len(input_data) != 2:
        break
    (data, ) = struct.unpack('>H', input_data)
    encoded_data.append(data)

#Defining maximum table size
max_table_size = math.pow(2, int(n_bits))

#calling lzw_decode function to decode the encoded data
decoded_data = lzw_decode(encoded_data)

#Writing the output to a file
output = input_file.split(".")[0]
output_filename = open(output+"_decoded.txt","w")
for comp in decoded_data:
    output_filename.write(comp)

#Closing all the file streams
output_filename.close()
f.close()

