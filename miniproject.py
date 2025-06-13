import sqlite3
from datetime import datetime
try:
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name VARCHAR NOT NULL,
               password VARCHAR NOT NULL,
               status BOOLEAN)''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menuitems(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name VARCHAR NOT NULL,
               category VARCHAR NOT NULL,
               description TEXT NOT NULL,
               price FLOAT NOT NULL,
               FOREIGN KEY (category) REFERENCES category(name))''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category(
               name VARCHAR PRIMARY KEY,
               description TEXT NOT NULL)''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               menu_id INTEGER NOT NULL,
               customer_name VARCHAR NOT NULL,
               user_id INTEGER NOT NULL,
               status TEXT NOT NULL,
               order_date DATE NOT NULL,
               FOREIGN KEY (menu_id) REFERENCES menuitems(id),
               FOREIGN KEY (user_id) REFERENCES users(id))''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount FLOAT NOT NULL,
            payment_method TEXT NOT NULL,
            payment_date DATE NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id))''')

    
    conn.commit()
except Exception as e:
    print("Error during database setup:", e)
conn.close()


def register():
    try:
        username = input("enter your username: ")
        password = input("enter your password: ")

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users(name,password,status)values(?,?,?)
                   ''',(username,password,False))
        user_id = cursor.lastrowid

        if user_id == 1:
            cursor.execute('''UPDATE  users SET status = ? WHERE id = ?''', (True, user_id))
    
        print('user registered successfully....')
        conn.commit()
    except Exception as e:
        print("Registration failed:", e)
    conn.close()

