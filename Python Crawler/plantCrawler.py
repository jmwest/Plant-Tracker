import sys
import time
import threading
import json
from concurrent.futures import ThreadPoolExecutor, wait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Exception Class Definition
class SaveException(Exception):
    def __init__(self, message):
        # Call base class constructor
        super(SaveException, self).__init__(message)

# Save Information Class Definition
class SaveInfo:
    save_dict = {}
    gen_i = 0
    counter_j = 0
    futures = []
    interrupted = False
    genus_url = ''
    genus_page_max = 0
    
    def __init__(self):
        pass

    def reset(self):
        self.save_dict = {}
        self.gen_i = 0
        self.counter_j = 0
        self.futures = []
        self.interrupted = False
        self.genus_url = ''
        self.genus_page_max = 0

    def print(self):
        print('\n', str(self.interrupted), '\n', str(self.gen_i), '\n', str(self.counter_j), '\n', str(self.genus_page_max), '\n', self.genus_url)
        print('\n', self.save_dict)

class CompletionInfo:

    global error_log
    genera_p = 0
    genera_m = 1
    genus_p = 0
    genera_m = 1
    current_page_p = 0
    current_page_m = 1

    def __init__(self):
        return

    def set_all(self, genera_percent, genera_max, genus_percent, genus_max, page_percent, page_max):
        self.genera_p = genera_percent
        if genera_max != 0:
            self.genera_m = genera_max
        self.genus_p = genus_percent
        if genus_max != 0:
            self.genus_m = genus_max
        self.current_page_p = page_percent
        if page_max != 0:
            self.current_page_m = page_max
        return
    
    def set_genera_counter(self, genera_percent):
        self.genera_p = genera_percent
        return

    def set_genera_max(self, genera_max):
        if genera_max != 0:
            self.genera_m = genera_max
        return
    
    def set_genus_counter(self, genus_percent):
        self.genus_p = genus_percent
        return

    def set_genus_max(self, genus_max):
        if genus_max != 0:
            self.genus_m = genus_max
        return
    
    def set_page_counter(self, page_percent):
        self.current_page_p = page_percent
        return

    def set_page_max(self, page_max):
        if page_max != 0:
            self.current_page_m = page_max
        return
    
    def update_progress(self):
        try:
            progress_file = open('progress.txt', 'w')
        except:
            try:
                error_log.write(get_time_string())
                error_log.write('- Unable to open progress.txt\n')
            except:
                print('Problem with error log in CompletionInfo class.\n')
            return
        else:
            progress_file.write('{:3.0f}'.format((self.genera_p/self.genera_m)*100) + '% of all genera pages complete.\n')
            progress_file.write('{:3.0f}'.format((self.genus_p/self.genus_m)*100) + '% of the current genus pages complete.\n')
            progress_file.write('{:3.0f}'.format((self.current_page_p/self.current_page_m)*100) + "% of the current genus' page complete.\n")
            progress_file.close()
        return

# Function to get a string of the current time
def get_time_string() -> str:
    t = time.localtime()
    return ('\n' + str(t.tm_mon) + '/' + str(t.tm_mday) + '/' + str(t.tm_year)[-2:] + ' ' + str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec) + ' ')

# Thread function to check user input
def get_user_input():
    my_bool = True
    while my_bool:
        if input() == 'save':
            sys.exit()

# Function to check the status of Thread1 (user input thread)
def check_thread1_alive() -> bool:
    return thread1.is_alive()

# Function to save current crawler status if program is exiting
def save_status():
    global save_dic
    global executor
    global driver
    if not write_save():
        save_dic.print()
    print('\nSaving...\nExit.')
    wait(save_dic.futures)
    executor.shutdown(wait=True)
    driver.quit()
    return

# Function to save the page output as JSON
def save_dic_as_JSON(s_dic):
    global file_lock
    global error_log
    file_lock.acquire()
    try:
        file = open('Database_save.txt', 'a')
    except:
        error_log.write(get_time_string())
        error_log.write('- Unable to save dic as JSON\n')
        for key, value in s_dic.items():
            error_log.write('\t' + str(key) + ' : ' + str(value) + '\n')
    else:
        save_out = json.dumps(s_dic, indent=2)
        file.write(save_out)
        file.close()
    file_lock.release()
    return

