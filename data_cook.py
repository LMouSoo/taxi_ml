import os
import taxi
import csv
import datetime



def progress_print(source_name, index_number, index_len, before):
    tmp = int(index_number/index_len*100)
    if tmp != before:
        print(f"{source_name}, {tmp}%")
        return tmp
    return before

#['taxi_id', 'longitude', 'latitude', 'altitude', 'time', 'direction', 'speed','1','passanger_inout']

taxi_dic = {}

source_list = taxi.make_source_list(test=0)
before = -1
save_file = open("cook_data.csv","a")

for index_number, source_name in enumerate(source_list):
    before = progress_print(source_name, index_number, len(source_list), before)
    source_file = open(source_name,'r')
    csv_df = csv.reader(source_file, delimiter=',')
    for row in csv_df:
        taxi_id, longitude, latitude, altitude, time, direction, speed, _, passanger_inout = row
        taxi_id = int(taxi_id)
        passanger_inout = int(passanger_inout)
        if not taxi.chk_in_kor(longitude,latitude):
            continue
        if taxi_id in taxi_dic:
            taxi_cursor=taxi_dic[taxi_id]
            if passanger_inout == taxi_cursor[4]:
                continue
            if passanger_inout:
                taxi_dic[taxi_id]=(longitude, latitude, time, direction, passanger_inout)
            else:
                start_time = datetime.datetime.strptime(taxi_cursor[2],'%Y%m%d%H%M%S')
                end_time = datetime.datetime.strptime(time,'%Y%m%d%H%M%S')
                tmp_time = (end_time-start_time).total_seconds()

                if tmp_time > 180 and tmp_time < 600000 :
                    save_file.write(f"{taxi_cursor[0]},{taxi_cursor[1]},{taxi_cursor[2]},{taxi_cursor[3]},{longitude},{latitude}\n")
                del taxi_dic[taxi_id]
        else:
            if passanger_inout == 0:
                taxi_dic[taxi_id]=(longitude, latitude, time, direction, passanger_inout)

save_file.close()
source_file.close()
