f = open('../../common/position','r')
list = []
for line in f:
    coordinate = (int(line.split()[0]), int(line.split()[1]))
    list.append(coordinate)
f.close()

file = open('../RSS_Location','w')
for i in range(113):
    for j in range(3):
        file_name = '../../survey/'+str(i+1)+'/wifi_recored'+str(j)
        f = open(file_name,'r')
        header = f.readline()
        begin_index = header.index('BSSID')
        end_index = header.index('RSSI')+3
        records = []
        for line in f:
            tmp = line[begin_index:end_index].split()
            try:
                record = (tmp[0], int(tmp[1]), list[i])
                records.append(record)
                file.write(tmp[0] +" "+ tmp[1] +" "+ list[i].__str__() +'\n')
            except IndexError:
                pass
            except ValueError:
                pass
        f.close()
file.close()