# consider changing the read/write functions to work with JSON <-> Dictionary conversion of saved values

# Function to read variables from the save file
def read_save() -> bool:
    global save_dic
    global error_log
    try:
        file = open('progress_save.txt', 'r')
    except:
        error_log.write(get_time_string())
        error_log.write('- Failed to read save or no save to read\n')
        return False
    save_dic.interrupted = bool(file.readline())
    save_dic.gen_i = int(file.readline())
    save_dic.counter_j = int(file.readline())
    save_dic.genus_url = file.readline().rstrip()
    save_dic.genus_page_max = int(file.readline())
    foo = False
    bar = False
    for line in file:
        if line.rstrip() == 'genus-indices':
            save_dic.save_dict['genus-indices'] = []
            save_dic.counter_j = save_dic.counter_j + 1
            foo = True
            bar = False
            continue
        if line.rstrip() == 'genera-indices':
            save_dic.save_dict['genera-indices'] = []
            foo = False
            bar = True
            continue
        if foo:
            save_dic.save_dict['genus-indices'].append(line)
        if bar:
            save_dic.save_dict['genera-indices'].append(line)
    file.close()
    return True

# Function to write variables to the save file
def write_save():
    global error_log
    try:
        file = open('progress_save.txt', 'w')
    except:
        error_log.write(get_time_string())
        error_log.write('- Failed to write save.\n')
        return False
    file.write(str(save_dic.interrupted) + '\n')
    file.write(str(save_dic.gen_i) + '\n')
    file.write(str(save_dic.counter_j) + '\n')
    file.write(save_dic.genus_url.rstrip() + '\n')
    file.write(str(save_dic.genus_page_max) + '\n')
    for key in save_dic.save_dict:
        file.write(key + '\n')
        for ndex in save_dic.save_dict[key]:
            file.write(ndex + '\n')
    file.close()
    return True

# THIS FUNCTION ISNT USED ?
# Function to convert dictionary to JSON
def output_data(dic, out_file):
    output = json.dumps(dic)
    out_file.write(output)
    return

# Function to scrape plant information from a page
def scrape_page(page_soup, url):
    global error_log
    dic = {}
    # search for the 'page-header' that contains the plant name and genus
    try:
        gsearch = page_soup.find_all('h1', class_='page-header')
    except:
        error_log.write(get_time_string())
        error_log.write('- No h1 for: ' + url + '\n')
        return
    try:
        genus = gsearch[0].find_all('a')[0].get_text()
    except:
        error_log.write(get_time_string())
        error_log.write('- Error finding a in h1 for: ' + url + '\n')
        return
    try:
        species = gsearch[0].get_text()
    except:
        error_log.write(get_time_string())
        error_log.write('- Error finding species.get_text() in h1 for: ' + url + '\n')
        return
    dic['genus'] = genus
    dic['species'] = species
    # search for 'col-sm-6' table containing the plant info
    try:
        search1 = page_soup.find_all('div', class_='col-sm-6')
    except:
        error_log.write(get_time_string())
        error_log.write('- No div for: ' + url + '\n')
        save_dic_as_JSON(dic)
        return
    # loop through all 'col-sm-6' classes
    for search2 in search1:
        try:
            search3 = search2.find_all('caption')               #find all 'caption' in 'col-sm-6' class
        except:
            error_log.write(get_time_string())
            error_log.write('- No caption for: ' + url + '\n')
            continue
        for search4 in search3:                                 #loop through every 'caption'
            if 'Plant Information' in search4.get_text():       #if caption is Plant Info
                try:
                    td = search2.find_all('td')                 #find all 'td' within 'col-sm-6' class
                except:
                    error_log.write(get_time_string())
                    error_log.write('- No td in caption for: ' + url + '\n')
                    continue
                i = 0
                while i < len(td):                              #loop through all 'td' to get plant values
                    try:
                        text = td[i].get_text()
                    except:
                        error_log.write(get_time_string())
                        error_log.write('- Unable to text=get_text() for td: ' + url + '\n')
                        continue
                    try:
                        value = td[i+1].get_text()
                    except:
                        error_log.write(get_time_string())
                        error_log.write('- Unable to value=get_text() for td: ' + url + '\n')
                        value = ''
                    if 'Plant Habit:' in text:                  #Assign value based on text if statements
                        dic['PlantHabit'] = value
                    elif 'Life cycle:' in text:
                        dic['LifeCycle'] = value
                    elif 'Sun Requirements:' in text:
                        dic['Sun'] = value
                    elif 'Water Preferences:' in text:
                        dic['Water'] = value
                    elif 'Soil pH Preferences:' in text:
                        dic['Soil pH'] = value
                    elif 'Plant Height:' in text:
                        dic['Height'] = value
                    elif 'Leaves:' in text:
                        dic['Leaves'] = value
                    elif 'Fruit:' in text:
                        dic['Fruit'] = value
                    elif 'Flowers:' in text:
                        dic['Flowers'] = value
                    elif 'Flower Color:' in text:
                        dic['Flower Color'] = value
                    elif 'Bloom Size' in text:
                        dic['Bloom Size'] = value
                    elif 'Suitable Locations:' in text:
                        dic['Locations'] = value
                    elif 'Resistances:' in text:
                        dic['Resistances'] = value
                    elif 'Propagation:' in text:
                        dic['Propagation'] = value
                    elif 'Containers:' in text:
                        dic['Containers'] = value
                    else:
                        if 'Other' in dic.keys():
                            dic['Other'][text] = value
                        else:
                            dic['Other'] = {text: value}
                    i = i + 2                                   #Iterate to next set of td
    save_dic_as_JSON(dic)
    return

