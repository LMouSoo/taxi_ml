import numpy
import csv
import sys
import os
from math import radians,sin,cos,atan2,sqrt,acos,asin,degrees

"""
Author : Kim Hyun-Soo (soo9211@gmail.com, University of Seoul)

#Some calculations on the basis of a spherical earth(ignoring ellipsoidal effects).
#The earth is very slighty ellipsoidal, using a spherical model gives errors typically up to 0.3%
#You want more information about spherical model error, please see this link = https://gis.stackexchange.com/questions/25494/how-accurate-is-approximating-the-earth-as-a-sphere#25580
#if You want a calculation that uses the ellipsoidal effects, please see this link = http://www.movable-type.co.uk/scripts/latlong-vincenty.html (Vincenty solutions of geodesics on the ellipsoid)


#Reference

#Calculate distance, bearing and more between Latitude/Longitude points (http://www.movable-type.co.uk/scripts/latlong.html)

"""

def gps_to_d(lon1,lat1,lon2,lat2,formula='haversine'):
    R = 6371000
    p1 = radians(float(lat1)*0.0000001)
    p2 = radians(float(lat2)*0.0000001)
    dp = radians(float(lat2)*0.0000001-float(lat1)*0.0000001)
    dl = radians(float(lon2)*0.0000001-float(lon1)*0.0000001)

    if formula == 'haversine' : # haversine formula - basic
        a = sin(dp/2)**2 + cos(p1)*cos(p2)*(sin(dl/2)**2)
        c = 2*atan2(sqrt(a),sqrt(1-a))
        d = R*c

    if formula == 'SLC' : # Spherical Law of Cosines - Simple.. but maybe slightly slower than the haversine //  error ~ 0.0000001
        d = acos(sin(p1)*sin(p2) + cos(p1)*cos(p2)*cos(dl))*R

    if formula == 'EA' : # Equirectangular approximation - performance is good / accuracy is very bad // error ~ 0.1
        x = dl*cos((p1+p2)/2)
        y = dp
        d = sqrt(x**2 + y**2)*R

    return d



def d_to_gps(lon,lat,brng,d):
    lon = radians(float(lon)*0.0000001)
    lat = radians(float(lat)*0.0000001)
    brng = radians(brng)
    R = 6371000

    r_lat = asin(sin(lat)*cos(d/R) + cos(lat)*sin(d/R)*cos(brng))
    r_lon = lon + atan2(sin(brng)*sin(d/R)*cos(lat), cos(d/R)-sin(lat)*sin(r_lat))

    r_lat = degrees(r_lat)
    r_lon = degrees(r_lon)

    return int(r_lon*10000000),int(r_lat*10000000)



def chk_in_kor(lon,lat):
    if int(lon) < 1295847220 and int(lon) > 1261116670 and int(lat) > 342922220 and int(lat) < 386111110 :
        return 1
    else :
        return 0


    
def make_source_list(source_dir='../source', folder_list='all', file_list='all', file_extension='.DAT', test=False):
    if test == True:
        folder_name = os.listdir(source_dir)
        folder_name.sort()
        folder_name = folder_name[0]
        file_name = os.listdir(source_dir+'/'+folder_name)
        file_name.sort()
        for i in range(len(file_name)):
            if '.DAT' == os.path.splitext(file_name[i])[1]:
                file_name = file_name[i]
                break
        else:
            print("errer oucurr")

        return [source_dir+'/'+folder_name+'/'+file_name]

    return_list = []

    if folder_list=='all':
        folder_list=os.listdir(source_dir)
        folder_list.sort()
    for folder_name in folder_list:
        if file_list=='all':
            file_list=os.listdir(source_dir+'/'+folder_name)
            file_list.sort()
        for file_name in file_list:
            if '.DAT' != os.path.splitext(file_name)[1]:
                continue
            return_list.append(source_dir+'/'+folder_name+'/'+file_name)

    return return_list
