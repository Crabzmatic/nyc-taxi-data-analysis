import os
import sys
import calendar
import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt

plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi'] = 500


def plot_results(payment_shares, payment_labels, xlabels):
    plt.bar(xlabels, payment_shares[0], width=0.5, label=payment_labels[0])
    bottom = np.zeros(len(payment_shares[0]))
    for i in range(1, len(payment_labels)):
        bottom = bottom + payment_shares[i - 1]
        plt.bar(xlabels, payment_shares[i], bottom=bottom, width=0.5, label=payment_labels[i])

    plt.xticks(rotation='vertical')
    plt.ylabel('Payment share')
    plt.title('Payment share by month')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('payment_share_output.svg')
    plt.show()


def process_data_file(data_file_path, payment_shares_per_month, pbar, rescale=True):
    pbar.set_description(f'{data_file_path}')

    year, month = data_file_path.split('/')[-1].split('_')[-1].split('.')[0].split('-')
    year, month = int(year), int(month)
    month = calendar.month_name[month]

    chunk_size = 100_000  # adjust according to your machine memory
    for chunk in pd.read_csv(data_file_path, chunksize=chunk_size, header=0, usecols=['payment_type',
                                                                                      'tpep_pickup_datetime']):
        for payment_type in chunk['payment_type']:
            try:
                payment_shares_per_month[int(payment_type) - 1] += 1
            except ValueError:
                pass
    if rescale:
        allsum = np.sum(payment_shares_per_month, dtype=np.float64)
        payment_shares_per_month /= allsum
    return payment_shares_per_month, year, month


def main(args):
    data_dir = args[0]
    data_files = os.listdir(data_dir)

    payment_labels = ['Credit card', 'Cash', 'No charge', 'Dispute', 'Unknown', 'Voided trip']
    payment_shares = []
    for i in range(0, len(payment_labels)):
        payment_shares.append([])

    xlabels = []

    pbar = tqdm(data_files[1:], colour='green')
    for data_file in pbar:
        payment_shares_per_month = np.zeros(len(payment_labels), dtype=np.float64)
        payment_shares_per_month, year, month = process_data_file(f'{data_dir}/{data_file}', payment_shares_per_month,
                                                                  pbar)
        xlabels.append(f'{month} {year}')
        for j in range(0, len(payment_labels)):
            payment_shares[j].append(payment_shares_per_month[j])

    plot_results(payment_shares, payment_labels, xlabels)


if __name__ == '__main__':
    main(sys.argv[1:])
