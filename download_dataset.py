import sys
import requests
import pandas as pd
from tqdm import tqdm


def main(args):
    data_sources = pd.read_csv("nyc_taxi_data_links.csv", header=0, dtype='str', sep=',')
    cab_type = args[0]
    year = args[1]

    for row in data_sources.iterrows():
        data_source = row[1]
        if data_source['name'] == cab_type and year in data_source['source']:
            url = data_source['source']
            response = requests.get(url, stream=True)

            with open(f"data/{url.split('/')[-1]}", "wb") as f:
                for data in tqdm(response.iter_lines()):
                    f.write(data)
                    f.write('\n'.encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1:])
