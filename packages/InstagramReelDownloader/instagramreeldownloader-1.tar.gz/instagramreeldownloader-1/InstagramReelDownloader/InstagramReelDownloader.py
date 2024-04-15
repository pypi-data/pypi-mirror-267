import itertools
import random
import urllib
from urllib import request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import quote
from re import fullmatch
import time , os


class ReelDownload:
    def __init__(self,reel_url, file_name="reel.mp4"):
        chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        chrome_options = Options()
        options = [
            "--headless" ,
            "--disable-gpu" ,
            "--window-size=1920,1200" ,
            "--ignore-certificate-errors" ,
            "--disable-extensions" ,
            "--no-sandbox" ,
            "--disable-dev-shm-usage"
        ]
        for option in options:
            chrome_options.add_argument(option)

        self.driver = webdriver.Chrome(service=chrome_service , options=chrome_options)
        self.wait_10 = WebDriverWait(self.driver , 10)
    #
    # def get(self, reel_url, file_name="reel"):
        reel_id = (reel_url.rsplit('/reel/' , 1)[1]).rsplit('/' , 1)[0]
        self.driver.get(f"https://www.instagram.com/reel/{reel_id}/")
        time.sleep(5)

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" ,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/88.0.705.81 Safari/537.36" ,
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36" ,
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36" ,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"
        ]
        try:
            video_src = self.wait_10.until(EC.presence_of_element_located((By.XPATH ,
                                                                           '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div[1]/article/div/div[1]/div/div/div/div/div/div/div/video'))).get_attribute(
                'src')
            headers = {'User-Agent': random.choice(user_agents)}
            request = urllib.request.Request(video_src , headers=headers)

            try:
                with urllib.request.urlopen(request) as response:
                    with open(file_name , 'wb') as f:
                        f.write(response.read())
            except Exception as e:
                print(f"An error occurred while downloading the image: {e}")


        except Exception as e:
            print('Something went wrong.')
            print(e)
            input("wait..")
            # self.driver.close()
            # self.driver.quit()
