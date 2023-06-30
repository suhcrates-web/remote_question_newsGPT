from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def send_key_really(driver0, id, letters, cmd=''):
    suc0 = False
    
    # check if element is writable
    while suc0 == False:
        try:
            elem = driver0.find_element(By.ID, id)
            elem.send_keys('')

            suc0 = True
        except:
            pass

    suc0 = False
    # print(letters)
    while suc0 == False:
        # print(f"{letters} a")
        elem.send_keys('a')
        len0 = len(driver0.find_element(By.ID, id).get_attribute('value'))
        if len0 > 0:
            suc0 = True

        for _ in range(len0):
            elem.send_keys(Keys.BACKSPACE)

    # elem.send_keys(letters)
    # elem.send_keys('\n')


    # # # letter 써넣기. 한글자씩 써넣어야 사람이 쓰는줄 앎.
    # letters = letters.replace('\n','♡')  # 실제론 별로 의미가 없음. prompt에 \n으로 넣어봐야 실제로는 \\n으로 입력되기때문.
    # # #그냥 처음부터 \n을 ♡로 바꿔서 입력시키는게 나음.
    
    # # 줄 띄우기. 
    # for i in letters:
        
    #     if i == '♡':
    #         elem.send_keys(Keys.SHIFT + '\n')
    #     else:
    #         elem.send_keys(i)


    ##다른버전
    # letter_list = letters.split('\n')
    # for line in letter_list:
    #     elem.send_keys(line)
    #     elem.send_keys(Keys.SHIFT + '\n')
    # if cmd == 'go':
    #     elem.send_keys('\n')

    ##다른버전
    letter_list = letters.split('\n')
    input0 = ''
    for line in letter_list:
        input0 += line + Keys.SHIFT + '\n' +Keys.NULL
    elem.send_keys(input0)
    time.sleep(1)
    elem.send_keys('\n')