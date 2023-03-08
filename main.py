# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
import student_info
from bb_info import *

while True:
    subject = input(
        "PLease provide a subject name as the folder (Ex: EIE2001):")
    try:
        folder_location = os.path.join(os.getcwd(), subject)
        if not os.path.exists(folder_location):
            os.mkdir(folder_location)
        break
    except Exception as e:
        print(f"{subject} is not a valid folder name, please modify")
        continue

# Configuration for browser to download automatically and to a specific directory
options = webdriver.ChromeOptions()
chrome_prefs = {
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.open_pdf_in_system_reader": False,
    "profile.default_content_settings.popups": 0,
    "download.default_directory": folder_location
}
options.add_experimental_option("prefs", chrome_prefs)

# Note: require chromedriver.exe in path, you may put it in directory with the script
driver = webdriver.Chrome(options=options)

# BB's login page
driver.get(base_url)
# Enter student ID and password and login
# input student id
driver.find_element(By.XPATH, input_SID_xpath).send_keys(student_info.S_ID)
# input password
driver.find_element(By.XPATH,
                    input_password_xpath).send_keys(student_info.password)
# Login
driver.find_element(By.XPATH, login_button_xpath).send_keys(Keys.ENTER)

# cookie agreement
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, privacy_cookie_page_button_bb_xpath)
    )
)
driver.find_element(By.XPATH,
                    privacy_cookie_page_button_bb_xpath).send_keys(Keys.ENTER)

# Go to course page
driver.get(base_url+coures_page)
# Now manually go to the target page that you would like to start your download

# %% [markdown]
# Manually go to a main content page of a course

# %%
IS_TEST = False  # This only works for CSC3100 2022-2023 Fall Term course
# if not please manually go to the Main content page
# An example url for main content page is below
# https://bb.cuhk.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_8275_1&content_id=_274527_1&mode=reset
if IS_TEST:
    course_page = "webapps/blackboard/execute/modulepage/view?course_id={course}&cmp_tab_id={cmp_tab}"
    course_content_page = "webapps/blackboard/content/listContent.jsp?course_id={course}&content_id={content}"
    course_id = "_8275_1"  # Not useful, it is course specific one
    cmp_tab_id = '_17861_1'
    main_content_id = '_274527_1'
    # This may needs automation
    my_url = base_url + \
        course_content_page.format(course=course_id, content=main_content_id)
    driver.get(my_url)
else:
    input("Is the browser at the content page? then press Enter ")


def save_text_in_page(file: str = "Obtain_text.txt", title=""):
    # Obtain page title
    if title == "":
        try:
            title = driver.find_element(By.ID, "pageTitleText").text
        except Exception as e:
            print(e)
            pass
    else:
        title = "page_title"
    # begin writing to file
    with open(file, 'a') as f:
        f.write("-"*5 + title + "-"*5 + "\n")

    # Scrape plain text from contentlist
    try:
        content_list = driver.find_element(By.ID, "content_listContainer")
        text_elements = content_list.find_elements(By.CLASS_NAME, "read")
        for ele in text_elements:
            with open(file, 'a') as f:
                f.write("\t" + ele.text.replace("\n", "    ") + '\n')
    except Exception as e:
        print(e)
    # Ending
    with open(file, 'a') as f:
        f.write("="*5 + f"END {title}" + "="*5 + "\n")


def download_files_from_this_page(total_file_links=[], pass_folder_links=[], depth=0, max_depth=-1):
    if max_depth >= 0 and depth > max_depth:
        return
    # locate file links in this page
    try:
        content_list = driver.find_element(By.CLASS_NAME, "contentList")
        page_urls = content_list.find_elements(By.TAG_NAME, 'a')

        # print(len(set(page_urls)) == len(page_urls)) # whether all urls in this page are unique, seems always True

        for url in page_urls:
            page_url = url.get_attribute('href')
            if 'bbcswebdav' in page_url and page_url not in total_file_links:
                total_file_links.append(page_url)
                print("find new file link: ", page_url)
    except NoSuchElementException:
        # print("Content list not found in {driver.current_url}")
        pass
    except Exception as e:
        print(e)
    pass_folder_links.append(driver.current_url)
    # locate each folder
    folder_links = []
    try:  # avoid stale references errors?
        folders = driver.find_element(
            By.XPATH, folder_entry_xpath).find_elements(By.CLASS_NAME, "read")
        for ele in folders:
            try:
                ref_link = ele.find_element(
                    By.TAG_NAME, 'a').get_attribute('href')
                if content_url in ref_link and ref_link not in folder_links and ref_link not in pass_folder_links:
                    folder_links.append(ref_link)
                    print("Add folder link", ref_link)
                else:
                    # print(f"{ref_link} is not a folder link in bb")
                    pass
            except NoSuchElementException:
                # print(f"No element found in {ele.text}")
                continue
    except:
        pass
    # go through each folder
    for url in folder_links:
        driver.get(url)
        pass_folder_links.append(url)
        print("Enter folder link: ", url)
        download_files_from_this_page(
            total_file_links, pass_folder_links, depth+1)

    if depth == 0:
        with open('file_links.txt', 'a') as f:
            for url in total_file_links:
                f.write(url + "\n")

        # download all file in file_links
        print("-"*10, "download starts", "-"*10)
        for idx, url in enumerate(total_file_links):
            if idx % 5 == 0:
                sleep(5)  # No meaning, please ignore
            driver.get(url)
        print("-"*10, "download has finished", "-"*10)


