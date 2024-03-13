from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4
from db_stuff import populate_table, create_table

# create_table()
for p in range(1, 2700):
    url = f"https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata/?page={p}"
    driver = webdriver.Firefox()
    driver.get(url)
    
    cnt = 1
    pg = 2
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "table")))
    except:
        print("Couldnt load the data table")
        exit(1)
    html = driver.page_source
    html_parsed = bs4(html, "html.parser")
    t = html_parsed.find("table", {"class": "list_table"})
    for row in t.find_all("tr")[1:]:
        # cols = row.find_elements(By.TAG_NAME, "td") doesnt work
        cols = row.find_all("td")
        item={}
        if len(cols):
            item["sno"]= cols[0].text,
            item["pub_date"]= cols[1].text,
            item["bid_sub_close"]= cols[2].text,
            item["tend_open"]= cols[3].text,
            item["title"]= cols[4].text,
            item["org"]= cols[5].text,
            item["link"]= cols[4].find("a").get("href"),
            driver.find_element(
                    By.XPATH, '//*[@id="table"]/tbody['+str(cnt)+']/tr/td[5]/a').click()
            # if linktxt: 
            # doesnt work tried opening it in a new tab and then getting
            #     driver.execute_script("window.open('', '_blank');")
            #     driver.switch_to.window(driver.window_handles[1])
            #     driver.get(linktxt)
            try:
                # wait for captcha to laod
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//img[@title="Image CAPTCHA"]')))
            except:
                print("CAPTCHA didnt load")
                exit(1)
            # get captcha value from alt of the img
            cap = driver.find_element(By.XPATH, '//img[@title="Image CAPTCHA"]').get_attribute("alt")
            i = driver.find_element(By.XPATH, '//input[@id="edit-captcha-response"]')
            # enter captcha into input
            i.click()
            i.send_keys(cap)
            # submit captcha
            submit = driver.find_element(By.XPATH, '//input[@id="edit-save"]')
            submit.click()
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="tfullview"]/div/table[4]/tbody')))
            except:
                print("table didnt load for the tender")
                exit(1)
            t = driver.find_element(By.XPATH, '//div[@id="tfullview"]/div/table[4]/tbody')
            item["refno"] = t.find_element(By.XPATH, '//tr[2]/td[3]').text
            item["tend_type"] = t.find_element(By.XPATH, '//tr[2]/td[6]').text
            item["tend_cat"] = t.find_element(By.XPATH, '//tr[2]/td[6]').text
            item["fee"] = t.find_element(By.XPATH, '//tr[4]/td[6]').text
            item["loc"] = t.find_element(By.XPATH, '//tr[5]/td[6]').text
            item["emd"] = t.find_element(By.XPATH, '//tr[5]/td[3]').text

            t = driver.find_element(By.XPATH, '//div[@id="tfullview"]/div/table[8]/tbody')
            item["des"] = t.find_element(By.XPATH, '//tr[1]/td[3]/div').text
            item["doc"] = t.find_element(By.XPATH, '//tr[2]/td[3]/div/a').text
            populate_table(item)
        cnt+=1
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "table")))
        except:
            print("Couldnt load the data table")
            exit(1)
    driver.close() 

