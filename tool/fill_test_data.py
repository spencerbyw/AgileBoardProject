
# Run this from the AgileBoardProject directory (use `make fill_test_data`)
import psycopg2

conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        host='127.0.0.1',
                        port='5432')
cur = conn.cursor()
print("DB: Connection successful.")

def fill_data(fname, columns=None):
    print('-> Filling %s' % fname)
    with open(fname, 'r') as f:
        cur.copy_from(f,
            fname.split('/')[-1].split('.')[0],
            sep=',',
            columns=columns)
    print('-> Successfully filled %s' % fname)


fill_data('data/Board.csv')
fill_data('data/Team.csv')
fill_data('data/Category.csv', columns=('title', 'description'))
fill_data('data/Card.csv', columns=('due_date', 'priority', 'description', 'title'))
fill_data('data/TeamMember.csv')
fill_data('data/SeniorDev.csv')
fill_data('data/JuniorDev.csv')
fill_data('data/Intern.csv')

print('DB: Attempting commit and close...')
conn.commit()
conn.close()
print('DB: Fill complete!')