file_links = []
passed_folder_links = []
depth = 0  # download collected files at depth 0
max_depth = -1  # no maximum depth
download_files_from_this_page(
    total_file_links=file_links, pass_folder_links=passed_folder_links, depth=depth, max_depth=max_depth
)

# obtain plain text info from each page
text_file = f"{subject}/{subject}_scraped_text.txt"
for link in passed_folder_links:
    driver.get(link)
    save_text_in_page(file=text_file)
# All has finished here, you may run next blcok or simply shutdown the script if your download is satisfied


# %%
driver.close()  # Everything done!


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%
# Below are useless only for my testing


# %%
content_ele = driver.find_element(By.XPATH, folder_entry_xpath)
print("--"*5 + "possible folder names " + "--"*5)
print(content_ele.text)

# Obtain each folder's reference link
# folders = driver.find_elements(By.CLASS_NAME, "read")
folders = content_ele.find_elements(By.CLASS_NAME, "read")

folder_links = []
ref_link = ""

for element in folders:
    try:
        a_tag = element.find_element(By.TAG_NAME, 'a')
    except NoSuchElementException:
        print(f"No element found in {element.text}")
        continue
    ref_link = a_tag.get_attribute('href')
    if content_url in ref_link:
        folder_links.append(ref_link)
    else:
        print(f"{ref_link} is not a folder link in bb")
print("--"*5 + "Folder links" + "--"*5)
print(folder_links)


# %%
# Obtain download urls from current page
file_links = []
try:
    content_list = driver.find_element(By.CLASS_NAME, "contentList")
    page_urls = content_list.find_elements(By.TAG_NAME, 'a')

    print(len(set(page_urls)) == len(page_urls))
    with open("file_link.txt", 'w') as f:
        with open('other_link.txt', 'w') as f2:
            for url in page_urls:
                page_url = url.get_attribute('href')
                if 'bbcswebdav' in page_url and page_url not in file_links:
                    file_links.append(page_url)
                    f.write(page_url + '\n')
                else:
                    f2.write(page_url + '\n')
except NoSuchElementException:
    print("Content list not found in {driver.current_url}")


# for url in page_urls:
#     print(url.get_attribute('href'))


# %%
real_file_links = []

with open('pdf_link.txt', 'w') as f:

    for url in file_links:
        driver.get(url)
        real_file_links.append(driver.current_url)
        print(driver.current_url)
        f.write(driver.current_url + '\n')


# %%
# Download pdf from url to specific folders https://scripteverything.com/download-pdf-selenium-python/
js_script = f''' 
			body = document.querySelector('body');
			element = document.createElement('a');
            element.href = "{real_file_links[5]}"
            element.download = "";
			text = document.createTextNode('Hello WOrld YABINYABIN');
			element.appendChild(text);
			body.append(element);
            //element.click()
'''

driver.execute_script(js_script)


# %%
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    # Change default directory for downloads
    "download.default_directory": "C:/Users/XXXX/Desktop",
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    # It will not show PDF directly in chrome
    "plugins.always_open_pdf_externally": True
})
driver.create_options()


# %%

driver.get(
    'https://bb.cuhk.edu.cn/bbcswebdav/pid-317351-dt-content-rid-4972414_1/xid-4972414_1')


# %%
for url in folder_links:
    driver.get(url)
    sleep(20)


# %%
driver.close()
