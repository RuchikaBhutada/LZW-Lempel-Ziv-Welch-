#Import Libraries
import sys
import struct
import math


#Encoding
def lzw_encode(data):

    #Initializing dictionary with (ASCII character, ASCII value) as (key,value) pair
    codes = dict((chr(i), i) for i in range(256))
    code = 256
    result = []
    string = ""

    for char in data:
        if string + char in codes:
            string += char
        else:
            if string in codes.keys():
                result.append(codes[string]) 
                if len(codes) <= max_table_size:
                    codes[string + char] = code
                    code += 1
                string = char
            else:
                raise ValueError("Symbol is not defined. Unknown Symbol: {}".format(string))

    if string:
        result.append(codes[string])

    return result


#Reading filename and fixed length bit from command line
input_file, n_bits = sys.argv[1:3]

#Reading data from the input file
f = open(input_file, "r")
input_data = f.read()

#Defining maximum table size
max_table_size = math.pow(2, int(n_bits))

#calling lzw_encode function to encode the data
encoded_data = lzw_encode(input_data)

#Printing the encoded data for easy debugging
print(encoded_data)

#Writing the output to a file
output = input_file.split(".")[0]     

#'wb' to write the output in binary mode
output_filename = open(output+".lzw","wb")
for comp in encoded_data:
    output_filename.write(struct.pack('>H', int(comp)))


#Closing all the file streams
output_filename.close()
f.close()
      