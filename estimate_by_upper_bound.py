import re


file_input = open('valid_id_from_site.txt', 'r')
file_output = open('estimated_id.txt', 'a+')

lines = file_input.readlines()
for line in lines:
    line = line.strip('\n')
    parts = re.split('_', line)
    index = parts[-1]
    for reg in ['HRB', 'HRA', 'GnR', 'PR', 'VR']:
        index = re.sub(reg, '', index)

    index = re.sub('\D{,2}', '', index)
    pattern = re.split(index, line) # here can collision if index contains in XJustiz-ID then len(pattern) can be only 2 or 3
    for i in range(0, int(index) + 1):
        id = []
        if len(pattern) == 3:
            id.append(pattern[0])
            id.append(i)            
            id.append(pattern[1])
            id.append(i)
            id.append(pattern[2])
        else:
            id.append(pattern[0])
            id.append(i)
            id.append(pattern[1])

        id_number = ''.join(map(str, id))
        if not(id_number in file_output.read()):
            file_output.write(id_number+'\n')

file_input.close()
file_output.close()

