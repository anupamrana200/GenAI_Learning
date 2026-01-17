import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL)


def fetch_all_patients():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, city, age, gender, height, weight
                FROM patients
            """)
            rows = cur.fetchall()

    patients = {}
    for row in rows:
        patients[row[0]] = {
            "name": row[1],
            "city": row[2],
            "age": row[3],
            "gender": row[4],
            "height": row[5],
            "weight": row[6],
        }

    return patients


def fetch_patient_by_id(patient_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, city, age, gender, height, weight
                FROM patients
                WHERE id = %s
            """, (patient_id,))
            row = cur.fetchone()

    if row is None:
        return None

    return {
        "name": row[1],
        "city": row[2],
        "age": row[3],
        "gender": row[4],
        "height": row[5],
        "weight": row[6],
    }


def insert_patient(patient: dict):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO patients (id, name, city, age, gender, height, weight)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                patient["id"],
                patient["name"],
                patient["city"],
                patient["age"],
                patient["gender"],
                patient["height"],
                patient["weight"],
            ))
        conn.commit()

def update_patient_by_id(patient_id: str, updated_fields: dict):
    if not updated_fields:
        return

    columns = []
    values = []

    for key, value in updated_fields.items():
        columns.append(f"{key} = %s")
        values.append(value)

    values.append(patient_id)

    query = f"""
        UPDATE patients
        SET {', '.join(columns)}
        WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, tuple(values))
        conn.commit()


def delete_patient_by_id(patient_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM patients WHERE id = %s",
                (patient_id,)
            )
        conn.commit()
