from database.db_manager import get_connection, init_database


def load_services():
    """Veritabanından servisleri oku."""
    init_database()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM services")
    rows = cursor.fetchall()
    conn.close()
    
    return [row['name'] for row in rows]


def save_services(services):
    """Tüm servis listesini veritabanına yaz (mevcut tüm servisleri siler ve yeniden ekler)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tüm servisleri sil
    cursor.execute("DELETE FROM services")
    
    # Yeni servisleri ekle
    for service in services:
        cursor.execute("INSERT INTO services (name) VALUES (?)", (service,))
    
    conn.commit()
    conn.close()


def add_service(name):
    """Yeni servis ekle."""
    services = load_services()
    if name not in services:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO services (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()


def delete_service(name):
    """Servisi sil."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE name = ?", (name,))
    conn.commit()
    conn.close()
