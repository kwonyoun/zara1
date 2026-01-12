import pymysql
from zara import crawl_zara_texts 
from dotenv import load_dotenv
import os


# 🔹 ENV 로드
load_dotenv()

# 🔹 DB 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4"
}

conn = pymysql.connect(**DB_CONFIG)
print("DB 연결 성공")
conn.close()


def insert_products(items):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
        INSERT INTO zara_products (name, price, price_text)
        VALUES (%s, %s, %s)
    """

    count = 0
    for item in items:
        cursor.execute(sql, (
            item["name"],
            item["price"],
            item["price_text"]
        ))
        count += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"[DB] INSERT 완료: {count}건")


def main():
    items = crawl_zara_texts()
    insert_products(items)


if __name__ == "__main__":
    main()
