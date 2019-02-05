import time
import armenianwords
import bs4
# from pyvirtualdisplay import Display
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from armenianwords.utils.logger import logger


def google_search():
    full_path = "/home/vahagn/dev/playground/my_projects/armenianwords/utils/chromedriver"
    google_path = 'https://www.google.com/'
    # display = Display(visible=0, size=(1280, 1024))
    # display.start()
    driver = webdriver.Chrome(executable_path=full_path)
    driver.get(google_path)
    search_bottom = driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')
    search_bottom.click()
    # time.sleep(1)
    search_bottom.clear()
    search_bottom.send_keys("online bararan")
    search_bottom.send_keys(Keys.RETURN)
    time.sleep(1)
    link_for_profiles = driver.find_elements_by_class_name("LC20lb")[0]
    link_for_profiles.click()
    return driver


def find_letter(driver, letter_number: int):
    letter = driver.find_elements_by_class_name("letters-href")[letter_number]
    letter.click()

    logger.info("sleeping in 2 mins")
    time.sleep(2)
    return driver


def parse_words(driver):
    html_soup = driver.page_source
    soup1 = bs4.BeautifulSoup(html_soup, "html.parser")

    word_list = []
    containers = soup1.find_all("a", {"class": "word-href"})
    for container in containers:
        # print(container.text)
        word_list.append(container.text)
    return word_list


def change_page(driver, page_number: int):
    search = driver.find_elements_by_xpath('//input[@class="go-to-page rounded p-1"]')[0]
    search.click()
    time.sleep(1)
    search.clear()
    search.send_keys(str(page_number))
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    return driver


if __name__ == '__main__':
    web_driver = google_search()
    logger.info("Google search is over")
    # for i in range(39):
    # for j in range(3,39):
    letter_driver = find_letter(web_driver, 3)
    with open("letter_{}.txt".format(3), "wb") as f:
        for i in range(0, 210):
            if i == 0:
                word_list = parse_words(letter_driver)
                time.sleep(3)
            else:
                changed_page = change_page(letter_driver, i + 1)
                word_list = parse_words(changed_page)
                time.sleep(3)

            for word in word_list:
                print(word)
                f.write(word.encode())

    logger.info("parsed soup")
    letter_driver.quit()
