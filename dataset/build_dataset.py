#!/usr/bin/env python3
# coding=utf-8
from __future__ import print_function
import re
import csv


DATA_PATTERN = re.compile('<(.*)> <.*> \"(.*)\"@(ja|en)')

def extract_titles(input_filename, output_filename):
    print('Extracting titles from [%s] into [%s]...' % (input_filename, output_filename))
    with open(input_filename) as input_file:
        with open(output_filename, 'w') as output_file:
            writer = csv.writer(output_file)
            for line in input_file:
                match = DATA_PATTERN.match(line)
                if match:
                    writer.writerow(match.groups())


KATAKANA_TITLES_PATTERN = re.compile(u"^[ァ-ヺ\\s・ー]+$", re.UNICODE)
ENGLISH_TITLES_PATTERN = re.compile(u"^([A-Z]\\w*)(\\s[A-Z]\\w*)?$", re.UNICODE)

NONE_ENGLISH_NAMES = {'Horse', 'Agate', 'Black Forest'}

def join_title_datasets(ja_titles_filename, en_titles_filename, output_filename):

    print('Loading all Japaneses (url, title) pairs into memory...')
    mapping = {}
    with open(ja_titles_filename) as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            url = row[0]
            ja_word = row[1]
            if KATAKANA_TITLES_PATTERN.match(ja_word):
                mapping[url] = ja_word

    print('Loaded %d Japanese titles into memory' % len(mapping))
    print('Reading and joining English (url, title) one pair at a time')
    count = 0
    with open(en_titles_filename) as input_file:
        reader = csv.reader(input_file)

        with open(output_filename, 'w') as output_file:

            fieldnames = ['english', 'katakana']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                url = row[0]
                en_word = row[1]

                if url in mapping and ENGLISH_TITLES_PATTERN.match(en_word) and en_word not in NONE_ENGLISH_NAMES:
                    ja_word = mapping[url]
                    writer.writerow({
                        'english': en_word, 'katakana': ja_word
                    })
                    count += 1
                    if count % 5000 == 0:
                        print('Written %d joined labels...' % count)


if __name__ == "__main__":
    extract_titles('labels_wkd_uris_en.ttl', 'english_titles.csv')
    extract_titles('labels_wkd_uris_ja.ttl', 'japanese_titles.csv')
    join_title_datasets('japanese_titles.csv', 'english_titles.csv', 'data.csv')
    print('Done!!')


