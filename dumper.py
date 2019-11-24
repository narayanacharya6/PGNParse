import os
import json
import csv


def dump_json(output_dir, file_name, games):
    try:
        json_file_path = os.path.join(output_dir, file_name + '.json')
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        json_file = open(json_file_path, 'w')

        json.dump(games, json_file)
        json_file.close()
        print('JSON dump complete:!', json_file.name)
    except Exception as inst:
        print('Something went wrong with JSON dump!', inst)


def dump_csv(output_dir, file_name, games):
    try:
        csv_file_path = os.path.join(output_dir, file_name + '.csv')
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        csv_file = open(csv_file_path, 'w')

        keys = games[0].keys()
        # Extrasaction ignore keys not in dict
        # Think again if we need this, example missing key is 'BlackTitle "LM"'
        dict_writer = csv.DictWriter(csv_file, keys, extrasaction='ignore')
        dict_writer.writeheader()
        dict_writer.writerows(games)
        csv_file.close()
        print('CSV dump complete:!', csv_file.name)
    except Exception as inst:
        print('Something went wrong with CSV dump!', inst)
