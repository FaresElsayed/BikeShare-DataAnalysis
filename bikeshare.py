import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
months = set(['january', 'february', 'march', 'april', 'may', 'june'])

days = set(['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
   
    print('-'*60)
    
    while True:
        while True:
            #Taking the set of cities to query from while making sure we reprompt the user if the input is invalid
            cities = input('Please choose a city to analyze: chicago, new york city, washington or all\nYou can also choose 2 cities just seperate them by a comma:\n').lower().split(',')
            cities = [s.strip() for s in cities]
        
            if cities[0] == 'all' or set(cities).issubset(CITY_DATA):
                break

            else:
                print('\nInvalid Input, Try again\n')
            
        print('-'*60)
    
        while True:
            #Taking the set of months to query from while making sure we reprompt the user if the input is invalid
            month = input('Now type the month name you want to analyze or type all\nYou can also choose more than one month by typing them seperated by a comma:\nPS: The data only contains the months January to May\n').lower().split(',')
            month = [s.strip() for s in month]
        
            if month[0] == 'all' or set(month).issubset(months):
                break
    
            else:
                print('\nInvalid Input, Try again\n')
    
        print('-'*60)
    
        while True:
            #Taking the set of days to query from while making sure we reprompt the user if the input is invalid
            day = input('lastly type the day name you want to analyze or type all\nStill you can choose more than one day seperated by a coma:\n').lower().split(',')
            day = [s.strip() for s in day]
        
            if day[0] == 'all' or set(day).issubset(days):
                break
    
            else:
                print('\nInvalid Input, Try again\n')

        print('-'*60)
        
        #Making sure the inputs were all correct
        check = input('So these are the chosen parameters, if you wish to proceed type yes, if you want to rechoose type no\nData: {}\nMonth/s: {}\nDays: {}\n'.format(cities, month, day))
    
        if check == 'yes':
            print('-'*60)
            break
    
        else:
            print('-'*60)
            continue
    
    return cities, month, day    


def load_data(cities, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dfs_filtered - List of Pandas DataFrame containing cities data filtered by month and day
    """
    
    print('FILTERING THE DATASET, PLEASE WAIT')
    
    dfs = []
    dfs_filtered = []
    
    #Making a list of data frames for each city prompted
    if cities[0] == 'all':
        for key in CITY_DATA:
            dfs.append(pd.read_csv(CITY_DATA[key]))
        
    else:
        for city in cities:
            dfs.append(pd.read_csv(CITY_DATA[city]))
            
    #Changing data types to time series and making some useful new columns like day and month
    for df in dfs:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        
        df['Day'] = df['Start Time'].dt.weekday_name
        df['Day'] = df['Day'].str.lower()
        
        df['Month'] = df['Start Time'].dt.month_name()
        df['Month'] = df['Month'].str.lower()
        
        df['End Time'] =  pd.to_datetime(df['End Time'])
        
        if month[0] == 'all':
            if day[0] == 'all':
                dfs_filtered.append(df)
        
            else:
                df = df[df['Day'].isin(day)]
                dfs_filtered.append(df)
        
        else:
            df = df[df['Month'].isin(month)]
            
            if day[0] == 'all':
                dfs_filtered.append(df)
        
            else:
                df = df[df['Day'].isin(day)]
                dfs_filtered.append(df)
    print('FILTERING SUCCESS')
    print('-'*60)
    
    return dfs_filtered


def modify_all(cities, month, day):
    """
    Checks if the input is 'all' if yes it converts the variable to a list of all values
    
    Args:
        (list) cities - list of cities to analyze
        (list) month - list of the months to filter by
        (list) day - list of days of week to filter by
    Returns:
        (list) cities - list of cities to analyze
        (list) month - list of the months to filter by
        (list) day - list of days of week to filter by
    """
    
    if cities[0] == 'all':
        cities = ['chicago', 'new york city','washington']
        
    if month[0] == 'all':
        month = ['january', 'february', 'march', 'april', 'may', 'june']
    
    if day[0] == 'all':
        day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    return cities, month, day

    
def time_stats(dfs_filtered, cities):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (list) dfs_filtered - list of dataframes after being filtered
        (list) cities - list of cities to analyze
    """

    i = 0
    
    for df in dfs_filtered:
        start_time = time.time()
        print('\nCalculating The Most Frequent Times of Travel for:')
        print('*' * (len(cities[i])+2))
        print('*{}*'.format(cities[i]))
        print('*' * (len(cities[i])+2))
        
        maxx = df['Month'].value_counts().index.tolist()[0] #Extracting the most frequent month
        count = df['Month'].value_counts()[0] #Extracting the count of the most frequent month
        print('The most frequent month is: {}\nwith a total count of {}.\n'.format(maxx.title(), count))
        
        maxx = df['Day'].value_counts().index.tolist()[0]
        count = df['Day'].value_counts()[0]
        print('The most frequent Day is: {}\nwith a total count of {}.\n'.format(maxx.title(), count))
        
        maxx = df['Start Time'].dt.hour.value_counts().index.tolist()[0]
        count = df['Start Time'].dt.hour.value_counts()[0]
        print('The most frequent time of day is: {}\nwith a total count of {}.'.format(maxx, count))
        
        i += 1
        print("\nThis took %s seconds." % (time.time() - start_time))
        input('Hit Enter to continue\n')
        print('-'*60)

        
def station_stats(dfs_filtered, cities):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        (list) dfs_filtered - list of dataframes after being filtered
        (list) cities - list of cities to analyze
    """

    i = 0
    
    for df in dfs_filtered:
        start_time = time.time()
        print('\nCalculating The Most Popular Stations and Trip for:')
        print('*' * (len(cities[i])+2))
        print('*{}*'.format(cities[i]))
        print('*' * (len(cities[i])+2))

        maxx = df['Start Station'].value_counts().index.tolist()[0]
        count = df['Start Station'].value_counts()[0]
        print('The most frequent Start Station is: {}\nwith a total count of {}.\n'.format(maxx.title(), count))
        
        maxx = df['End Station'].value_counts().index.tolist()[0]
        count = df['End Station'].value_counts()[0]
        print('The most frequent End Station is: {}\nwith a total count of {}.\n'.format(maxx.title(), count))
        
        df['Trip'] = df['Start Station'] + df['End Station']
        maxx = df['Trip'].value_counts().index.tolist()[0]
        count = df['Trip'].value_counts()[0]
        print('The most frequent Trip is: {}\nwith a total count of {}.\n'.format(maxx.title(), count))
        
        i += 1
        print("\nThis took %s seconds." % (time.time() - start_time))
        input('Hit Enter to continue\n')
        print('-'*60)
        
        
def trip_duration_stats(dfs_filtered, cities):
    """Displays statistics on the total and average trip duration."""

    i = 0
    
    for df in dfs_filtered:
        start_time = time.time()
        print('\nCalculating Trip Duration for:')
        print('*' * (len(cities[i])+2))
        print('*{}*'.format(cities[i]))
        print('*' * (len(cities[i])+2))
    
        print('The total travel time of all Trips is: {} hours.'.format(df['Trip Duration'].sum()/60/60))
        print('The average travel time of Trips is: {} minutes.'.format(df['Trip Duration'].mean()/60))
        
        i += 1
        print("\nThis took %s seconds." % (time.time() - start_time))
        input('Hit Enter to continue\n')
        print('-'*60)

        
def user_stats(dfs_filtered, cities):
    """Displays statistics on bikeshare users."""

    i = 0
    
    for df in dfs_filtered:
        start_time = time.time()
        print('\nCalculating The User statistics for:')
        print('*' * (len(cities[i])+2))
        print('*{}*'.format(cities[i]))
        print('*' * (len(cities[i])+2))
        
        print('The distribution of user types is:\n{}'.format(df['User Type'].value_counts()))
        print('\n')
        
        if cities[i] == 'washington':
            i += 1
            print("This took %s seconds." % (time.time() - start_time))
            input('Hit Enter to continue\n')
            print('-'*60)
            continue
            
        maxx = int(df['Birth Year'].value_counts().index.tolist()[0])
        count = df.loc[df['Birth Year'] == maxx,'Birth Year'].count()
       
        print('The distribution of user genders is:\n{}'.format(df['Gender'].value_counts()))
        print('\n')
        print('The youngest customer is born in: {} \nAnd the oldest is born in {}\nHowever the most frequent birth date is {} with a total of {} customers.'.format(df['Birth Year'].max(), df['Birth Year'].min(), maxx, count)) 
                    
        i += 1
        print("\nThis took %s seconds." % (time.time() - start_time))
        input('Hit Enter to continue\n')
        print('-'*60)

        
def sampling (dfs_filtered, cities):
    """Displays sample data from the data set."""
    i = 0
    
    for df in dfs_filtered:
        while True:
            check = input('Would you like to see some random samples from the {} dataset? '.format(cities[i]))
            
            if check == 'yes':
                print(df.sample(5))
            else:
                i += 1
                break
    
                
def main():
    while True:
        cities, month, day = get_filters()
        df = load_data(cities, month, day)
        cities, month, day = modify_all(cities, month, day)
        time_stats(df, cities)
        station_stats(df, cities)
        trip_duration_stats(df, cities)
        user_stats(df, cities)
        sampling(df, cities)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    