import pandas as pd
import numpy as np
import os
import time

desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option("display.max_columns", None)

cities = ['Chicago', 'New york city', 'Washington']
months = ['all', 'January', 'February', 'March', 'April', 'May', 'June']
day_week = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def input_user():
    """
    Use user input to define city, month and day variables
    All variables set to lowercase to compare with list in lowercase as well
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """

    print("""\nHello world, let's explore some US bike share data!\n""")

    while True:
        city = input('\nWhich city would you like to get the data from: ' + str(cities)+ ' ''').lower()
        if city not in list(pd.Series(cities).str.lower()):
            print('Sorry the city needs to be from that list:' + str(cities))
            continue
        else: break

    while True:
        month = input('For which month would you like to explore the data?: ' + str(months) + ' ''').lower()
        if month not in list(pd.Series(months).str.lower()):
            print('Sorry the month needs to be from that list:' + str(months))
            continue
        else: break

    while True:
        day = input('For which day of the week would you like to explore the data?: ' + str(day_week)+ ' ''').lower()
        if day not in list(pd.Series(day_week).str.lower()):
            print('Sorry the day needs to be from that list:' + str(day_week))
            continue
        else: break

    return(city, month, day)

def load_data(city, month, day):
    CITY_DATA = {'chicago': 'chicago.csv',
                 'new york city': 'new_york_city.csv',
                 'washington': 'washington.csv'}
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    #Printing user selection
    print('\nSo your selection is:\n -->City: {}\n -->Month: {}\n -->Day: {}'.format(city, month, day))

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour
    #df['day_of_week'] = df['Start Time'].dt.day_name()

    #Create a trip column
    df['Trip'] = df['Start Station'] + ' TO ' + df['End Station']

    #Cleaning Columns and rows
    df = df.dropna()
    if 'Birth Year' in df: df['Birth Year'] = df['Birth Year'].astype(int)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month.title())
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    #Print dataframe for debug only
    #print(df.head(100))

    return df

def statistic(df):
    """
    :param df generated in load_data
    :Output:
    #1 Popular times of travel
    #2 Popular stations and trip
    #3 Trip duration
    #4 User info
    """
    # Display the total number of trips for the selection
    number_of_rows = len(df.index)
    print('\nThe total number of trips for your selection is: {}'.format(number_of_rows))

    # 1 Popular times of travel
    popular_month = df['month'].value_counts().idxmax()
    popular_month_c = df['month'].value_counts().max()
    popular_day= df['day_of_week'].value_counts().idxmax()
    popular_day_c = df['day_of_week'].value_counts().max()
    popular_hour = df['hour'].value_counts().idxmax()
    popular_hour_c = df['hour'].value_counts().max()
    print('\n#############################')
    print('# 1 Popular times of travel #')
    print('#############################')
    print('The most popular month of the year is: {} with a count of: {}'.format(months[popular_month],popular_month_c))
    print('The most popular day of the week is: {} with a count of: {}'.format(popular_day,popular_day_c))
    print('The most popular hour the of day is: {} with a count of: {}'.format(popular_hour,popular_hour_c))

    #2 Popular stations and trip
    popular_start_station = df['Start Station'].value_counts().idxmax()
    popular_start_station_c = df['Start Station'].value_counts().max()
    popular_end_station = df['End Station'].value_counts().idxmax()
    popular_end_station_c = df['End Station'].value_counts().max()
    popular_trip = df['Trip'].value_counts().idxmax()
    popular_trip_c = df['Trip'].value_counts().max()
    print('\n###############################')
    print('# 2 Popular stations and trip #')
    print('###############################')
    print('The most popular start station is: {} with a count of: {}'.format(popular_start_station,popular_start_station_c))
    print('The most popular end station is: {} with a count of: {}'.format(popular_end_station,popular_end_station_c))
    print('The most popular trip is: {} with a count of: {}'.format(popular_trip,popular_trip_c))

    #3 Trip duration
    print('\n###################')
    print('# 3 Trip duration #')
    print('###################')
    total_duration = df['Trip Duration'].sum()
    max_duration = df['Trip Duration'].max()
    min_duration = df['Trip Duration'].min()
    mean_duration = df['Trip Duration'].mean()
    print('The total duration of all trips is: {} seconds'.format(int(total_duration)))
    print('The maximun duration for a trip is: {} seconds'.format(int(max_duration)))
    print('The minimun duration for a trip is: {} seconds'.format(int(min_duration)))
    print('The mean duration for a trip is: {} seconds'.format(int(mean_duration)))

    #4 User info
    print('\n################')
    print('# 4 User info #')
    print('################')
    # Counting the numbers of each unique type of user
    # Using the for to eliminate the dftype at the end of the display
    user_types = df['User Type'].value_counts()
    for key, type in user_types.items():
        print('The count of {}s is: {}'.format(key, type))

    if 'Gender' in df:
        #Count male users
        gender_count_male = df[df.Gender == 'Male'].Gender.value_counts()
        print('\nThe count for male users is: {}'.format(gender_count_male[0]))
        #Count female users
        gender_count_female = df[df.Gender == 'Female'].Gender.value_counts()
        print('The count for female users is: {}'.format(gender_count_female[0]))
        # Return min, max and most common birth year
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('\nThe earliest year of birth is: {}'.format(earliest_year))
        print('The most recent year of birth is: {}'.format(recent_year))
        print('The most common year of birth is: {}\n'.format(most_common_year))

    print('################')
    print('# END #')
    print('#################')

def clear():
    #Function to clear output
    os.system( 'cls' )

def display_raw_data(df):
    """
    :param df generated in load_data - Should be already sliced as per user instruction
    :Output: raw data if requested by user
    """

    i = 0
    raw = input("Do you want to look at raw data for your selection? (yes/no)").lower()

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])
            raw = input("Do you want to continue ?(yes/no)").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        city, month, day = input_user()
        start_time = time.time()
        df = load_data(city, month, day)
        statistic(df)
        print('\nThe runtime of the program is {:.4f} s\n'.format(time.time() - start_time))
        display_raw_data(df)
        again = input("\nDo you wish to start with a new selection? (yes/no) ")
        if 'yes' in again:
              clear()
              continue
        else:
              print("End")
              break

if __name__ == '__main__':
    main()
