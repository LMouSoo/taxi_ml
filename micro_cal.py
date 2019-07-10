import numpy as np
import os
import taxi

orders = 23
ext = 2**orders
origin = np.array([1265732668,371220608])

source_dir = "../source"
folder_list=np.array(os.listdir(source_dir))
folder_list.sort()


error_log = ""


#for order in range(0,orders):
for order in [5]:     #limit 18
    flag = False
    mat = np.full((2**order,2**order), False)
#    for folder_name in folder_list:
    for folder_name in ["2017-05-21"]:
        file_list=np.array(os.listdir(source_dir+"/"+folder_name))
        file_list.sort()
#        for file_name in file_list:
        for file_name in ["022730.DAT"]:
            if ".DAT" != os.path.splitext(file_name)[1]:
                continue
            print(f"{order} / {folder_name} /  {file_name}")
#            try:
            data_file=np.loadtxt(source_dir+"/"+folder_name+"/"+file_name, delimiter=",", dtype=np.int64)
#            except:
#                error_log += f"{order} / {folder_name} /  {file_name}\n"
#                continue
            for data in data_file:
                if origin[0] > data[1] or origin[0]+ext < data[1] or origin[1] > data[2] or origin[1]+ext < data[2]:
                    continue
                lon, lat = (data[1:3]-origin)/(2**(23-order))
                lon = int(lon)
                lat = int(lat)
                mat[lat][lon] = True
                if mat.min() :
                    flag = True
                    break
            if flag :
                break
        if flag :
            break
    save_file = open(f"{order}.csv","a")
    percent = mat.sum()/((2**order)**2)
    save_file.write(f"{order}, {percent}\n")
    save_file.close()

print(error_log)