# Function to generate an href list from a genus page
def crawl_index_page(index_soup):
    global error_log
    try:
        gensearch = index_soup.find_all('table', class_='table table-striped table-bordered table-hover pretty-table')
    except:
        error_log.write(get_time_string())
        error_log.write('- Unable to find_all("table") in crawl_index_page.\n')
        return []
    gen_list = []
    try:
        for a in gensearch[0].find_all('a', href=True):
            if (a.get_text() != ' ') and (a.get_text() != ''):
                gen_list.append(a['href'])
    except IndexError as err:
        error_log.write(get_time_string())
        error_log.write('- ' + str(err))
    return gen_list

# Function to iterate through each genus's index pages
def crawl_genus_page(genus_url, genus_soup=None, j=0, page_max=0, genus_index=[]):
    global completion_info
    global last_get_time
    global save_dic
    global driver
    global error_log
    try:
        if page_max == 0:
            # Take the offset=0 page results to find the total number of pages for the genus
            genus_pages_search = genus_soup.find_all('a', class_='PageInactive')
            for gen in genus_pages_search:
                if int(gen.get_text()) > page_max:
                    page_max = int(gen.get_text())
        # Set Completion Info
        completion_info.set_genus_counter(j)
        completion_info.set_genus_max(page_max)
        completion_info.update_progress()
        # Check to see if a genus_index is passed to the function
        if not genus_index:
            # Call crawl_index_page to get all of the species listed on offset=0 page
            genus_index = crawl_index_page(genus_soup)
            # Crawl through all species on the current page
            crawl_genus_index_page(genus_index)
            # While loop to move through all subsequent pages for the genus
        while j < (page_max - 1):
            j = j + 1
            completion_info.set_genus_counter(j)
            completion_info.update_progress()
            if not check_thread1_alive():
                raise SaveException('SaveException raised from crawl_genus_page')
            if (time.time() - last_get_time) < 2.0:
                time.sleep(2.0 - (time.time() - last_get_time))
            try:
                driver.get(genus_url + offset_url + str(_offset_mult*j))
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to complete driver.get in crawl_genus_page for: ' + genus_url + offset_url + str(_offset_mult*j) + '\n')
            else:
                last_get_time = time.time()
            try:
                gen_content = driver.page_source
                gen_soup = BeautifulSoup(gen_content, 'html.parser')
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to make soup in crawl_genus_page for offset: ' + genus_url + ' page:' + str(j) + '\n')
                continue
            else:
                gindex = crawl_index_page(gen_soup)
                crawl_genus_index_page(gindex)
    except (SaveException, KeyboardInterrupt):
        save_dic.interrupted = True
        save_dic.counter_j = j - 1
        save_dic.genus_url = genus_url
        save_dic.genus_page_max = page_max
        raise
    return

