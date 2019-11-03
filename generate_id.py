import re


file_output = open('id_pattern1.txt', 'a')
file_input = open('national_identifiers.txt', 'r')
id = []
lines = file_input.readlines()

for line in lines:
    for n in ['R', 'V', '']:
        for a in ['HRB', 'HRA', 'GnR', 'PR', 'VR']:
            for x in range(0, 1000000):
                for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ':
                    for j in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ':
                        id = []
                        id.append(line.strip('\n'))
                        id.append(n)
                        id.append('_')
                        id.append(a)
                        id.append(x)
                        id.append(i)
                        id_number = ''.join(map(str, id))
                        id_number.strip()
                        file_output.write(id_number, '\n')

file_input.close()
file_output.close()
