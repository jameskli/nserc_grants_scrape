#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import csv
import sys
import getopt
from random import randint
from datetime import datetime
from selenium import webdriver

# GLOBAL CONSTANTS
BASE_URL = 'http://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id='
MAX_ID = 592610
MIN_ID = 1


def initialize_browser():
    """Initialize browser, also includes using an adblocker, but I dont think it quite works"""
    const_adblock_xpi_path = 'res/uBlock0.firefox.xpi'  # load Firefox with uBlock Origin enabled
    ffprofile = webdriver.FirefoxProfile()
    ffprofile.add_extension(const_adblock_xpi_path)
    browser = webdriver.Firefox(firefox_profile=ffprofile)

    return browser


def browser_load_url(browser, url_string):
    """load browser from url_string"""
    browser.get(url_string)
    browser_wait(3)


def browser_quit(browser):
    """Quits the browser"""
    browser.quit()


def browser_wait(approx_time=None):
    """Randomizes an arbitrary wait time (in sec)"""
    if (not approx_time) or approx_time < 3:
        time.sleep(2 + randint(0, 2))
    else:
        time.sleep(approx_time + randint(0, round(0.5 * approx_time)))


def grab_data(browser):
    """ Grab data from NSERC website"""
    column_header = ["Competition Year", "Fiscal Year", "Project Lead Name", "Institution",
                     "Department", "Province", "Award Amount", "Installments", "Program",
                     "Selection Committee", "Research Subject", "Area of Application",
                     "Co-Researchers", "Partners", "Award Summary"
                     ]

    column_data_source = ["""/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][1]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][1]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[2]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[2]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][2]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][2]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[4]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[4]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][3]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][3]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[6]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[6]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][4]/td[2]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']
                            /table[@class='researchDetails']/tbody/tr[@class='oddRow'][4]/td[4]""",
                          """/html/body/div[@id='cn-body-inner-1col']/div[@id='cn-cols']
                            /div[@id='cn-cols-inner']/div[@id='cn-centre-col']
                            /div[@id='cn-centre-col-inner']/section/div[3]/div[@id='CenterCol']
                            /div[@id='main-container-1col']/div[@id='RightColDetails']/div[3]/p"""
                          ]
    result_dict = dict()
    for category, xpath in zip(column_header, column_data_source):
        try:
            result_dict[category] = browser.find_element_by_xpath(
                xpath).text.encode('utf-8')
        except:
            print("Table read error")
            return result_dict

    return result_dict


def nserc_scrape(start_index, end_index):
    result_order_list = ["Index", "Competition Year", "Fiscal Year", "Project Lead Name",
                         "Institution", "Department", "Province", "Award Amount", "Installments",
                         "Program", "Selection Committee", "Research Subject",
                         "Area of Application", "Co-Researchers", "Partners", "Award Summary"
                         ]

    log_filename = 'log_{}_{}.txt'.format(start_index, end_index)
    result_filename = 'result_{}_{}.csv'.format(start_index, end_index)
    id_to_work_on = start_index
    if os.path.exists(log_filename):
        with open(log_filename, 'r') as log_file:
            try:
                print(" Resuming work")
                id_to_work_on = int(log_file.readline())
            except ValueError:
                id_to_work_on = start_index

    if not os.path.exists(result_filename):
        print("Saving in", result_filename)
        with open(result_filename, 'w') as results_file:
            csv_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(result_order_list)

    browser = initialize_browser()

    if id_to_work_on <= end_index:
        for index in xrange(id_to_work_on, end_index+1):
            if index % 50 == 0:
                print("{} Refreshing browser".format(
                    datetime.now().strftime('%Y-%m-%d %H:%M')))
                browser_quit(browser)
                browser = initialize_browser()

            print(index)
            browser_load_url(browser, BASE_URL + str(index))
            result_dict = {item: 'N/A' for item in result_order_list}
            result_dict.update(grab_data(browser))
            result_dict['Index'] = index
            with open(result_filename, 'a+') as results_file:
                csv_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
                csv_writer.writerow([result_dict[item]
                                     for item in result_order_list])
            with open(log_filename, 'w') as log_file:
                log_file.writelines('{}'.format(index+1))
            sys.stdout.flush()
    else:
        print("{} Finished".format(datetime.now().strftime('%Y-%m-%d %H:%M')))
    sys.stdout.flush()

    browser_quit(browser)


def is_intstring(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main(argv):
    """Main function to call scraper"""
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        print('test.py start_index end_index')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py start_index end_index')
            sys.exit()
    for arg in args:
        if not is_intstring(arg):
            sys.exit("All arguments must be integers. Exit.")
    if len(args) > 2:
        sys.exit("Too many arguments. Exit.")

    start_index = MIN_ID
    end_index = MAX_ID

    if len(args) == 1:
        if MIN_ID <= args[0] <= end_index:
            start_index = args[0]
    elif len(args) == 2:
        min_index = min(map(int, args))
        max_index = max(map(int, args))

        if MIN_ID <= min_index <= MAX_ID:
            start_index = min_index
        if MIN_ID <= max_index <= MAX_ID:
            end_index = max_index
    print("From {} to {}".format(start_index, end_index))
    print('{} Start'.format(datetime.now().strftime('%Y-%m-%d %H:%M')))
    nserc_scrape(start_index, end_index)


if __name__ == "__main__":
    main(sys.argv[1:])