def crawl_genus_index_page(index):
    global completion_info
    global last_get_time
    global save_dic
    global executor
    global driver
    global error_log

    # Set Completion Info
    info_counter = 0
    completion_info.set_page_counter(info_counter)
    completion_info.set_page_max(len(index))
    completion_info.update_progress()
    try:
        for indx in index:
            if not check_thread1_alive():
                index_rem = []
                index_bool = False
                for dex in index:
                    if dex == indx:
                        index_bool = True
                    if index_bool:
                        index_rem.append(dex)
                save_dic.save_dict['genus-indices'] = index_rem
                raise SaveException('SaveException raised from crawl_genus_index_page')
            if (time.time() - last_get_time) < 2.0:
                time.sleep(2.0 - (time.time() - last_get_time))
            try:
                driver.get(base_url + indx)
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to complete driver.get in crawl_genus_index_page for: ' + base_url + indx + '\n')
            else:
                last_get_time = time.time()
            try:
                genus_content = driver.page_source
                genusoup = BeautifulSoup(genus_content, 'html.parser')
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to make soup in crawl_genus_index_page for genus: ' + indx + '\n')
                continue
            page_url = base_url + indx
            save_dic.futures.append(executor.submit(scrape_page, genusoup, page_url))
            # Set Completion Info
            info_counter = info_counter + 1
            completion_info.set_page_counter(info_counter)
            completion_info.update_progress()
    except (SaveException, KeyboardInterrupt):
        save_dic.interrupted = True
        raise
    return

