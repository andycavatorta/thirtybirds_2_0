
import sys
import x24bitParallelPort

while True:
    sys.stdout.write("please input a 23-bit binary number")
    input_raw = sys.stdin.readline()
    input_trimmed = input_raw[:-1]
    #input_padded =  '{0:03d}'.format(4)
    if len(input_trimmed) != 23:
        print "input is not 23 bits. try again"
    else:
        x24bitParallelPort.send(list(input_trimmed))
