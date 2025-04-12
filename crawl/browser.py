import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


HEAD_LESS = False  # 是否使用無頭模式


def trigger_course_requests():
    chrome_options = Options()
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:8080")
    chrome_options.add_argument('--ignore-certificate-errors')
    if HEAD_LESS:
        chrome_options.add_argument("--headless=new")  # 避免 GUI 開啟

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://courseap2.itc.ntnu.edu.tw/acadmOpenCourse/index.jsp")

    time.sleep(5)
    driver.find_element(By.ID, "treeview-1012-record-C1").click()
    driver.find_element(By.ID, "tab-1019-btnInnerEl").click()
    driver.switch_to.default_content()
    iframe = driver.find_element(By.ID, "C1").find_element(By.ID, "C1_iframe")
    driver.switch_to.frame(iframe)

    driver.find_element(By.ID, "ext-gen1162").click()
    inquire = driver.find_element(By.ID, "tab-1051-btnEl")
    details = driver.find_element(By.ID, "tab-1052-btnEl")

    departments = driver.find_elements(
        By.XPATH, '//*[@id="boundlist-1059-listEl"]/ul/li')
    for i in range(1, len(departments) + 1):
        inquire.click()
        driver.find_element(By.ID, "ext-gen1162").click()
        department = driver.find_element(
            By.XPATH, f'//*[@id="boundlist-1059-listEl"]/ul/li[{i}]')
        department.click()
        driver.find_element(By.ID, "button-1012-btnInnerEl").click()
        details.click()
        time.sleep(1)

    driver.switch_to.default_content()
    time.sleep(15)
    driver.quit()
