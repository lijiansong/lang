import csv

# format of input csv: delimited by space
# <testname> <time step> <space step> <nbpml> <dimension>
# <chipname> <environment specification>
# <time order> <space order> <time used>
# .
# .
# .
# look at xeon.csv for example

glops_correction = 1000000000
#max bandwidth and flops dictionary
# key = chip name
# value = (bw, flop)
bfd = {'none' : (0, 0)}
# xeon
cname = 'xeon'
bfd[cname] = (44.27, 241.5)
# xeon phi
cname = 'xeon-phi'
bfd[cname] = (166, 1010)
# KNL
cname = 'KNL'
bfd[cname] = (366, 3000)

#totoal ops dictionary
# key = (name of test, time order, space order)
# value = (ops, oi)
topsd = {('none', 0, 0) : 0}
#acoustic2d
tname = 'acoustic3d'
topsd[(tname, 2, 2)] = (27, 1.6875)
topsd[(tname, 2, 4)] = (39, 2.4375)
topsd[(tname, 2, 6)] = (51, 3.1875)
topsd[(tname, 2, 8)] = (63, 3.9375)
topsd[(tname, 2, 10)] = (75, 4.6875)
topsd[(tname, 2, 12)] = (87, 5.4375)
topsd[(tname, 2, 14)] = (99, 6.1875)
topsd[(tname, 2, 16)] = (111, 6.9375)
topsd[(tname, 4, 4)] = (50, 3.125)
topsd[(tname, 4, 6)] = (62, 3.875)
topsd[(tname, 4, 8)] = (74, 4.625)
topsd[(tname, 4, 10)] = (86, 5.375)
topsd[(tname, 4, 12)] = (98, 6.125)
topsd[(tname, 4, 14)] = (110, 6.875)
topsd[(tname, 4, 16)] = (122, 7.625)

def read_csv(filepath):
    with open(filepath, 'rb') as f:
        mycsv = csv.reader(f, delimiter=' ')
        result = []
        i = 0
        for row in mycsv:
            if i == 0:
                meta = [row[0]] + map(int, row[1:]) 
                print(meta)
                result.append(meta)
                i = 1
            elif i == 1:
                print row
                env = map(lambda c : '\_' if c == '_' else c, ' '.join(row[1:]))
                result.append([row[0], env])
                i = 2
            else:
                result.append(map(float, row))
        f.close()
        return result


def get_bw_f(chipname):
    return bfd[chipname]

def get_oi(testname, time_order, space_order):
    (_, oi) = topsd[testname, time_order, space_order]
    return oi


def calc_flops(testname, space, time_step, time_order, space_order, time,
               padding, dimension):
    (ops, _) = topsd[testname, time_order, space_order]
    return ((space + padding - space_order) ** dimension * time_step * ops)\
           / (time * glops_correction)

