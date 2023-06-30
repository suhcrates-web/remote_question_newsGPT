from database import config
import mysql.connector
import numpy as np

db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute(
    """
    select gid from news_gpt.remote_question where questions is NULL and checked is NULL limit 5
    """
)
print(cursor.fetchall())

np.random.randint(5)