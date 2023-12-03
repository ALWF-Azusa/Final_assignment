# lib.py

import json
import sqlite3


def display_menu():
    """顯示主選單"""
    print("\n---------- 選單 ----------")
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")
    print("--------------------------")


def read_pass_file():
    """讀取 pass.json 檔案"""
    try:
        with open('pass.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("找不到 pass.json 檔案")
        return []


def authenticate(username, password, pass_data):
    """驗證帳號密碼是否正確"""
    for user in pass_data:
        if user['帳號'] == username and user['密碼'] == password:
            return True
    return False


def create_database():
    """建立 sqlite3 資料庫及資料表"""
    try:
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS members (
                    iid INTEGER PRIMARY KEY AUTOINCREMENT,
                    mname TEXT NOT NULL,
                    mgender TEXT NOT NULL,
                    mphone TEXT NOT NULL
                )
            '''
            )
        print("=>資料庫已建立")
    except sqlite3.Error as e:
        print(f"資料庫建立失敗: {e}")
    display_menu()


def import_data():
    """匯入資料"""
    try:
        with open('members.txt', 'r', encoding='utf-8') as f:
            data = [line.strip().split(',') for line in f]
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()
            cursor.executemany(
                'INSERT INTO members (mname, mgender, mphone) VALUES (?, ?, ?)', data
            )
        print(f"=>異動 {len(data)} 筆記錄")
    except FileNotFoundError:
        print("找不到 members.txt 檔案")
    display_menu()


def display_records():
    """顯示所有紀錄"""
    try:
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()

            # 檢查資料表是否存在
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='members'")
            table_exists = cursor.fetchone()

            if table_exists:
                cursor.execute('SELECT * FROM members')
                data = cursor.fetchall()
                if not data:
                    print("=>查無資料")
                else:
                    # 計算每個欄位的最大長度
                    max_name = max(len(row[1]) for row in data)
                    max_gender = max(len(row[2]) for row in data)
                    max_phone = max(len(row[3]) for row in data)

                    # 調整最大長度，確保每個欄位的長度一致
                    max_length = max(max_name, max_gender, max_phone)

                    print(
                        "{:<{}} {:<{}} {:<{}}".format(
                            "姓名", (max_length - 2), "性別", (max_length - 8), "手機", (max_length - 2)
                        )
                    )
                    print("-" * (max_length * 3 - 4))

                    for row in data:
                        name = row[1]
                        gender = row[2]
                        phone = row[3]

                        # 對齊資料
                        print(
                            "{:<{}} {:<{}} {:<{}}".format(
                                name,
                                (max_length - len(name) + 1),
                                gender,
                                (max_length - len(gender) - 6),
                                phone,
                                (max_length - len(phone)),
                            )
                        )
            else:
                print("=>查無資料表")

        display_menu()  # 顯示資料後再顯示菜單

    except sqlite3.Error as e:
        print(f"資料庫操作失敗: {e}")


def add_record():
    """新增記錄"""
    try:
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS members (iid INTEGER PRIMARY KEY AUTOINCREMENT, mname TEXT NOT NULL, mgender TEXT NOT NULL, mphone TEXT NOT NULL);'
            )

            name = input("請輸入姓名: ")
            sex = input("請輸入性別: ")
            phone = input("請輸入手機: ")

            cursor.execute(
                'INSERT INTO members (mname, mgender, mphone) VALUES (?, ?, ?)', (name, sex, phone)
            )
            conn.commit()

            print(f"=>異動 1 筆記錄\n")

    except sqlite3.Error as e:
        print(f"資料庫操作失敗: {e}")

    display_menu()  # Display the menu after adding record


def modify_record():
    """修改記錄"""
    name_to_modify = input("請輸入想修改記錄的姓名: ")
    try:
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM members WHERE mname=?', (name_to_modify,))
            data = cursor.fetchone()
        if not data:
            print("=>必須指定姓名才可修改記錄")
        else:
            sex_to_change = input("請輸入要改變的性別: ")
            phone_to_change = input("請輸入要改變的手機: ")
            print("\n原資料：")
            print(f"姓名：{data[1]}，性別：{data[2]}，手機：{data[3]}")
            with sqlite3.connect('wanghong.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE members SET mgender=?, mphone=? WHERE mname=?',
                    (sex_to_change, phone_to_change, name_to_modify),
                )
            print("=>異動 1 筆記錄")
            print("修改後資料：")
            print(f"姓名：{name_to_modify}，性別：{sex_to_change}，手機：{phone_to_change}")
    except sqlite3.Error as e:
        print(f"資料庫操作失敗: {e}")

    display_menu()  # Display the menu after modifying record


def query_phone():
    """查詢指定手機"""
    phone_to_query = input("請輸入想查詢記錄的手機: ")
    try:
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM members WHERE mphone=?', (phone_to_query,))
            data = cursor.fetchall()
        if not data:
            print("=>查無資料")
        else:
            # 計算每個欄位的最大長度
            max_name = max(len(row[1]) for row in data)
            max_gender = max(len(row[2]) for row in data)
            max_phone = max(len(row[3]) for row in data)

            # 調整最大長度，確保每個欄位的長度一致
            max_length = max(max_name, max_gender, max_phone)

            print(
                "{:<{}} {:<{}} {:<{}}".format(
                    "姓名", (max_length - 2), "性別", (max_length - 8), "手機", (max_length - 2)
                )
            )
            print("-" * (max_length * 3 - 4))

            for row in data:
                name = row[1]
                gender = row[2]
                phone = row[3]

                # 對齊資料
                print(
                    "{:<{}} {:<{}} {:<{}}".format(
                        name,
                        (max_length - len(name) + 1),
                        gender,
                        (max_length - len(gender) - 6),
                        phone,
                        (max_length - len(phone)),
                    )
                )
    except sqlite3.Error as e:
        print(f"資料庫操作失敗: {e}")

    display_menu()  # Display the menu after querying phone


def delete_all_records():
    """刪除所有記錄"""
    try:
        with sqlite3.connect('wanghong.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM members')
            num_deleted = cursor.rowcount
        print(f"=>異動 {num_deleted} 筆記錄")
    except sqlite3.Error as e:
        print(f"資料庫操作失敗: {e}")
    display_menu()


def nochoice():
    display_menu()
