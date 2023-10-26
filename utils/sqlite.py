import sqlite3
from data import orm


def migr_users():
    connection = sqlite3.connect(r'database.db')
    cursor = connection.cursor()


    user = cursor.execute('SELECT * FROM users').fetchall()
    prod = cursor.execute('SELECT * FROM users_product').fetchall()
    print(len(user))
    for us in user:
        orm.db_add_user(user_id=us[1])

    for pr in prod:
        p = dict()
        p['user_id'] = pr[0]
        p['id_prod'] = pr[1]
        p['name_prod'] = pr[2]
        p['start_price'] = pr[3]
        p['min_price'] = pr[4]
        p['price'] = pr[5]
        p['pars_price'] = pr[5]
        p['photo_link'] = pr[6]
        p['link'] = pr[7]
        orm.db_add_product(p)
        print('ok')


