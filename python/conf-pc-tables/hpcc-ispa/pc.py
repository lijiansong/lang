global_info = {}
ispa_pc_set = set()
with open('ispa.txt', 'r') as ispa_reader:
    pc_list = ispa_reader.readlines()
    for pc in pc_list:
        pc = pc.rstrip('\n')
        info = pc.split('\t')
        name, institute, country = info[0], info[1], info[2]
        print('{n}, {i}, {c}'.format(n=name, i=institute, c=country))
        ispa_pc_set.add(name)
        global_info[name] = (institute, country)

print('------------------------------------------------------------')
hpcc_pc_set = set()
with open('hpcc.txt', 'r') as hpcc_reader:
    pc_list = hpcc_reader.readlines()
    for pc in pc_list:
        pc = pc.rstrip('\n')
        info = pc.split('\t')
        name, institute, country = info[0], info[1], info[2]
        print('{n}, {i}, {c}'.format(n=name, i=institute, c=country))
        hpcc_pc_set.add(name)
        global_info[name] = (institute, country)

print('------------------------------------------------------------')
print('ISPA PC # {}'.format(len(ispa_pc_set)))
print('HPCC PC # {}'.format(len(hpcc_pc_set)))
print('ISPA & HPCC #: {}'.format(len(ispa_pc_set & hpcc_pc_set)))
print('------------------------------------------------------------')
hpcc_ispa_common_pc = ispa_pc_set & hpcc_pc_set
for pc_name in hpcc_ispa_common_pc:
    print('{n}, {i}, {c}'.format(n=pc_name,
                                 i=global_info[pc_name][0],
                                 c=global_info[pc_name][1]))
