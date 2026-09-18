import db_connection

db_con = db_connection.db_con
cursor = db_con.cursor()

rack_data = [
    (1, "Rak A-01 (Elektronik Utama)"),
    (2, "Rak A-02 (Aksesoris Komputer)"),
    (3, "Rak B-01 (Alat Tulis & Kantor)"),
    (4, "Rak B-02 (Peralatan Kemas)"),
    (5, "Rak C-01 (Sparepart & Komponen)")
]

category_data = [
    (1, "Komputer & Laptop"),
    (2, "Periferal & Aksesoris"),
    (3, "Alat Tulis Kantor"),
    (4, "Perlengkapan Packing"),
    (5, "Komponen Elektronik")
]

item_data = [
    ("Mouse Wireless Logitech M220", 45, 2, 2),
    ("Mechanical Keyboard TKL", 18, 2, 2),
    ("Monitor LED 24 Inch 100Hz", 12, 1, 1),
    ("Kertas HVS A4 75 GSM (Rim)", 50, 3, 3),
    ("Pulpen Gel Hitam 0.5mm (Pak)", 30, 3, 3),
    ("Bubble Wrap Roll 50m", 25, 4, 4),
    ("Lakban Cokelat Fragile 48mm", 60, 4, 4),
    ("RAM DDR4 8GB 3200MHz", 15, 5, 5),
    ("SSD NVMe 512GB PCIe 4.0", 22, 5, 5),
    ("Kabel HDMI to HDMI 2 Meter", 40, 2, 2)
]

try:
    rack_query = "INSERT IGNORE INTO rack (id, name) VALUES (%s, %s)"
    cursor.executemany(rack_query, rack_data)

    category_query = "INSERT IGNORE INTO categories (id, name) VALUES (%s, %s)"
    cursor.executemany(category_query, category_data)

    item_query = """
        INSERT INTO items (name, stock, rack_id, category_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(item_query, item_data)

    print("Seeding berhasil disimpan!")

except Exception as err:
    db_con.rollback()
    print(f"Terjadi error saat seeding: {err}")

finally:
    cursor.close()
    db_con.close()