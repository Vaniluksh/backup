# -*- coding: utf-8 -*-
import pymysql

host = 'souschef4.cpnuf7y1bad6.us-east-2.rds.amazonaws.com'
port = 3306
user = 'admin'
password = '88888888'
db_name = 'souschef3'


def get_connection():
    connection = pymysql.connect(host=host, user=user, password=password, database=db_name, port=port)
    print("Connection OK")
    return connection


def users_app_id(app_id):  # проверка пользователя в таблице users
    connection = get_connection()  # Создаем новую сессию
    cursor = connection.cursor()  # Будем получать информацию от сюда
    sql_select_app_id = "SELECT app_id FROM users WHERE app_id = %s"  # делаем запрос
    cursor.execute(sql_select_app_id, (app_id))  # получаем запрашиваемые данные
    user = cursor.fetchone()  # записываем id в user
    user_status=0

    if user is not None:   # если id есть в бд
        old_user = user[0]  # создаем переменную old_user
        print('old friend id=', old_user)
        fav_adds = user_fav_adds(old_user)  # получаем адреса пользователя
        user_status =  "старый"
        return fav_adds

    if user is None:  # если user новый
        new_user = app_id  # создаем переменную new_user и присваеваем ей пришедший id
        print("new user: id=", new_user)
        sql_insert_new_user = "INSERT INTO users (app_id) VALUES (%s)"  # добавляем app_id в таблицу users
        cursor.execute(sql_insert_new_user, (new_user))
        sql_insert_user_id = "INSERT INTO users_adds (user_id) SELECT user_id FROM users WHERE app_id = %s"  # добавляем user_id в таблицу user_adds
        cursor.execute(sql_insert_user_id, (new_user))
        connection.commit()
        return 0
        # если user новый то возвращаем 0
    connection.close()
    print("status user", user_status)


def user_fav_adds(old_user_id):  # функция для получения адресов пользователя
    connection = get_connection()  # Создаем новую сессию
    cursor = connection.cursor()  # Будем получать информацию от сюда
    sql_select_fav_user_adds = """SELECT address
                                  FROM users_adds
                                  INNER JOIN users on users_adds.user_id = users.user_id
                                  WHERE users.app_id = %s"""  # делаем запрос на вывод адресов old_user
    cursor.execute(sql_select_fav_user_adds, (old_user_id))  # получаем список адресов
    fav_adds = cursor.fetchall()  # добавляем адреса в переменную fav_adds
    return fav_adds


def adds_check(address, old_user_id):
    connection = get_connection()  # Создаем новую сессию
    cursor = connection.cursor()  # Будем получать информацию от сюда
    sql_select_check_adds = """SELECT address
                                      FROM users_adds
                                      INNER JOIN users on users_adds.user_id = users.user_id
                                      WHERE users.app_id = %s"""  # делаем запрос на вывод адресов old_user
    cursor.execute(sql_select_check_adds, (old_user_id))  # получаем список адресов
    check_adds = cursor.fetchall()  # добавляем адреса в переменную fav_adds
    connection.close()

    print(check_adds)
    for add in check_adds:  # достаем элементы кортежа check_add
        print(add[0])
        if address == add[0]:  # если элемент кортежа совпадает с address
            print('Адрес есть в БД')
            return 1  # возвращаем 1
        else:
            print('Адрес не совпадает')
            #return 0  # если элемент кортежа не совпадает с address возвращаем 0


def adds_update(address, old_user_id):
    connection = get_connection()  # Создаем новую сессию
    cursor = connection.cursor()  # Будем получать информацию от сюда
    sql_select_user_id = """SELECT user_id
                                       FROM users
                                       WHERE users.app_id = %s"""  # делаем запрос на вывод адресов old_user
    cursor.execute(sql_select_user_id, (old_user_id))
    user_id = cursor.fetchone()
    sql_insert_adds_update = """INSERT INTO users_adds (address, user_id) 
                                       VALUES (%s, %s)"""  # делаем запрос на вывод адресов old_user
    cursor.execute(sql_insert_adds_update, (address, user_id))  # получаем список адресов
    connection.commit()
    connection.close()
   # fav_adds = cursor.fetchall()  # добавляем адреса в пере

#def main():
    #users_app_id(183284977)
    #adds_check('Центр', 183284977)
 #   adds_update("Ломоносово", 183284977)


"""def users_app_id():
    with con:
        cur = con.cursor()
        cur.execute("SELECT app_id FROM users")
        app_id=cur.fetchall()
        print(app_id)"""


#if __name__=='__main__':
 #   main()
