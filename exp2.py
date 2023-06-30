from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
from ToolBox_selenium import send_key_really
from selenium.webdriver.common.by import By
from giveme_fresh_gid import giveme_fresh_gid
from giveme_prompt import giveme_prompt
import mysql.connector
from database import config
import binascii

## selenium 최근 버전에선 이렇게 'service'를 통해 열어야됨. 아래와 같이 설정해야됨
service = Service(executable_path=r'C:/stamp/chromedriver')
chrome_options = Options()

## selenium으로는 크롬에 로그인할 수 없음. 다만 크롬에 로그인된 채 브라우저를 열 수는 있음. 다음과 같이 그렇게 함.
user_data_dir = os.path.expanduser(r'C:\Users\DONGA\AppData\Local\Google\Chrome\User Data')  # r' 해야함.  \U 가 unicode 열겠다는거기때문.  r'' 은 raw 로 읽겠다는거임
chrome_options.add_argument(f"user-data-dir={user_data_dir}")

driver = webdriver.Chrome(service =service, options=chrome_options)    # 다른 크롬드라이버에 다른아이디로라도 로그인된채로 열려있으면 안됨.


# Navigate to a URL
driver.get("https://accounts.google.com/")
# 여기서 chat.openai.com 으로 직접 타고 들어가야됨.


input("continue:")

while True:
    gid = giveme_fresh_gid(1)
    prompt = giveme_prompt(gid)
    send_key_really(driver, 'prompt-textarea', prompt, cmd='go')
    
    def wait():
        # 생겼는지 체크
        while True:
            streaming = driver.find_elements(By.CLASS_NAME,"result-streaming")
            if len(streaming) >= 1:
                break
            else:
                time.sleep(0.3)
                pass
        
        #없어졌는지 체크
        while True:
            streaming = driver.find_elements(By.CLASS_NAME,"result-streaming")
            if len(streaming) >= 1:
                time.sleep(0.5)
                pass
            else:
                break
    
        # input("keep going:")


        # 'Continue generating' 인지 확인
        cont_gen = driver.find_elements(By.CLASS_NAME,"btn-neutral")
        if len(cont_gen) ==2:
            cont_gen[-1].click()
            wait()
        

    wait()

    
    markdown = driver.find_elements(By.CLASS_NAME, 'markdown')

    if markdown == []:   # 네트워크에러 났을 가능성이 높음
        print("[]결과 나옴")  # 이러면 그냥 아무것도 안되고 있을 가능성이 높음. 에러 문자 보내야할듯.
        
    else:
        question = markdown[-1].text
        question = bin(int(binascii.hexlify(question.encode('utf-8')), 16))[2:]
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        cursor.execute(
            f"""
            update news_gpt.remote_question set questions = b'{question}' where gid = '{gid}' 
            """
        )

        time.sleep(3)