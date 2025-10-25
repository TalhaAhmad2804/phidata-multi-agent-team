import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="talhaahmad")

cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS chats
""")

conn.commit()