### 위에 둘을 합침 ####
from database import config
import mysql.connector
import numpy as np

def giveme_fresh_gid(multi):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    cursor.execute(
        """
        select gid from news_gpt.remote_sampled_ordered where questions is NULL and checked is NULL limit 10
        """
    )
    candidate =  cursor.fetchall()
    if len(candidate)==0:
        raise Exception("작업 끝")   ### 실제 멀티 ec2 환경에서는 작업 멈추도록 함. 멀티프로세싱이 아니기때문.
        # print(f'{multi} end  print')
        # return(f'end')
        # raise Exception("더 할거 없음")

    n_overlap = 0
    while True:
        gid = candidate[np.random.randint(len(candidate))][0]
        # gid= '100000119'
        cursor.execute(
            f"""
            update news_gpt.remote_sampled_ordered set checked = '1' where gid = '{gid}' and checked is NULL
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

if __name__ == "__main__":
    gid =giveme_fresh_gid()
    print(giveme_fresh_gid())
    print(gid)