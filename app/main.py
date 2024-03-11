from selenium import webdriver
from selenium.webdriver.chromium import options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from fastapi import FastAPI
from app.driver import create_driver
app = FastAPI()


@app.get("/")
def read_root():
    return { "Jai Mata Di"}

@app.get("/codechef")
def codechef(username: str):
    url = f"https://www.codechef.com/users/{username}"
    driver = create_driver()

    try:
        response = driver.get(url)
        rating_header = driver.find_element(By.CLASS_NAME, "rating-header")
        rating = rating_header.find_element(By.CLASS_NAME, "rating-number").text
        max_rating = rating_header.find_element(By.TAG_NAME, 'small').text[1:-1].split()
        rating_star = len(driver.find_element(By.CLASS_NAME, "rating-star").find_elements(By.TAG_NAME, 'span'))
        ranks = driver.find_element(By.CLASS_NAME, "rating-ranks").find_element(By.TAG_NAME, 'strong')
        global_rank = ranks.text
        country_rank = ranks.text
        rows = driver.find_elements(By.XPATH, "//table[@class='dataTable']/tbody/tr")
        last_submissions = []

        if len(rows) <= 0:
            return {"error" : "Not Question"}

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if columns[0].get_attribute("title") == "No Recent Activity" :
              return {"error" : "Not Question"}
            last_submission_time = columns[0].get_attribute("title")
            last_submission_question = columns[1].text
            last_submission_lang = columns[3].text
            last_submission_status = "Fail" if columns[2].text != '(100)' else "Success"

            last_submission_data = {
                "submission_status": last_submission_status,
                "submission_time": last_submission_time,
                "submission_question": last_submission_question,
                "submission_language": last_submission_lang
            }
            last_submissions.append(last_submission_data)

    except Exception as e:
        return {"error": "User not found"}
    finally:
        driver.close()
        driver.quit()

    return {
        'status': 'OK',
        'username': username,
        'rating': rating,
        'max_rating': max_rating,
        'global_rank': global_rank,
        'country_rank': country_rank,
        'recent_submission' : last_submissions
    }
