#### 프롬프트 만들기 #####
import codecs
import mysql.connector
from database import config

def giveme_prompt(gid):
    ## document 
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        f"""
        select title, createtime, content, length from news_gpt.remote_sampled_ordered where gid = "{gid}"
        """
    )
    title, createtime, content, length =  cursor.fetchall()[0]
    content = codecs.decode(content, 'utf-8')

    document = f"""title: {title}
create date: {createtime}
text:{content}
"""

    # 문제 수
    if length <300 :
        n_elastic = 10
        n_factorial = 5
    elif length <500:
        n_elastic = 20
        n_factorial = 5
    elif length <700:
        n_elastic = 30
        n_factorial = 5
    elif length <1000:
        n_elastic = 40
        n_factorial = 5
    else:
        n_elastic = 100
        n_factorial = 10
        

    ## prompt sheet
    prompt=f"""{document}
---------------------------------
위 기사를 읽고, 한국의 정치, 사회, 경제, 문화, 산업 등 다양한 문제에 관심이 있는 사람이 기자와 전문가에게 물어보고싶을 만한 질문 {n_elastic}개를 자유롭게 만들어줘. 기사와 직접 관련이 없는 분야에 대해서도 질문해줘. 위 기사에서만 알 수 있는 사실확인 문제도 {n_factorial}개 내줘

기사를 읽지 않아도 질문이 이해되도록 완결성 있는 문장으로 써줘. 
"""
    return prompt






#     prompt= """Instruction: Your task is two things.
# 1. show all full name of proper nouns(name and title of celebrity, organization name) from the document enclosed in three single quotation marks, which is used multiple time.
# 2. Present 15 questions for which you can hint from the document enclosed in three single quotation marks. Avoid questions whose answer exists in the form of a span in the text .
# For the names of people and organizations, NEVER use abbreviations.
# use the following format for 2 tasks:
# {"proper_noun":["Alpha", "Beta", "Gamma"],"questions":["qeustion1", "question2", "question15"]}
# document : 
# '''
# """+ document+"""'''
# reply in 한국어"""