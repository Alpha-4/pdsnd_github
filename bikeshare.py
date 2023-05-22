import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'febrary', 'march', 'april', 'may', 'june', 'july', 'august', 'september' ,'october', 'november', 'december']
WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
CITY_NAME = ['chicago', 'new york city', 'washington']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    #valid_city_response = [x for x in range(1,4)]
    #valid_months_response = [x for x in range(13)]
    #valid_day_of_week_response = [x for x in range(8)]
    while True:
        try:
            city = input("choose a city to analyze: chicago, new york city or washington.\n").lower().strip()
            if city not in CITY_NAME:
                print("\n *** Invalid user input. Please choose a city from - chicago, new york city or washington ***\n")
            else:
                city = CITY_NAME.index(city)
                break
        except ValueError:
            print("\n *** Invalid user input. Please choose a city from - chicago, new york city or washington ***\n")
            

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("choose a specific month: Enter january, february, march, april, .. , november, december or all (for all months) \n").lower().strip()
            if month not in MONTHS and month != 'all':
                print("\n *** Invalid user input. Please enter a month as january, february, march, april, .. , november, december or all (for all months) ***\n")
            else:
                if month == 'all':
                    month = 0
                else:
                    month = MONTHS.index(month)
                break
        except ValueError:
            print("\n *** Invalid user input. Please enter a month as january, february, march, april, .. , november, december or all (for all months) ***\n")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("choose a specific day of week: Enter monday, tuesday, .. , saturday, sunday or all (for all days of the week) \n").lower().strip()
            if day not in WEEK_DAYS and day != 'all':
                print("\n *** Invalid user input. Please choose a day as monday, tuesday, .. , saturday, sunday or all (for all days of the week) ***\n")
            else:
                if day == 'all':
                    day = 0
                else:
                    day = WEEK_DAYS.index(day)
                break
        except ValueError:
            print("\n *** Invalid user input. Please choose a day as monday, tuesday, .. , saturday, sunday or all (for all days of the week) ***\n")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city_index=[x for x in CITY_DATA.keys()][city-1]
    df = pd.read_csv(CITY_DATA[city_index])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    
    if month != 0:
        df = df[df['month'] == month]
        
    if day != 0:
        df = df[df['day'] == day-1]
         
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    
    df['hour'] = df['Start Time'].dt.hour
    df['week'] = df['Start Time'].dt.dayofweek

    # display the most common month
    print('Most common month : %s' % (MONTHS[df['month'].mode()[0] - 1]))

    # display the most common day of week
    print('Most common day of week : %s' % (WEEK_DAYS[df['week'].mode()[0]]))

    # display the most common start hour
    print('Most common start hour : %s' % (df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station : %s' % ( df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most popular end station : %s' % ( df['End Station'].mode()[0]))

    df['combo'] = df['Start Station'] + '  --To--  ' + df['End Station']
    # display most frequent combination of start station and end station trip
    print('Most popular combination of start station and end station : %s' % ( df['combo'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total trips
    print('Total number of trips: %s' % (df['Start Time'].count()))
    

    # display total travel time
    df['total time'] = pd.to_datetime(df['End Time']) - df['Start Time']
    print('Total travel time (in seconds) of trip: %s' % (df['total time'].sum()/ np.timedelta64(1, 's')))
    

    # display mean travel time
    print('Average travel time (in seconds) of trip: %s' % (df['total time'].mean()/ np.timedelta64(1, 's')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_map = df['User Type'].value_counts().to_dict()
    for key in user_type_map.keys():
        print('Total number of \'%s\' type of user: %s' %(key,user_type_map[key]))
    
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_map = df['Gender'].value_counts().to_dict()
        for key in gender_map.keys():
            print('Total %s users: %s' %(key,gender_map[key]))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the data')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Year of birth for eldest user: %s' %(int(df['Birth Year'].min())))
        print('Year of birth for youngest user: %s' %(int(df['Birth Year'].max())))
        print('Most common year of birth: %s' %(int(df['Birth Year'].mode()[0])))
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def generate_data(df,size,count):
    """Displays 5 records to user"""
    
    print('\n Printing 5 trip data records...\n')
    
    if count >= size:
        raise ValueError("No more records!")
    elif(count + 5 > size):
        return df.iloc[count : size]
    return df.iloc[count : count + 5]
  
  
def print_data(city):
    """Displays 5 records to user"""
    
    city_index=[x for x in CITY_DATA.keys()][city-1]
    data_df = pd.read_csv(CITY_DATA[city_index]);
    
    # Added column name to column with ids
    data_df.columns.values[0]='User ID'
    
    # Prompt for user input to display records
    show_data = input('\nWould you like to see 5 trip data records? Enter \'yes\' to view data or else \'no\'.\n')
    count=0
    
    while show_data == 'yes':
        start_time = time.time()
        try:
            output_list=generate_data(data_df,data_df.shape[0],count)
        except ValueError:
            print(ValueError)
            
        count += 5
        print(output_list)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
        # Prompt for user input to display more records
        show_data = input('\nWould you like to see next 5 records? Enter \'yes\' to view data or else \'no\'.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
    
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        #Prints the data to user in small chunks of size 5
        print_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
