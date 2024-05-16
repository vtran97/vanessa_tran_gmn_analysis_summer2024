# -----------------------------------------------------------------------------------------------------------
# function : get all entries up to the current month 
# this helps to automatically create a list of all the years in the system so that
# you don't have to loop through them all manually (done by just making a bunch of lists and putting them
# into one at the end, but long term this is not effective)

# getting dates
from datetime import datetime

def get_all_months_by_year_list():
    # returns a list of all months that the GMN has been active -- used to acccess data through GMN database

    # beginning of all data of GMN
    year = 2018

    all_months = []

    # Get the current mo
    x = str(datetime.now().date()).split("-")
    current_month = x[0] + "-" + x[1] 
    year_list = []
    start = "2018-12"
    current_month 

    for year in range(int(start.split("-")[0]), int(current_month.split("-")[0]) + 1):
        year_list.append(year)

    for year_no in range(len(year_list)):

        # this just allows the computer see the correct year instead of using index
        year = year_no + 2018

        if year == 2018:
            # special case, only one month and should never change (unless we build a time machine)
            all_months.append(['2018-12'])

        else:
            # for all months after leading up to current date for the current year 

            year_month_list = [] # full list
            cut_list = [] # list for the cut off year
            done = False # used for later for cut list

            for month in range(1, 13):

                if month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    month_name = str(year) + '-0' + str(month)
                    year_month_list.append(month_name)

                else: # months 10, 11, 12
                    month_name = str(year) + "-" + str(month)
                    year_month_list.append(month_name)
            
            if year != int(current_month.split("-")[0]): # if the year is not the current year
                all_months.append(year_month_list)
            
            else: # if the year is the current year
                # need to shorten the lsit to find the months up to this point that we can analyse 
                # (not getting results from the future)

                while not done:
                    for i in range(len(year_month_list)):
                        if year_month_list[i] == current_month:
                            cut_list.append(year_month_list[i])
                            done = True
                        if year_month_list[i] != current_month and done == False:
                            cut_list.append(year_month_list[i])

                all_months.append(cut_list)

    # return list in form [[months from 2018], [months from 2019], [months from 2020], etc...]
    return all_months