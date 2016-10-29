
# Drop all tables, allowing for a fresh start
import psycopg2

conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        host='127.0.0.1',
                        port='5432')
cur = conn.cursor()
print("DB: Connection successful.")

print('-> Dropping all the tables...')
cur.execute('DROP TABLE assignedto, board, card, categorizedas, category, composedof, contains, hasleader, intern, isbackloggedon, juniordev, runby, seniordev, team, teammember;')
print('-> Dropped all the tables.')

print('DB: Attempting commit and close...')
conn.commit()
conn.close()
print('\033[92mDB: Drop complete!\033[0m')
