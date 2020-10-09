
import pandas as pd
import numpy as np
import collections

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = [*CITY_DATA]
options = ["a", "b", "c"]
diction = dict(zip(options, cities))
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']


def get_filters():
    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!\n')

    option = input("Can you choose a city by typing the letter corresponding:\n"
                   " a) chicago , b) new york city , c) washington\n ").lower().strip()
    while option not in options:
        option = input(
            'Invalid input, please choose a city by typing the letter corresponding:\n'
            ' a) chicago , b) new york city , c) washington\n ').lower().strip()
    city = diction[option]
    month = input(
        "And also choose a month please: [january , february , march , april , may , june , all]?\n ").lower().strip()
    while month not in months:
        month = input(
            'Invalid input please choose from the options provided: [january , february , march , april , may , '
            'june , all]?\n ').lower().strip()

    day = input(
        "Lastly, which day do you want to study: [sunday , monday "
        ", tuesday , wednesday , thursday , friday , saturday, "
        "all]?\n ").lower().strip()
    while day not in days:
        day = input(
            "Invalid input please choose from the options provided: [sunday , monday , tuesday , wednesday , "
            "thursday , friday , saturday, all]?\n ").lower().strip()

    print('-' * 40)

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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'all':
        mode_month = df['month'].mode()[0]
        i = 0
        for mon in df['month']:
            if mon == mode_month:
                i += 1

        print('The most-common-month prize goes to: {}\nand its nu'
              'mber of occurrences is {}\n '.format(mode_month, i))

    if day == 'all':
        mode_day = df['day_of_week'].mode()[0]
        ii = 0
        for d in df['day_of_week']:
            if d == mode_day:
                ii += 1
        print('And the most-common-month prize goes to: {}\nand its nu'
              'mber of occurrences is {}\n '.format(mode_day, ii))

    mode_time = df['Start Time'].dt.hour.mode()[0]
    iii = 0
    for t in df['Start Time'].dt.hour:
        if t == mode_time:
            iii += 1
    print('Last but not least, the most-common-start-hour prize goes to: {}\nand its nu'
          'mber of occurrences is {}\n '.format(mode_time, iii))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_stations = df['Start Station']
    mode_start_station = start_stations.mode()[0]
    n_s_mode = len(df[start_stations == mode_start_station])
    print('The most-common-start-station prize goes to: {}\nand its nu'
          'mber of occurrences is {}\n '.format(mode_start_station, n_s_mode))

    end_stations = df['End Station']
    mode_end_station = end_stations.mode()[0]
    n_e_mode = len(df[end_stations == mode_end_station])
    print('And the most-common-end-station prize goes to: {}\nand its nu'
          'mber of occurrences is {}\n '.format(mode_end_station, n_e_mode))

    combinations = list(zip(start_stations, end_stations))
    n_combinations = 0
    mode_trip = collections.Counter(combinations).most_common(1)[0][0]
    for combination in combinations:
        if combination == mode_trip:
            n_combinations += 1

    print('Last but not least, the most-common-trip prize goes to: {}\nand its nu'
          'mber of occurrences is {}\n '.format(mode_trip, n_combinations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum() / 3600
    print('The Total Trip time for the timeframe and city chosen is: {} hours\n'.format(round(total_travel, 2)))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean() / 60
    print('For an average of: {} minutes\n'.format(round(mean_travel, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = list(set(df['User Type']))
    print('Now for the types of existing customers in the criteria chosen, there is {} for a total of'
          ' {} types. \n'.format(types, len(types)))

    df_types = df['User Type']
    for df_type in types:
        print("{}s: {}\n".format(df_type, len(df[df_types == df_type])))

    # Display counts of gender
    if city != "washington":
        gender = list(set(df['Gender'].fillna("Gender not provided")))
        df_genders = df['Gender']

        print('And the Genders of existing customers for the criteria chosen are {} for a total of'
              ' {} genders. \n'.format(gender, len(gender)))

        for df_gender in gender:
            print(
                "{}s: {} customer\n".format(df_gender, len(df[df_genders.fillna("Gender not provided") == df_gender])))

        print('Also the majority of the our customers in this'
              ' criteria are {}s.\n'.format(df["Gender"].mode()[0]))

        # Display earliest, most recent, and most common year of birth
        df_sorted = df.sort_values(by='Start Time', ascending=False)

        print('And now the first customer we dealt with in the criteria chosen was born in {}.\n'.format(
            int(df_sorted["Birth Year"].iloc[-1])))
        print('The most recent customer was born in {}.\n'.format(int(df_sorted["Birth Year"].iloc[0])))
        print('The most common birth year is {}.\n'.format(int(df["Birth Year"].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        i=5
        while True:
            print_data = input('\nWould you like to print some data? Enter yes or no\n')

            if print_data.lower().strip() != 'yes':
                break
            else:
                print(df.head(i))
                print(df.tail(i))
                i += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
    main()
