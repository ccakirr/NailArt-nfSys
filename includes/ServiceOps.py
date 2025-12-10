from database.db_manager import get_connection, init_database


def load_services():
    init_database()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM services")
    rows = cursor.fetchall()
    conn.close()
    
    return [row['name'] for row in rows]


def save_services(services):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM services")
        
        for service in services:
            cursor.execute("INSERT INTO services (name) VALUES (?)", (service,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Servisler kaydedilemedi: {e}")
        return False
    finally:
        conn.close()


def add_service(name):
    services = load_services()
    if name not in services:
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO services (name) VALUES (?)", (name,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Servis eklenemedi: {e}")
            return False
        finally:
            conn.close()
    return False


def delete_service(name):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM services WHERE name = ?", (name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Servis silinemedi: {e}")
        return False
    finally:
        conn.close()
