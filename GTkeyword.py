"""Helper function to retrieve Google Trends for specified search dates - expansion of pytrends"""
def GTkeyword(keywords, counts = 1, sleeptime = 0, time_start = "2012-01-01", time_end = "2019-06-30", time_interval = 2738,
              region = "US", region_level = "DMA", Timezone = "360"):
    now_min = datetime.datetime.now().min
    timenow = datetime.datetime.now().strftime('%Y%m%d%H%M')
   

        def dateRange(beginDate, endDate):
            dates = []
            dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
            date = beginDate[:]
            while date <= endDate:
                dates.append(date)
                if (date == dt.strftime ("2004-01-01")) or (date == dt.strftime ("2008-01-01"))\
                or (date == dt.strftime ("2012-01-01")) or (date == dt.strftime ("2016-01-01")) \
                or  (date == dt.strftime ("2020-01-01")) or  (date == dt.strftime ("2024-01-01")):
                    dt = dt + datetime.timedelta(time_interval+1)
                    date = dt.strftime("%Y-%m-%d")
                else:
                    dt = dt + datetime.timedelta(time_interval)
                    date = dt.strftime("%Y-%m-%d")          
            return dates

        list_of_dates = []
        if __name__ == '__main__':
            for date in dateRange(time_start, time_end):
                print (date)
                list_of_dates.append(date)

        timeframeX = time_start + " " + time_end

        if len(kw_list) == 1:
                filename = keywords.replace('*', '').replace(" ","_")[0:6]+"_"+ \
                timeframeX + ' tz=' + Timezone +" "+ str(time_interval) + 'days' \
                + " " + region + region_level + str(Rotate) + "_" + timenow + '.csv'
                with open(filename, 'a+', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(['DateStart','DateEnd', 'Interval Days', 'GeoName', 'Keyword1_' + kw_list[0]])
        elif len(kw_list) == 2:
                filename = keywords.replace('*', '').replace(" ","_")[0:6]+"_"+ \
                kw_list[1] +"_"+ timeframeX + ' tz=' + Timezone +" "+ str(time_interval)\
                + 'days' + " " + region + region_level + str(Rotate) + "_" + timenow + '.csv'
                with open(filename, 'a+', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(['DateStart','DateEnd', 'Interval Days',\
                                     'GeoName', 'Keyword1_' + kw_list[0], 'Keyword2_' + kw_list[1]])



        for i in range(0, len(list_of_dates)-1):
            end_of_interval_day_plus_one = datetime.datetime.strptime(list_of_dates[i+1], '%Y-%m-%d')\

            delta = datetime.timedelta(days=1) 
            n_days= end_of_interval_day_plus_one - delta  
            end_of_interval_day = n_days.strftime('%Y-%m-%d') 
            timeframeX = list_of_dates[i] + " " + end_of_interval_day 
            pytrend.build_payload(kw_list, timeframe = timeframeX, geo = region) 
            print(pytrend.interest_by_region(resolution = region_level)) 


            select_df = pd.DataFrame(pytrend.interest_by_region(resolution = region_level)) #grab data    

            '''X = dict(select_df)
            print(X)
            print(select_df.shape)
            print(select_df.columns)
            print(select_df.index)
            print(select_df.describe())'''

            G = select_df.index 

            if len(kw_list) == 1:
                Y1 = select_df[kw_list[0]]
                with open(filename, 'a+', newline='') as csvfile:
                    for j in range (0, len(G.values)):
                        writer = csv.writer(csvfile, delimiter=',')
                        text = G.values[j]
                        if Y1.values[j] != 0:
                            writer.writerow([list_of_dates[i], end_of_interval_day, time_interval, text, Y1.values[j]])

            elif len(kw_list) == 2:
                Y1 = select_df[kw_list[0]]
                Y2 = select_df[kw_list[1]]
                with open(filename, 'a+', newline='') as csvfile:
                    for j in range (0, len(G.values)):
                        writer = csv.writer(csvfile, delimiter=',')
                        text = G.values[j]

                        writer.writerow([list_of_dates[i], end_of_interval_day, time_interval,\
                                         text, Y1.values[j], Y2.values[j]])



        if list_of_dates[-1] != time_end or (list_of_dates[-1] == time_end and time_interval == 1):
            timeframeX = list_of_dates[-1]+" "+time_end
            X1 = datetime.datetime.strptime(list_of_dates[-1], "%Y-%m-%d")
            X2 = datetime.datetime.strptime(time_end, "%Y-%m-%d")
            last_interval_of_days = (X2-X1).days + 1
            pytrend.build_payload(kw_list, timeframe = timeframeX, geo = region)
            print(pytrend.interest_by_region(resolution = region_level))
            select_df = pd.DataFrame(pytrend.interest_by_region(resolution = region_level))
            G = select_df.index

            if len(kw_list) == 1:
                Y1 = select_df[kw_list[0]]
                with open(filename, 'a+', newline='') as csvfile:
                    for j in range (0, len(G.values)):
                        writer = csv.writer(csvfile, delimiter=',')
                        text = G.values[j]
                        if Y1.values[j] != 0:
                            writer.writerow([list_of_dates[-1], time_end, last_interval_of_days, text, Y1.values[j]])

            elif len(kw_list) == 2:
                Y1 = select_df[kw_list[0]]
                Y2 = select_df[kw_list[1]]
                with open(filename, 'a+', newline='') as csvfile:
                    for j in range (0, len(G.values)):
                        writer = csv.writer(csvfile, delimiter=',')
                        text = G.values[j]
                        writer.writerow([list_of_dates[-1], time_end, last_interval_of_days,\
                                         text, Y1.values[j], Y2.values[j]])