from includes.ArtistInf import Artist
from includes.CostumerInf import Costumer
from includes.ManagerInf import Manager
from database.db_manager import get_connection, init_database


def load_users():
    """Veritabanından kullanıcıları okuyup kullanıcı nesneleri döner."""
    init_database()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    users = []
    for row in rows:
        user_type = row['user_type']
        username = row['username']
        password = row['password']
        
        if user_type == "manager":
            users.append({
                "type": "manager",
                "username": username,
                "password": password,
                "object": Manager(row['name'], row['surname'], row['email'], row['phone'], row['off_day'])
            })
        elif user_type == "artist":
            users.append({
                "type": "artist",
                "username": username,
                "password": password,
                "object": Artist(row['name'], row['surname'], row['email'], row['phone'], row['off_day'], row['earnings'])
            })
        elif user_type == "customer":
            users.append({
                "type": "customer",
                "username": username,
                "password": password,
                "object": Costumer(row['name'], row['surname'], row['email'], row['phone'])
            })
    return users


def save_user(user_type, username, password, obj):
    """Yeni kullanıcıyı veritabanına yazar."""
    conn = get_connection()
    cursor = conn.cursor()
    
    details = obj.getDetails()
    
    try:
        if user_type == "manager":
            cursor.execute("""
                INSERT INTO users (user_type, username, password, name, surname, email, phone, off_day, earnings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_type, username, password, details['name'], details['surname'],
                  details['mail'], details['phone'], obj.getOffDay(), 0.0))
        elif user_type == "artist":
            cursor.execute("""
                INSERT INTO users (user_type, username, password, name, surname, email, phone, off_day, earnings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_type, username, password, details['name'], details['surname'],
                  details['mail'], details['phone'], details['offDay'], details['earnings']))
        elif user_type == "customer":
            cursor.execute("""
                INSERT INTO users (user_type, username, password, name, surname, email, phone, off_day, earnings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_type, username, password, details['name'], details['surname'],
                  details['mail'], details['phone'], None, 0.0))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Kullanıcı kaydedilemedi: {e}")
        return False
    finally:
        conn.close()


def update_user_earnings(email, new_earnings):
    """Sanatçının kazancını günceller"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users
            SET earnings = ?
            WHERE email = ? AND user_type = 'artist'
        """, (new_earnings, email))
        conn.commit()
        return True
    except Exception as e:
        print(f"Kazanç güncellenemedi: {e}")
        return False
    finally:
        conn.close()
