
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
    with open('data/%s' % fname, 'r') as f:
        cur.copy_from(f,
            fname.split('/')[-1].split('.')[0],
            sep=',',
            columns=columns)
    print('-> Successfully filled %s' % fname)


fill_data('Board.csv')
fill_data('Team.csv')
fill_data('Category.csv', columns=('title', 'description'))
fill_data('Card.csv', columns=('due_date', 'priority', 'description', 'title'))
fill_data('TeamMember.csv')
fill_data('SeniorDev.csv')
fill_data('JuniorDev.csv')
fill_data('Intern.csv')
fill_data('contains.csv')
fill_data('isBackloggedOn.csv')
fill_data('categorizedAs.csv')
fill_data('runBy.csv')
fill_data('hasLeader.csv')
fill_data('composedOf.csv')
fill_data('assignedTo.csv')

print('DB: Attempting commit and close...')
conn.commit()
conn.close()
print('\033[92mDB: Fill complete!\033[0m')
