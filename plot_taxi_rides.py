import os
import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from calendar import monthcalendar
from matplotlib import pyplot as plt

plt.rcParams['savefig.dpi'] = 500


def moving_average(x, window_size):
    return np.convolve(x, np.ones(window_size), 'valid') / window_size


def plot_results(all_days):
    x = list(range(0, len(all_days)))
    plt.bar(x, all_days)
    plt.xticks(ticks=[0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366, 397, 425, 456, 486, 517, 547],
               labels=['January 2020', 'February 2020', 'March 2020', 'April 2020', 'May 2020', 'June 2020',
                       'July 2020', 'August 2020', 'September 2020', 'October 2020', 'November 2020', 'December 2020',
                       'January 2021', 'February 2021', 'March 2021', 'April 2021', 'May 2021', 'June 2021',
                       'July 2021'],
               rotation='vertical')
    window_size = 7
    averaged = moving_average(all_days, window_size=window_size)
    averaged = moving_average(averaged, window_size=window_size)

    plt.plot(x[:-2 * (window_size - 1)], averaged, color='green', linewidth=4)
    plt.title('Number of yellow taxi rides in New York per day')
    plt.suptitle(' ')
    plt.tight_layout()
    plt.savefig('output.png')
    plt.show()


def process_data_file(data_file_path, taxi_rides_per_month, pbar):
    year, month = data_file_path.split('/')[-1].split('_')[-1].split('.')[0].split('-')
    year, month = int(year), int(month)
    pbar.set_description(f'{year} {month}')

    days_in_month = np.max(monthcalendar(year, month))
    taxi_rides_per_day = np.zeros(days_in_month, dtype=np.int32)
    chunk_size = 100_000  # adjust according to your machine memory
    for chunk in pd.read_csv(data_file_path, chunksize=chunk_size, header=0, usecols=['tpep_pickup_datetime']):
        for date in chunk['tpep_pickup_datetime']:
            parsed_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
            if parsed_date.month == int(month):  # filter out taxi rides that are in wrong file
                taxi_rides_per_day[int(parsed_date.day) - 1] += 1
    taxi_rides_per_month.append(taxi_rides_per_day)


def main(args):
    data_dir = args[0]
    data_files = os.listdir(data_dir)
    taxi_rides_per_month = []
    pbar = tqdm(data_files, colour='green')
    for data_file in pbar:
        process_data_file(f'{data_dir}/{data_file}', taxi_rides_per_month, pbar)
    all_days = [day for taxi_rides_per_day in taxi_rides_per_month for day in taxi_rides_per_day]
    plot_results(all_days)


if __name__ == '__main__':
    main(sys.argv[1:])
