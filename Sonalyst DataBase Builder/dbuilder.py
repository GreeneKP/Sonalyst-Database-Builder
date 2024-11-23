#!/usr/bin/env python3

import pandas as pd
from requests import get, Session, post
import time
from datetime import datetime, timedelta
import os



uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"



siteCred = {'identity': "space.state@aol.com", 'password': "123SSptaactee123!"}


with Session() as session:
    resp = session.post(uriBase + requestLogin, data = siteCred)
    if resp.status_code != 200:
        raise MyError(resp, "POST fail on login")

    seshcook = resp.headers['Set-Cookie']
    seshcook = seshcook.split(' ')[0][:-1]

hdrs2 = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
'Authorization': 'TOK:space.state@aol.com',
'accept-encoding':'gzip, deflate, br, zstd',
'accept-language':'en-US,en;q=0.9,es;q=0.8',
'cache-control':'max-age=0',
'cookie':f'spacetrack_csrf_cookie=8u4fvh6rr0rr9bm68ovuf6h2l2v728r2; {seshcook}',
'priority':'u=0, i',
'referer':'https://www.space-track.org/auth/login',
'sec-ch-ua':'"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
'sec-ch-ua-mobile':'?1',
'sec-ch-ua-platform':'"Android"',
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"'}

today = datetime.today()
today=str(today)
today=today[:10]

onelist = []
tenlist = [37810, 42814, 39476, 37749, 45920, 27718, 41589, 38991, 34111, 32487]
twentylist = [40732, 37810, 40364, 42814, 36101, 39476, 39498, 37749, 37933, 45920, 39216, 27718, 42741, 41589, 33278, 38991, 37602, 34111, 33055, 32487]
thirtylist = [44334, 54048, 37810, 43700, 47306, 42814, 38245, 39034, 39476, 38098, 41552, 37749, 39460, 42951, 45920, 36744, 40940, 27718, 32252, 37834, 41589, 28446, 39688, 38991, 42432, 40874, 34111, 43039, 37816, 32487]
fortylist = [32299, 40732, 36582, 37810, 39215, 40364, 41384, 42814, 43632, 36101, 43698, 39476, 41747, 39498, 40880, 37749, 41028, 37933, 32019, 45920, 38331, 39216, 41836, 27718, 35756, 42741, 28187, 41589, 28252, 33278, 37809, 38991, 49055, 37602, 38867, 34111, 37264, 33055, 36830, 32487]
fiftylist = [38652, 41310, 28946, 44479, 37810, 32294, 29526, 41186, 29270, 42814, 49333, 44035, 37393, 42698, 39476, 38740, 41793, 39508, 45026, 37749, 42815, 35696, 46112, 41903, 45920, 42917, 41034, 43611, 28899, 27718, 25924, 43633, 40882, 26580, 41589, 39127, 36516, 28702, 33373, 38991, 40733, 43562, 38749, 43175, 34111, 28945, 42950, 40875, 32794, 32487]

specified_sat = input('\n\nPlease enter the 5-digit NORAD SCC number for a specific satellite in GEO. Simply hit "Enter" if you have no specific satellite in mind to skip to the next step.')
selection_criteria = input('\n\nPlease enter how many additional satellites you would like to populate by Option number:\n Option 0- 0 additionals\n Option 1- 10 additionals\n Option 2- 20 additionals\n Option 3- 30 additionals\n Option 4- 40 additionals\n Option 5- 50 additionals\n')


satlist = []
if selection_criteria == '':
    satlist = onelist
elif selection_criteria == '1':
    satlist = tenlist
elif selection_criteria == '2':
    satlist = twentylist
elif selection_criteria == '3':
    satlist = thirtylist
elif selection_criteria == '4':
    satlist = fortylist
elif selection_criteria == '5':
    satlist = fiftylist

if specified_sat != '':
    satlist.append(specified_sat)

print(f'\n\nBuilding database for the following satellites: \n{satlist}\n\nPlease be patient; estimated total time to completion is {len(satlist)*2/60} to {len(satlist)*4/60} hours. \n-Expect completion at approximately {datetime.now()+timedelta(hours=len(satlist)*3/60)}-\n\n',flush=True)

how_many = 0
for satnum in satlist:
    zr = get(f"https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{satnum}/orderby/TLE_LINE1%20ASC/EPOCH/2000-01-01--{today}/format/tle",headers=hdrs2)
    oneline = zr.text
    tlesraw = oneline.split('\r\n1')
    for i in range(len(tlesraw)):
       tlesraw[i] = tlesraw[i].replace('\r\n','|')
    for i in range(len(tlesraw)):
        tlesraw[i] = tlesraw[i].replace(' ','|')
        tlesraw[i] = tlesraw[i].split('|')
    tle_df = pd.DataFrame(tlesraw)
    tle_df['Output']=''
    def get_daytime(index_num):
        jday = tle_df.iloc[index_num][5]
        jday = float(jday)
        date, time = divmod(jday, 1.0)
        date = str(int(date))
        timedelta(days=time)
        output = datetime.strptime(date, '%y%j') + timedelta(time)
        return output.strftime("TLE,%b %d %Y %H:%M:%S.%f,1 ")
    for i in range(len(tle_df[0])):
        try:
            tle_df[0].iloc[i] = get_daytime(i)
        except:
            tle_df[0].iloc[i] = 'Flag for Del'
    
    tle_df = tle_df[tle_df[0] != 'Flag for Del']
    tle_df = tle_df.map(lambda x: str(x) if type(x) != type(str) else x)
    tle_df = tle_df.map(lambda x: '' if x == 'None' else x)
    tle_df = tle_df.map(lambda x: x + ' ' if type(x) == str and len(x)>1 else x)
    for h in range(28):
        for col in tle_df.columns[:-2]:
            for i in range(len(tle_df[col])):
                if tle_df[col].iloc[i] == '' and tle_df[col].iloc[i] != tle_df[col+1].iloc[i]:
                    tle_df[col].iloc[i] = tle_df[col+1].iloc[i] 
                    tle_df[col+1].iloc[i] = ''
    for col in tle_df.columns[:-1]:
        if tle_df[col].iloc[0] == tle_df[col].iloc[len(tle_df)-1] and tle_df[col].iloc[0] == '':
            tle_df = tle_df.drop(columns=col)
    tle_df[3] = '  ' + tle_df[3]
    tle_df[8] = ''
    tle_df[9] = '   1,2'
    tle_df[10] = ' ' + tle_df[10] + '  '
    tle_df[14] = ' ' + tle_df[14] + ' '
    tle_df['Output']=tle_df.sum(axis=1,skipna=True)
    tle_df['Output'] = tle_df['Output'] + '\n'
    tle_df['JDATE']=None
    for i in range(len(tle_df)):
        tle_df['JDATE'].iloc[i] = tle_df[3].iloc[i]
        tle_df['JDATE'].iloc[i] = tle_df['JDATE'].iloc[i][2:7]
    
    tle_df = tle_df.sort_values('JDATE',ascending=False)
    for i in range(len(tle_df)):
        jate = tle_df['JDATE'].iloc[i]
        filepath = f'DATABASE/StateProcessing/StateDatabase/{jate}_Database_States.txt'
        if os.path.exists(filepath):
            with open(filepath, 'a') as file:
                file.write(tle_df['Output'].iloc[i])
        else:
            with open(filepath, 'w') as file:
                file.write(tle_df['Output'].iloc[i])
    
    how_many += 1
    print(f'SCC #{satnum} Complete- {len(satlist)-how_many} satellites remain...',flush=True)
print(f'\n\nDatabase for {len(satlist)} GEO satellites complete!',flush=True)

