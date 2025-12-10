from database.db_manager import get_connection, init_database


def load_reservations():
    """Veritabanından rezervasyonları oku."""
    init_database()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()
    conn.close()
    
    reservations = []
    for row in rows:
        reservations.append({
            "customer_mail": row['customer_mail'],
            "day": row['day'],
            "hour": row['hour'],
            "service": row['service'],
            "artist": row['artist']
        })
    return reservations


def save_reservations(res_list):
    """Tüm rezervasyon listesini veritabanına yaz (mevcut tüm rezervasyonları siler ve yeniden ekler)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tüm rezervasyonları sil
    cursor.execute("DELETE FROM reservations")
    
    # Yeni rezervasyonları ekle
    for res in res_list:
        cursor.execute("""
            INSERT INTO reservations (customer_mail, day, hour, service, artist)
            VALUES (?, ?, ?, ?, ?)
        """, (res['customer_mail'], res['day'], res['hour'], res['service'], res.get('artist', None)))
    
    conn.commit()
    conn.close()


def add_reservation(data):
    """Yeni randevu ekle."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO reservations (customer_mail, day, hour, service, artist)
        VALUES (?, ?, ?, ?, ?)
    """, (data['customer_mail'], data['day'], data['hour'], data['service'], data.get('artist', None)))
    
    conn.commit()
    conn.close()


def delete_reservation(customer_mail, day, hour):
    """Belirli bir müşterinin belirli randevusunu sil."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM reservations
        WHERE customer_mail = ? AND day = ? AND hour = ?
    """, (customer_mail, day, hour))
    
    conn.commit()
    conn.close()
