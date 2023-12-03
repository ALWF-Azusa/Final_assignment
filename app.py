# app.py

from lib import (
    add_record,
    authenticate,
    create_database,
    delete_all_records,
    display_records,
    import_data,
    modify_record,
    nochoice,
    query_phone,
    read_pass_file,
)


def main():
    pass_data = read_pass_file()
    username = input("請輸入帳號：")
    password = input("請輸入密碼：")

    if not authenticate(username, password, pass_data):
        print("=>帳密錯誤，程式結束")
        return

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

    while True:
        choice = input("請輸入您的選擇 [0-7]: ").strip()

        if choice == '0':
            break
        elif not choice:
            break
        elif choice == '1':
            create_database()
        elif choice == '2':
            import_data()
        elif choice == '3':
            display_records()
        elif choice == '4':
            add_record()
        elif choice == '5':
            modify_record()
        elif choice == '6':
            query_phone()
        elif choice == '7':
            delete_all_records()
        else:
            print("=>無效的選擇")
            nochoice()


if __name__ == "__main__":
    main()
