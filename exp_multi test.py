### 위에 둘을 합침 ####
from database import config
import mysql.connector
import numpy as np

def giveme_fresh_gid(multi):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    cursor.execute(
        """
        select gid from news_gpt.remote_question where questions is NULL and checked is NULL limit 10
        """
    )
    candidate =  cursor.fetchall()
    if len(candidate)==0:
        print(f'{multi} end  print')
        return(f'end')
        # raise Exception("더 할거 없음")

    n_overlap = 0
    while True:
        gid = candidate[np.random.randint(len(candidate))][0]
        # gid= '100000119'
        cursor.execute(
            f"""
            update news_gpt.remote_question set checked = '1' where gid = '{gid}' and checked is NULL
            """
        )
        if cursor.rowcount == 0:
            n_overlap +=1

            if n_overlap > 10:
                print(f"{multi} 넘침")
                return giveme_fresh_gid(multi)
                # break
            print(f'{multi}  shit {n_overlap}')
            pass
        else:
            db.commit()
            return gid
            # break



#### 프롬프트 만들기 #####
import codecs

def giveme_prompt(gid):
    ## document 
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        f"""
        select title, createtime, content from news_gpt.remote_question where gid = "{gid}"
        """
    )
    title, createtime, content =  cursor.fetchall()[0]
    content = codecs.decode(content, 'utf-8')

    document = f"""title: {title}
create date: {createtime}
text:{content}
"""

    ## prompt sheet

    prompt= """Instruction: Your task is two things.
1. show all full name of proper nouns(name and title of celebrity, organization name) from the document enclosed in three single quotation marks, which is used multiple time.
2. Present 15 questions for which you can hint from the document enclosed in three single quotation marks. Avoid questions whose answer exists in the form of a span in the text .
For the names of people and organizations, NEVER use abbreviations.
use the following format for 2 tasks:
{"proper_noun":["Alpha", "Beta", "Gamma"],"questions":["qeustion1", "question2", "question15"]}
document : 
'''
"""+ document+"'''"
    return prompt



import multiprocessing
import time
def each(result_list, i):
    print('yoyoyo')
    while True:
        
        gid = giveme_fresh_gid(i)
        print(f"{i}  {gid}")
        result_list.append(gid)
        if gid == 'end':
            return "done"

def do():
    print('here2')
    result_list = multiprocessing.Manager().list()
    processes = []
    for i in range(3):
        print(f'here   {i}')
        p = multiprocessing.Process(target=each, args=(result_list, i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    return list(result_list)
if __name__ == "__main__":
    print(do())
    