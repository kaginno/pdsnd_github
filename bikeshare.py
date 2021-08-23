import time
import pandas as pd
import numpy as np
import json



CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
# List of months
MONTH_DATA = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
# List of days
DAY_DATA = ('all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday')


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
    while True:
        city = input(
            "Please specify a city ('chicago, new york city, washington'): ").lower().strip()
        if city in CITY_DATA:
            break
        else:
            print('Invalid City Entry, please specify one of indicated options.')
            continue
        
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Please specify a month ('all, january, february, ... , june'): ").lower().strip()
        if month in MONTH_DATA:
            break
        else:
            print('Invalid Month Entry, please specify one of indicated options.')
            continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Please specify a day of week (all, monday, tuesday, ... sunday): ").lower().strip()
        if day in DAY_DATA:
            break
        else:
            print('Invalid Day Entry, please specify one of indicated options.')
            continue

    # while True:
    #     try:
    #         if city.isalpha() || month.isalpha() || day.isalpha():

    #     except ValueError:
    #         print("Sorry, I didn't understand that.")
    #         continue
    #     else:

    #         break
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
    df = pd.read_csv(CITY_DATA[city],index_col=0)
    # convert the Start Time  & End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month ,hour day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # # Convert month column values from digit to readable string
    # months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    #     7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    # df['month'] = df['month'].apply(lambda x: months[x])

    # filter by month if applicable
    if month != 'all':
        # # use the index of the months list to get the corresponding int
        months = ['january',
                  'february',
                  'march',
                  'april',
                  'may',
                  'june']

        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('================================================================')

    start_time = time.time()

    # display the most common month
    print("Most common month is: {}".format(df.month.mode()[0]))

    # display the most common day of week
    print("Most common day of week is: {}".format(df.day_of_week.mode()[0]))

    # display the most common start hour
    print("Most common start hour: {}".format(df.hour.mode()[0]))

    print("\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('================================================================')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station is: {} ".format(
        most_common_start_station))

    print("\n")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station is: {}".format(
        most_common_end_station))

    print("\n")

    # display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size(
    ).sort_values(ascending=False).index.tolist()[0]

    print("Most frequent combination of start station and end station trip is from : {} to {}".format(
        start_end_station[0], start_end_station[1]))

    print("*******************************************************************\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('================================================================')

    start_time = time.time()

    # display total travel time
    # convert seconds to hours & minutes
    total_travel_time = df['Trip Duration'].sum()
    total_seconds = total_travel_time % (24 * 3600)
    total_hour = total_seconds // 3600
    total_seconds %= 3600
    total_minutes = total_seconds // 60
    total_seconds %= 60

    print("Total Travel Time is {} hrs {} mins {} seconds".format(
        int(total_hour), int(total_minutes), int(total_seconds)))

    print("\n")
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_seconds = mean_travel_time % (24 * 3600)
    mean_hour = mean_seconds // 3600
    mean_seconds %= 3600
    mean_minutes = mean_seconds // 60
    mean_seconds %= 60

    print("Mean Travel Time is {} hrs {} mins {} seconds".format(
        int(mean_hour), int(mean_minutes), int(mean_seconds)))

    print("*******************************************************************\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print('================================================================')

    start_time = time.time()

    # Display counts of user types
    print("Breakdown of user types...")
    print("--------------------------------")
    print(df['User Type'].value_counts())

    print("\n")

    # Display counts of gender
    print("Breakdown of gender...")
    print("--------------------------------")
    if 'Gender' in df.columns:

        print(df['Gender'].value_counts())
    else:
        print("This Data Frame has no gender information")

    print("\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        print("Earliest Year of Birth: {}".format(int(df['Birth Year'].min())))
        print("Most Recent Year of Birth: {}".format(
            int(df['Birth Year'].max())))
        print("Most Common Year of Birth: {}".format(
            int(df['Birth Year'].mode()[0])))
    else:
        print("This Data Frame has no Birth Year information")

    print("*******************************************************************\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Get input from user and loop through the Dataframe to display 5 rows displayed as JSON till user types 'NO' """
    i = 0
    raw = input('\nWould you like to see 5 rows of raw data? yes or no:\n').lower().strip() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
             # TO DO: appropriately subset/slice your dataframe to display next five rows
            row_data=df.iloc[i:i+5].to_json(orient='records',lines=True).split('\n')
            for row in row_data:                
                json_row = json.dumps(json.loads(row), indent=2)
                print(json_row)
            
            raw = input('\nWould you like to see 5 more rows of data? yes or no:\n').lower().strip()  # TO DO: convert the user input to lower case using lower() function
            
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        #restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes':
            main()
        elif restart.lower() == 'no':
            break
        else:
            print("\nThat is not a valid answer. Please try again.")
            restart = input('\nInvalid Entry? Please choose either yes or no.\n')
        
        
                

if __name__ == "__main__":
    main()
