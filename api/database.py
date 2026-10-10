import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

databaseUrl = os.environ["DATABASE_URL"]

def addProduct(barcode: str, description: str, isHalal: bool):
    with psycopg2.connect(databaseUrl) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO products (barcode, description, "isHalal")
                VALUES (%s, %s, %s)
                RETURNING barcode;
                """,
                (barcode, description, isHalal)
            )

def getDBProduct(barcode: str):
    with psycopg2.connect(databaseUrl) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT barcode, description, "isHalal"
                FROM products
                WHERE barcode = %s;
                """,
                (barcode,)
            )

            row = cur.fetchone()

            if row is None:
                return None

            return {
                "barcode": row[0],
                "description": row[1],
                "isHalal": row[2]
            }
