# import psycopg

# url = "postgresql://edunexia_user:123456@127.0.0.1:5432/edunexia_dev"

#try:
#    with psycopg.connect(url) as conn:
#        print("✅ PostgreSQL connected")
# except Exception as e:
#    print("❌ Connection error:", e)

import psycopg2

try:
    conn = psycopg2.connect(
        dbname="edunexia_dev",
        user="edunexia_user",
        password="123456",
        host="127.0.0.1",
        port=5432
    )

    print("✅ Kết nối PostgreSQL THÀNH CÔNG")

    conn.close()
    print("🔌 Đã đóng kết nối")

except psycopg2.OperationalError as e:
    print("❌ Kết nối PostgreSQL THẤT BẠI")
    print("Lỗi:", e)

except Exception as e:
    print("❌ Lỗi khác")
    print("Chi tiết:", e)
