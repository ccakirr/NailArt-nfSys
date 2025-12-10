import sqlite3
import os

# Database dosyasının yolu
DB_PATH = os.path.join(os.path.dirname(__file__), "nailart.db")


def get_connection():
    """Veritabanı bağlantısını döndürür."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Sonuçları dict gibi kullanabilmek için
    return conn


def init_database():
    """Veritabanı tablolarını oluşturur."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            off_day TEXT,
            earnings REAL DEFAULT 0.0
        )
    """)
    
    # Reservations tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_mail TEXT NOT NULL,
            day TEXT NOT NULL,
            hour TEXT NOT NULL,
            service TEXT NOT NULL,
            artist TEXT,
            UNIQUE(customer_mail, day, hour)
        )
    """)
    
    # Services tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Varsayılan servisleri ekle
    _init_default_services()
    # Varsayılan admin kullanıcısını ekle
    _init_default_admin()


def _init_default_services():
    """Varsayılan servisleri ekler."""
    default_services = ["Classic Manicure", "Gel Polish", "Nail Art Design", "Pedicure"]
    conn = get_connection()
    cursor = conn.cursor()
    
    for service in default_services:
        try:
            cursor.execute("INSERT INTO services (name) VALUES (?)", (service,))
        except sqlite3.IntegrityError:
            # Servis zaten varsa atla
            pass
    
    conn.commit()
    conn.close()


def _init_default_admin():
    """Varsayılan admin kullanıcısını ekler."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Admin zaten var mı kontrol et
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (user_type, username, password, name, surname, email, phone, off_day, earnings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("manager", "admin", "1234", "Elif", "Yılmaz", "manager@nails.com", "05061231234", "Pazar", 0.0))
        conn.commit()
    
    conn.close()


# İlk çalıştırmada veritabanını oluştur
if not os.path.exists(DB_PATH):
    init_database()