#################
# Define main() #
def main():
    global file_lock
    file_lock = threading.Lock()
    
    # Start threads
    global thread1
    thread1 = threading.Thread(target=get_user_input)
    thread1.daemon = True
    thread1.start()

    global executor
    executor = ThreadPoolExecutor(20)

    # Declare globals
    global driver
    global error_log
    global completion_info
    global save_dic
    global last_get_time
    global browse_url
    global base_url
    global offset_url
    global _offset_mult

    # Initialize variables
    last_get_time = 0
    save_dic = SaveInfo()
    completion_info = CompletionInfo()
    completion_info.set_all(0, 1, 0, 1, 0, 1)
    browse_url = 'https://garden.org/plants/browse/plants/genus/?offset='
    base_url = 'https://garden.org'
    offset_url = '?offset='
    _offset_mult = 20
    _num_pages = 830 #should be 830

    # Update Completion Info
    completion_info.set_genera_max(_num_pages)
    try:
        driver = webdriver.Chrome("/opt/WebDriver/bin/chromedriver")
    except:
        error_log.write(get_time_string())
        error_log.write('- Unable to open Chrome webdriver.\n')
        sys.exit()

    # Loop to iterate through all genera
    i = 0
    if read_save():
        i = int(save_dic.gen_i)
    # Update Completion Info
    completion_info.set_genera_counter(i)
    completion_info.update_progress()
    # Check Interrupted progress
    if save_dic.interrupted:
        print('Handling start up from save. Do not save yet...\n')
        genus_indx = []
        if 'genus-indices' in save_dic.save_dict.keys():
            genus_indx = save_dic.save_dict['genus-indices']
            crawl_genus_index_page(genus_indx)
        if save_dic.genus_url != '':
            try:
                driver.get(save_dic.genus_url)
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to complete driver.get in interrupted reset for: ' + save_dic.genus_url + '\n')
            else:
                last_get_time = time.time()
                try:
                    i_content = driver.page_source
                    i_soup = BeautifulSoup(i_content, 'html.parser')
                except:
                    error_log.write(get_time_string())
                    error_log.write('- Unable to make soup in interrupted reset for url: ' + save_dic.genus_url + '\n')
                else:
                    crawl_genus_page(save_dic.genus_url, i_soup, save_dic.counter_j, save_dic.genus_page_max, genus_indx)
        if 'genera-indices' in save_dic.save_dict.keys():
            i = i + 1
            for _genera in save_dic.save_dict['genera-indices']:
                if (time.time() - last_get_time) < 2.0:
                    time.sleep(2.0 - (time.time() - last_get_time))
                try:
                    driver.get(base_url + _genera)
                except:
                    error_log.write(get_time_string())
                    error_log.write('- Unable to complete driver.get in interrupted reset for: ' + base_url + _genera + '\n')
                else:
                    last_get_time = time.time()
                    try:
                        genera_content = driver.page_source
                        gsoup = BeautifulSoup(genera_content, 'html.parser')
                    except:
                        error_log.write(get_time_string())
                        error_log.write('- Unable to make soup in interrupted reset for offset: ' + str(_offset) + '\n')
                        continue
                    else:
                        crawl_genus_page(base_url + _genera, gsoup)
        save_dic.reset()
    # There are issues if save is called during the interruption handling.
    print('Okay to save.\n')
    try:
        while i < _num_pages:
            completion_info.set_genera_counter(i)
            completion_info.update_progress()
            _offset = i
            i = i + 1
            if not check_thread1_alive():
                save_dic.interrupted = False
                raise SaveException('SaveException raised from main')
            try:
                driver.get(browse_url + str(_offset_mult*_offset))
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to complete driver.get in main for: ' + browse_url + str(_offset_mult*_offset) + '\n')
                continue
            else:
                last_get_time = time.time()
            try:
                content = driver.page_source
                soup = BeautifulSoup(content, 'html.parser')
            except:
                error_log.write(get_time_string())
                error_log.write('- Unable to make soup in main for offset: ' + str(_offset) + '\n')
                continue
            else:
                genera_list = crawl_index_page(soup)
                for genera in genera_list:
                    try:
                        if not check_thread1_alive():
                            raise SaveException('SaveException raised from main/genera_list')
                        if (time.time() - last_get_time) < 2.0:
                            time.sleep(2.0 - (time.time() - last_get_time))
                        try:
                            driver.get(base_url + genera)
                        except:
                            error_log.write(get_time_string())
                            error_log.write('- Unable to complete driver.get in main/genera_list for: ' + base_url + genera + '\n')
                        else:
                            last_get_time = time.time()
                            try:
                                genera_content = driver.page_source
                                gsoup = BeautifulSoup(genera_content, 'html.parser')
                            except:
                                error_log.write(get_time_string())
                                error_log.write('- Unable to make soup in main/genera_list for offset: ' + str(_offset) + '\n')
                                continue
                            else:
                                crawl_genus_page(base_url + genera, genus_soup=gsoup)
                    except (SaveException, KeyboardInterrupt):
                        save_dic.interrupted = True
                        index_rem = []
                        index_bool = False
                        for gen in genera_list:
                            if gen == genera:
                                index_bool = True
                            if index_bool:
                                index_rem.append(gen)
                        save_dic.save_dict['genera-indices'] = index_rem
                        raise
    except (SaveException, KeyboardInterrupt):
        save_dic.gen_i = i - 1
        wait(save_dic.futures)
        executor.shutdown(wait=True)
        driver.quit()
        raise
    else:
        # Clean up open operations
        wait(save_dic.futures)
        executor.shutdown(wait=True)
        driver.quit()

###############################
# If this file is run as main #
if __name__ == "__main__":
    global error_log

    # Open error log
    try:
        error_log = open('error_log.txt', 'a')
    except:
        print('Error log failed to open. Exiting...\n')
        sys.exit(1)
    
    try:
        main()
    except (SaveException, KeyboardInterrupt) as exc:
        save_status()
        error_log.write(get_time_string())
        error_log.write('- Saved after exception: ')
        error_log.write(str(exc) + '\n')
        error_log.close()
        sys.exit(1)
    except Exception as e:
        save_status()
        error_log.write(get_time_string())
        error_log.write('- Saved after unknown exception: ')
        error_log.write(str(e) + '\n')
        error_log.close()
        sys.exit(1)
    except:
        save_status()
        error_log.write(get_time_string())
        error_log.write('- Saved after unknown error in main.\n')
        error_log.close()
        sys.exit(1)
    else:
        error_log.close()
        sys.exit(0)
