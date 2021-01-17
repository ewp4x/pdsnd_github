import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

#Function to take inputs from the user and validate the values
def get_filters():
    #Grab all inputs of the user
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for City
    while True:
        try:
            city = str(input('Please enter a city - Chicago, New York City, or Washington: ').lower())
            if city in CITY_DATA.keys():
                break
            print("Please enter one of the cities listed")
        except Exception as e:
            print(e)
            
    # Get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Please enter a month like January or February or All: ').lower())
            if month in months:
                month = month.title()
                break
            print("Invalid month entered")
        except Exception as e:
            print(e)
    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Please enter a day of week like Monday or Tuesday or All: ').lower())
            if day in days:
                day = day.title()
                break
            print("Invalid day entered")
        except Exception as e:
            print(e)
            
    print('-'*40)
    
    return city, month, day

#Function to take the user inputs and create final DataFrame to use in statistics
def load_data(city, month, day):
    #Load the city csv into DataFrame
    df = pd.DataFrame(pd.read_csv(CITY_DATA.get(city)))
    
    #Create datetime columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    df['route_count'] = 1
    
    #Create subset of full DataFrame based on inputs
    if month !='All' and day != 'All':
        df = df.loc[df['month'] == month]
        df = df.loc[df['day_of_week'] == day]
    elif month == 'All' and day == 'All':
        df = df
    elif month == 'All':
        df = df.loc[df['day_of_week'] == day]
    elif day == 'All':
        df = df.loc[df['month'] == month]              
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is {}'.format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]             
    print('The most common day of week is {}'.format(most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df['start_hour'].mode()[0]             
    print('The most common start hour is {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    mc_start_station = df['Start Station'].mode()[0]             
    print('The most common Start Station is {}'.format(mc_start_station))

    # Display most commonly used end station
    mc_end_station = df['End Station'].mode()[0]             
    print('The most common End Station is {}'.format(mc_end_station))

    # Display most frequent combination of start station and end station trip
    station_pair_count = df.groupby(['Start Station','End Station'])['route_count'].sum()
    mc_station_pair = station_pair_count.nlargest(1)
    print('The top 5 Start Station and End Stations by trip count are: \n{}'.format(mc_station_pair))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = round(df['Trip Duration'].sum()/60,2)
    print('The total travel time for all trips during this timeframe is {} minutes'.format(total_travel_time))
    
    # Display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean()/60,2)
    print('The average travel time for this timeframe is {} minutes'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['route_count'].sum()
    print('Here is the breakdown of user types: \n{}\n'.format(user_types))
    
    # Display counts of gender
    
    try:
        gender_counts = df.groupby(['Gender'])['route_count'].sum()
        print('Here is the breakdown of gender counts: \n{}\n'.format(gender_counts))
    except KeyError:
        print('There is no \'Gender\' column to use for Gender statistics')

    # Display earliest, most recent, and most common year of birth
    try:
        mc_birth_year = df['Birth Year'].mode()[0]
        oldest_birth_year = df['Birth Year'].min()
        youngest_birth_year = df['Birth Year'].max()
        print('Here are statistics on age of ridership: \n Oldest Year {}\n Most Recent Year {}\n Most Common Year {}'.format(oldest_birth_year,youngest_birth_year,mc_birth_year))
    except KeyError:
        print('There is no \'Birth Year\' column to use for Birth Year statistics')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_data(df):
    #Printing 5 rows of the DataFrame as requested by user
    data_rows = input('\nNow that you\'ve seen the statistics would you like to see 5 rows of data?  Enter yes or no.\n').lower()
    start_loc = 0
    end_loc = 5
    while data_rows.lower() == 'yes':
        print(df.iloc[start_loc:end_loc,:])
        start_loc += 5
        end_loc += 5
        data_rows = input("Do you wish to see 5 more rows?  Enter yes or no.\n").lower()
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
