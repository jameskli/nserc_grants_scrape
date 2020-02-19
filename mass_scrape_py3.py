#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from lxml import html
import time
from random import randint
from random import shuffle
import csv


# GLOBAL CONSTANTS
BASE_URL = "https://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id="
MAX_ID = 670100
MIN_ID = 592611
BROWSER_WAIT_TIME = 10

# DIRECTORIES AND FILENAMES
TEST_CSV_SOURCE_DIR = "test-data"
# CSV_SOURCE_DIR = TEST_CSV_SOURCE_DIR
CSV_SOURCE_DIR = "data"
WIP_DIR = "wip"
RESULTS_DIR = "results"
# HTMLS_DIR = "htmls"
DIR_LIST = [WIP_DIR, RESULTS_DIR]
# WORKING_IDS_FILE = "working_ids_test.txt"
WORKING_IDS_FILE = "working_ids_full.txt"

NSERC_XPATHS = {
    "Title": "//div[@id='main-container-1col']/h2",
    "Competition Year": "//table[@class='researchDetails']//td[contains(.,'Competition Year:')]/following-sibling::td[1]",
    "Fiscal Year": "//table[@class='researchDetails']//td[contains(.,'Fiscal Year:')]/following-sibling::td[1]",
    "Project Lead Name": "//table[@class='researchDetails']//td[contains(.,'Project Lead Name:')]/following-sibling::td[1]",
    "Institution": "//table[@class='researchDetails']//td[contains(.,'Institution:')]/following-sibling::td[1]",
    "Department": "//table[@class='researchDetails']//td[contains(.,'Department:')]/following-sibling::td[1]",
    "Province": "//table[@class='researchDetails']//td[contains(.,'Province:')]/following-sibling::td[1]",
    "Award Amount": "//table[@class='researchDetails']//td[contains(.,'Award Amount:')]/following-sibling::td[1]",
    "Installment": "//table[@class='researchDetails']//td[contains(.,'Installment:')]/following-sibling::td[1]",
    "Program": "//table[@class='researchDetails']//td[contains(.,'Program:')]/following-sibling::td[1]",
    "Selection Committee": "//table[@class='researchDetails']//td[contains(.,'Selection Committee:')]/following-sibling::td[1]",
    "Research Subject": "//table[@class='researchDetails']//td[contains(.,'Research Subject:')]/following-sibling::td[1]",
    "Area of Application": "//table[@class='researchDetails']//td[contains(.,'Area of Application:')]/following-sibling::td[1]",
    "Co-Researchers": "//table[@class='researchDetails']//td[contains(.,'Co-Researchers:')]/following-sibling::td[1]",
    "Partners": "//table[@class='researchDetails']//td[contains(.,'Partners')]/following-sibling::td[1]",
    "Award Summary": """///div[@id='main-container-1col']/div[@id='RightColDetails']//p""",
}

RESULT_ORDER_LIST = [
    "Index",
    "Title",
    "Competition Year",
    "Fiscal Year",
    "Project Lead Name",
    "Institution",
    "Department",
    "Province",
    "Award Amount",
    "Installment",
    "Program",
    "Selection Committee",
    "Research Subject",
    "Area of Application",
    "Co-Researchers",
    "Partners",
    "Award Summary",
]


def check_page_headers_exist():
    id_list = list(range(MIN_ID, MAX_ID + 1))
    shuffle(id_list)
    working_urls = check_page_headers_exist(id_list)
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
    with open(WORKING_IDS_FILE, "w") as file:
        for item in working_urls:
            file.write("{}\n".format(item))


# CALCULATION HELPER FUNCTIONS


def browser_wait(approx_time=None):
    """Randomizes an arbitrary wait time (in sec)"""
    if (not approx_time) or approx_time < 3:
        time.sleep(0 + randint(0, 2))
    else:
        time.sleep(approx_time + randint(0, round(0.5 * approx_time)))


def return_url(page_id):
    """Return string of the URL to visit given a stock symbol"""
    return BASE_URL + page_id


def grab_data(page_id):
    """ Grab data from NSERC website"""
    # print("visiting", return_url(page_id))
    response = requests.get(return_url(page_id))
    result_dict = dict()
    result_dict["Index"] = page_id
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        for category, xpath in NSERC_XPATHS.items():
            found_text = "".join(s.text_content() for s in tree.xpath(xpath)).strip()
            try:
                # print(category, ":", found_text)
                result_dict[category] = found_text
            except:
                # print("Table read error")
                return result_dict

    return result_dict


def create_directories(dir_list):
    for dir_name in dir_list:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


def create_output_files():
    log_fullpath = WORKING_IDS_FILE
    results_fullpath = "{}/results.csv".format(RESULTS_DIR)

    if not os.path.exists(log_fullpath):
        with open(log_fullpath, "w") as file:
            file.write("")
    if not os.path.exists(results_fullpath):
        with open(results_fullpath, "w") as results_file:
            csv_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(RESULT_ORDER_LIST)


def return_curr_list_of_ids(log_fullpath):
    with open(WORKING_IDS_FILE, "r") as file:
        working_ids = [line.rstrip("\n") for line in file]

    if os.path.exists(log_fullpath):
        with open(log_fullpath, "r") as file:
            last_finished_id = file.readline().rstrip("\n")
    else:
        with open(log_fullpath, "w") as file:
            file.write("")
        last_finished_id = ""

    if last_finished_id not in working_ids:
        rest_of_ids = working_ids
    else:
        rest_of_ids = working_ids[working_ids.index(last_finished_id) + 1 :]

    return rest_of_ids


def nserc_scrape(id_name):
    result_dict = {item: "N/A" for item in RESULT_ORDER_LIST}

    result_dict.update(grab_data(id_name))
    return result_dict


def update_logs(id_name, log_fullpath):
    with open(log_fullpath, "w") as log_file:
        log_file.writelines("{}".format(id_name))


def update_result_csv(result_dict, results_fullpath):

    with open(results_fullpath, "a+") as results_file:
        csv_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
        csv_writer.writerow([result_dict[item] for item in RESULT_ORDER_LIST])


def main():
    create_directories(DIR_LIST)
    # working_urls = check_page_headers_exist()
    create_output_files()
    log_fullpath = "{}/{}".format(WIP_DIR, "last_id_logged.txt")
    results_fullpath = "{}/{}".format(RESULTS_DIR, "results.csv")

    ids_pending = return_curr_list_of_ids(log_fullpath)
    if len(ids_pending):
        continue_processing = True
        print(
            "Starting with ID {}. {} left to process".format(
                ids_pending[0], len(ids_pending)
            )
        )
    else:
        continue_processing = False
        print("Nothing in the queue")

    for id_name in ids_pending:
        if continue_processing:
            try:
                result_dict = nserc_scrape(id_name)
                update_logs(id_name, log_fullpath)
                update_result_csv(result_dict, results_fullpath)

            except:
                continue_processing = False
                print("Error with", id_name)
            if randint(1, 50) == 1:
                print(id_name, " sleeping...")
                browser_wait()


main()
