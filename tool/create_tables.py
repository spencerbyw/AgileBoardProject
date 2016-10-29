
# Attempts to create all the tables, prepped for insertion
import psycopg2

conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        host='127.0.0.1',
                        port='5432')
cur = conn.cursor()
print("DB: Connection successful.")

with open('sql/create/tables.sql') as f:
    create_query = f.read()

print('-> Creating all the tables...')
cur.execute(create_query)
print('-> Created all the tables.')

print('DB: Attempting commit and close...')
conn.commit()
conn.close()
print('\033[92mDB: Create complete!\033[0m')
