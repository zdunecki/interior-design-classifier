from pathlib import Path
import argparse
import urllib.request
import glob
import json
import os
import re


def download(arguments):
    style_counter = {}
    input_dir = arguments.input_dir
    output_dir = arguments.output_dir

    for file in os.listdir(input_dir):
        with open(os.path.join(input_dir, file)) as json_file:
            spitted = Path(file).stem.split("_")
            key = spitted[0]
            print(key)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if not hasattr(style_counter, key):
                list_of_files = glob.glob(output_dir + "/*")

                if len(list_of_files) == 0:
                    count_from = 0
                else:
                    latest_file = max(list_of_files, key=os.path.getctime)
                    last_file_index, *rest = map(int, re.findall('\d+', Path(latest_file).stem))
                    count_from = last_file_index + 1

            style_counter[key] = count_from

            data = json.load(json_file)

            uniq_folder = os.path.join(output_dir, key)

            if not os.path.exists(uniq_folder):
                os.makedirs(uniq_folder)

            for item in data[count_from:]:
                print("START DOWNLOAD....")
                full_file_name = os.path.join(output_dir, key, key + str(style_counter[key]) + ".jpg")

                try:
                    urllib.request.urlretrieve(item['imageURL'], full_file_name)
                    style_counter[key] = style_counter[key] + 1
                    print("DOWNLOAD FINISHED")
                except KeyError:
                    print("ITEM DOESN'T HAVE imageURL")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='input dir')
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='output dir')
    a, _ = parser.parse_known_args()
    return a


if __name__ == '__main__':
    args = get_args()
    download(args)

# example:
# python data.py --input-dir ./sources/pinterest --output-dir ./data/output/validation
