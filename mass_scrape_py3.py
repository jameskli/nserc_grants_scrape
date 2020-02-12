#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from lxml import html
import time
from random import randint
from random import shuffle

# GLOBAL CONSTANTS
BASE_URL = "https://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id="
MAX_ID = 670100
MIN_ID = 592611
BROWSER_WAIT_TIME = 10


def check_page_headers_exist(id_list):
    shuffle(id_list)
    working_urls = list()
    for index, item in enumerate(id_list):
        response = requests.head(BASE_URL + str(item))
        if response.status_code == 200:
            working_urls.append(item)
        else:
            print(item, " does not exist")
        if randint(1, 100) == 100:
            print(index, " sleeping...")
            browser_wait()
    working_urls.sort()
    return working_urls


# CALCULATION HELPER FUNCTIONS


def browser_wait(approx_time=None):
    """Randomizes an arbitrary wait time (in sec)"""
    if (not approx_time) or approx_time < 3:
        time.sleep(0 + randint(0, 2))
    else:
        time.sleep(approx_time + randint(0, round(0.5 * approx_time)))


def main():
    id_list = list(range(MIN_ID, MAX_ID + 1))
    # id_list = list(range(MIN_ID, MIN_ID + 10))
    working_urls = check_page_headers_exist(id_list)
    print(len(working_urls), "/", len(id_list))
    with open("working_ids.txt", "w") as file:
        for item in working_urls:
            file.write("{}\n".format(item))


main()