def login():
    try:
        username = input("enter your username: ")
        password = input("enter your  password: ")

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM users WHERE name=? AND password =? ''',(username,password))
        user = cursor.fetchone()
        if user:
            if user[3]==1:
                print("\nwelcome admin....")
                admin()
            else:
                print("\nwelcome Customer..")
                customer(user[0])
        else:
            print("login failed invalid credentials.....")

        conn.commit()
    except Exception as e:
        print("Login failed due to an error:", e)
    conn.close()
def Add():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        while True:
            print("\n1.Add Category..")
            print("2.Add Menu Items..")
            print("3.Exit")
            select = int(input("Enter the choice... "))

            if select == 1:
                name = input("Category name... ") 
                desc = input("Description.. ")               
                    
                cursor.execute('''
                    INSERT INTO category (name,description)values(?,?)''',(name,desc))
                print("Category inserted successfully...")
                
            elif select == 2:
                menu_name = input("Menu name.. ")
                menu_desc = input("Description ... ")
                price = float(input("Price of the menu.. "))
                    
                cursor.execute('''SELECT * FROM category''')
                categ = cursor.fetchall()
                print("\nAvailable categories:")
                for category in categ:
                    print(category[0])
                choose = input("enter the category name.. ")
                cursor.execute('''INSERT INTO menuitems (name,description,price,category)VALUES(?,?,?,?)''',
                                   (menu_name,menu_desc,price,choose))
                print("Menu items inserted successfully..")
            elif select == 3:
                break   
            else:
                print("Invalid option")
            conn.commit()
    except Exception as e:
        print("error in add function..",e)
    conn.close()
            
def view():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        while True:
            print("\n")
            print("1.View users..")
            print("2.View category.")
            print("3.view menu items")
            print("4.View orders")
            print("5.Exit")
            cho = int(input("Enter the choice... "))
            if cho == 1:
                cursor.execute('''SELECT * FROM users''')
                user=cursor.fetchall()
                    
                for rows in user:
                    print(f"ID: {rows[0]}, Name: {rows[1]}")
            elif cho == 2:
                cursor.execute('''SELECT * FROM category''')
                categ = cursor.fetchall()
                for rows in categ:
                    print(f"Category: {rows[0]}, Description: {rows[1]}")
            elif cho == 3:
                cursor.execute('''SELECT * FROM menuitems''')
                menus = cursor.fetchall()
                for item in menus:
                    print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Description: {item[3]}, Price: {item[4]}")
            elif cho == 4:
                cursor.execute('''SELECT * FROM orders''')
                order=cursor.fetchall()
                for rows in order:
                    print(f"Order ID: {rows[0]}, Menu ID: {rows[1]}, Customer: {rows[2]}, Status: {rows[4]}, Date: {rows[5]}")
            elif cho == 5:
                break
            else:
                print("Invalid option")
            conn.commit()
    except Exception as e:
        print("error occured...",e)
    conn.close()

def update():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        while True:
            print("\n1.update category")
            print("2.Update menu items")
            print("3.Update Orders")
            print("4.exit")
            select = int(input("Enter the choice.. "))

            if select == 1:
                cat_name=input("enter the name:: ")
                cat_desc=input("enter the description:: ")
                cursor.execute('''SELECT * FROM category WHERE name=?''',(cat_name,))
                if cursor.fetchone():
                    cursor.execute('''UPDATE category SET  description=? WHERE name=? ''',(cat_desc,cat_name))
                    print("category Updated")
                else:
                    print("category name not found..")
            elif select == 2:
                id = int(input("Enter the menu id: "))
                menu_name = input("Enter menu name: ")
                menu_desc =input("enter the menu description: ")
                price = input("enter the new price: ")
                cursor.execute('''SELECT * FROM menuitems WHERE id=?''',(id,))
                if cursor.fetchone():
                    cursor.execute('''UPDATE menuitems SET name=?, description=?,price=? WHERE id=?''',
                                       (menu_name,menu_desc,price,id))
                    print("Menu Item Updated")
                else:
                    print("menu id not found")
            elif select == 3:
                
                cursor.execute('''SELECT * FROM orders WHERE status='paid' ''')
                view_orders=cursor.fetchall()
                for rows in view_orders:
                    print(f'ORDER ID: {rows[0]}, CUSTOMER NAME: {rows[2]}, STATUS: {rows[4]}, DATE: {rows[5]}')
                id = int(input("Enter the Order Id: "))
                order_status =input("Enter the status completed/not: ")
                cursor.execute('''SELECT * FROM orders WHERE id=? AND status='paid' ''',(id,))
                if cursor.fetchone():
                    cursor.execute('''UPDATE orders SET status=? WHERE id=?''',(order_status,id))
                    print("Order status updated..")
                else:
                    print("order Id not found")  

            elif select ==4:
                break
            else:
                print("Invalid option")
            conn.commit()
    except Exception as e:
        print("error occured..",e)
    conn.close()

def delete():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        while True:
            print("1.Delete user")
            print("2.Delete category")
            print("3.Delete Menu")
            print("4.Delete order")
            print("5.exit")
            opt = int(input("Enter the option... "))

            if opt == 1:
                id = int(input("user id::  "))
                cursor.execute('''SELECT * FROM users WHERE id=?''',(id,))
                
                if cursor.fetchone():
                    cursor.execute('''DELETE FROM users WHERE id =?''',(id,))
                    print("user deleted")
                else:
                    print("User not found..")
            elif opt == 2:
                name = input("Category Name:  ")
                cursor.execute(''' SELECT * FROM category WHERE name = ?''',(name,))
                
                if cursor.fetchone():
                    cursor.execute('''DELETE FROM category WHERE name =?''',(name,))
                    print("category deleted..")
                else:
                    print("Category name not found..")
            elif opt == 3:
                id = int(input(" Menu Id::  "))
                cursor.execute('''SELECT * FROM menuitems WHERE id =?''',(id,))

                if cursor.fetchone():
                    cursor.execute('''DELETE FROM menuitems WHERE id =?''',(id,))
                    print("menu deleted..")
                else:
                    print("Menu id not found..")
            elif opt == 4:
                id = int(input("Order Id:  "))
                cursor.execute('''SELECT * FROM orders WHERE id =?''',(id,))
                if cursor.fetchone():
                    cursor.execute('''DELETE FROM orders WHERE id =?''',(id,))
                    print("order deleted")
                else:
                    print("order id not found..")
            elif opt == 5:
                break
            
            conn.commit()
    except Exception as e:
        print("error occured",e)
    conn.close()

def admin():
    while True:
        try:
            print("\n Admin Panel...")
            print("1.Add")
            print("2.View")
            print("3.Update")
            print("4.Delete")
            print("5.Exit")
            choice = int(input("Enter your choice...."))
         
            if choice == 1:
                Add()
                
            elif choice ==2:
                view()
            elif choice == 3:
                update()
                
            elif choice == 4:
                delete()
            elif choice == 5:
                break
            else:
                print("Invalid option")
        except Exception as e:
            print("error occured in admin's page..", e)


def customer(user_id):
    while True:
        try:
            print("\n--- Customer Menu ---")
            print("1. View Menu Items")
            print("2. Place an Order")
            print("3. View My Orders")
            print("4. delete order")
            print("5. Make payment")
            print("6. Exit")
            choice = input("Enter your choice: ")

            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()

            if choice == '1':
                cursor.execute('SELECT * FROM menuitems')
                items = cursor.fetchall()
                print("\nAvailable Menu Items:")
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Description: {item[3]}, Price: {item[4]}")
            
            elif choice == '2':
                customer_name = input("Enter your name: ")
                cursor.execute('SELECT * FROM menuitems')
                items = cursor.fetchall()
                print("\nAvailable Menu Items:")
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[4]}")
                
                menu_id = int(input("Enter the Menu ID to order: "))
                order_status = "pending"
                order_date = datetime.now().strftime('%Y-%m-%d')

                cursor.execute('''
                    INSERT INTO orders(menu_id, customer_name, user_id, status, order_date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (menu_id, customer_name, user_id, order_status, order_date))
                print("Order placed successfully!")

            elif choice == '3':
                cursor.execute('SELECT * FROM orders WHERE user_id=?', (user_id,))
                orders = cursor.fetchall()
                print("\nYour Orders:")
                for order in orders:
                    print(f"Order ID: {order[0]}, Menu ID: {order[1]}, Name: {order[2]}, Status: {order[4]}, Date: {order[5]}")

            elif choice == '4':
                cursor.execute('SELECT * FROM orders WHERE user_id=?', (user_id,))
                orders = cursor.fetchall()
                print("\nYour Orders:")
                for order in orders:
                    print(f"Order ID: {order[0]}, Menu ID: {order[1]}, Name: {order[2]}, Status: {order[4]}, Date: {order[5]}")
                order_id = int(input("order id.. "))
                if cursor.fetchone():
                    cursor.execute('''DELETE FROM orders WHERE id=?''',(order_id,))
                    print("your order deleted..")
            elif choice == '5':
                make_payment(user_id)

            elif choice == '6':
                break
            else:
                print("Invalid choice. Try again.")

            conn.commit()
        except Exception as e:
            print("Error in customer section:", e)
        conn.close()
