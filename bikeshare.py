import time
import pandas as pd
import numpy as np

#global dict of source files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')


    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('What city would you like to explore? Enter Chicago, New York City, or Washington for Washington DC): ').lower() #get city
        if city not in ['chicago', 'new york city', 'washington']: #check if city is in not in List of acceptable cities
            print('\nThat\'s not an option, choose an available option: ')
            continue #if city is not in List, do While until entered city is in List
        else:
            break #exit While when entered city is in List


    # get user input for month (all, january, february, ... , june)
    # follows same logic as city
    while True:
        month = input('For what month? Enter January, February, March, April, May, June, or All): ').lower()
        if month not in ['january','february', 'march', 'april', 'may', 'june', 'all']:
            print('Data unavailable for that month, choose one of the available months or choose All: ')
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    # follows same logic as city
    while True:
        day = input('And for which day? Enter any of the usual days of the week or enter All for every day: ').lower()
        if day not in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday', 'all']:
            print('That\'s not a usual day of the week on Earth, pick a day or enter All.')
            continue
        else:
            break

    print('-'*40)
    return city, month, day #return values back to main function


def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load city .csv file into a dataframe; uses global dict defined in row 6
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month #dt.month gets the number of month, not name
    df['day_of_week'] = df['Start Time'].dt.day_name() #day_name() method gets the actual name of day


    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june'] #create months List to check against
        month = months.index(month) + 1 #convert the month entered by user to a number (i.e. march is 3, so month = 3)

        # filter by month column to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week column to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0] #get mode as int
    print("The most popular month is: ", months[popular_month - 1].title()) #convert mode as int to month name


    # display the most common day of week (same logic as month)
    popular_day_of_week = df['day_of_week'].mode()[0]
    print("The most popular day of the week is: ", popular_day_of_week)


    # display the most common start hour (same logic as month)
    df["hour"] = df["Start Time"].dt.hour #create hour column in order to get most popular hour
    popular_hour = df["hour"].mode()[0]
    print("The most popular hour is: ", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    fav_start_station = df['Start Station'].mode()[0]
    print('The most commonly used Start Station is: ', fav_start_station)


    # display most commonly used end station

    fav_end_station = df['End Station'].mode()[0]
    print('The most commonly used End Station is: ', fav_end_station)


    # display most frequent combination of start station and end station trip

    start_end_filter = df.value_counts(['Start Station', 'End Station']).head(1).index.tolist()
    print('The majority of people would start at', start_end_filter[0][0], 'station and end their journey at', start_end_filter[0][1], ' station')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    trip_duration_sum = df['Trip Duration'].sum()
    print('The total duration for all trips for the selected criteria is:', trip_duration_sum//86400, 'days', trip_duration_sum%86400//3600, 'hours', trip_duration_sum%86400%3600//60, 'minutes and', trip_duration_sum%86400%3600%60, 'seconds.')


    # display mean travel time
    trip_duration_avg = df['Trip Duration'].mean()
    print('The average travel time for all trips for the selected criteria is:', round(trip_duration_avg/60, 2), 'minutes.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types

    user_types = df['User Type'].value_counts().index.tolist()
    user_types_counts = df['User Type'].value_counts().tolist()
    print('These are the types of users and their counts:')

    i = 0
    while i < len(user_types):
        print('\t', user_types[i], user_types_counts[i])
        i += 1
    print()


    # Display counts of gender

    if('Gender' not in df):
        print('Washington DC does not have gender data.')
    else:
        genders = df['Gender'].value_counts().index.tolist()
        gender_counts = df['Gender'].value_counts().tolist()
        print('These are the genders and their counts:')

        i = 0
        while i < len(genders):
            print('\t', genders[i], gender_counts[i])
            i += 1
    print()


    # Display earliest, most recent, and most common year of birth

    if('Birth Year' not in df):
        print('Washington DC does not have birth year data.')
    else:
        youngest = int(df['Birth Year'].max())
        print('The youngest user was born in:', youngest,'\n')

        oldest = int(df['Birth Year'].min())
        print('The oldest user was born in:', oldest,'\n')

        birth_year_mode = int(df['Birth Year'].mode())
        print('Most users were born in:', birth_year_mode)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    while True:
        view_data = input('Would you like to view the raw data? Enter Yes or press any key to exit. ').lower()
        if view_data != 'yes':
            break

        else:
            continue_view = 'yes'
            position_one = 0
            position_two = 5

            while continue_view == 'yes':
                print(df[position_one:position_two])
                continue_view = input('Would you like to cotinue viewing the data? Enter Yes or press any key to exit.').lower()
                position_one = position_two
                position_two += 5

            break

#funtion controlling program
def main():

    while True:
        city, month, day = get_filters() #grab inputs for city, month, and day
        df = load_data(city, month, day) #create DataFrame

        print('For the criteria selected:')

        #below set of functions return various desired stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        #do While loop as long as user enters 'yes'; otherwise end program
        restart = input('\nWould you like to restart? Enter Yes or press any key.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