def pass_reset():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        id = int(input("id: "))
        username=input("username: ")
        new_password = input("New password: ")
        cursor.execute('''
                    UPDATE users SET password=? where id=? AND name=?''',(new_password,id,username))
        print("password reset successfully..")
        conn.commit()
    except Exception as e:
        print("error occured in password reset..")
    conn.close()

def make_payment(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT o.id, o.menu_id, m.name, m.price, o.status
            FROM orders o
            JOIN menuitems m ON o.menu_id = m.id
            WHERE o.user_id = ? AND o.status = 'pending'
        ''', (user_id,))
        orders = cursor.fetchall()

        if not orders:
            print("No pending orders found.")
            conn.close()
            return

        print("\nPending Orders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Menu: {order[2]}, Price: {order[3]}")

        order_id = int(input("Enter the Order ID to pay for: "))
        payment_method = input("Enter payment method (e.g., card, cash, online): ")
        payment_date = datetime.now().strftime('%Y-%m-%d')


        selected_order = next((order for order in orders if order[0] == order_id), None)
        if not selected_order:
            print("Invalid Order ID.")
            return
        amount = selected_order[3]

        cursor.execute('''
            INSERT INTO payment(order_id, amount, payment_method, payment_date)
            VALUES (?, ?, ?, ?)
        ''', (order_id, amount, payment_method, payment_date))

        cursor.execute('''
            UPDATE orders SET status = 'paid' WHERE id = ?
        ''', (order_id,))

        print("Payment successful!")

        conn.commit()
    except Exception as e:
        print("Error occurred during payment:", e)
    finally:
        conn.close()


def main():
    while True:
        try:
            print("welcome to meenu's kitchen....")
            print("\n")
            print("1. Register new user")
            print("2. Login")
            print("3. password reset")
            print("4. Exit")
            choice = input("enter your choice: ")
            if choice == '1':
                register()
            elif choice == '2':
                login()
            elif choice == '3':
                pass_reset()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print("An error occurred in the main menu:", e)

main()