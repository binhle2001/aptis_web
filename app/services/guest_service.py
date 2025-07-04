import math
from fastapi import APIRouter, HTTPException, status
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi.responses import JSONResponse
from services.auth_service import get_db_connection
import psycopg2
from datetime import timedelta


def insert_guest_info(fullname, phone_number):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("Select id FROM guest Where phone_number = %s", (phone_number,))
        row = cur_validate.fetchone()
        if row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Phone number have already existed!")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO guest (fullname, phone_number) VALUES (%s, %s) RETURNING id, fullname, phone_number, created_at", (fullname, phone_number))
        row = cursor.fetchone()
        conn.commit()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data = {
                "sub": "guest", # "sub" is a standard claim for subject (username)
                "id": row["id"],
                "role": "guest",
                "fullname": row["fullname"]
                # Bạn có thể thêm các thông tin khác vào payload của token nếu cần
            }
        access_token = create_access_token(
                data=access_token_data, expires_delta=access_token_expires
            )

        return JSONResponse(status_code=status.HTTP_200_OK, content = {"access_token": access_token, "token_type": "bearer"})
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
    

def call_guest(guest_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("Select * FROM guest Where id = %s", (guest_id,))
        row = cur_validate.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Guest with {guest_id} not exist!")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE guest SET is_called = %s Where id = %s", (True, guest_id))
        conn.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content = {"message": "success"})
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def recall_guest(guest_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("Select * FROM guest Where id = %s", (guest_id,))
        row = cur_validate.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Guest with {guest_id} not exist!")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE guest SET is_called = %s Where id = %s", (False, guest_id))
        conn.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content = {"message": "success"})
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()



def get_list_guest(
    page: int = 1,
    limit: int = 100
    ):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        offset = (page-1) * limit
        cursor.execute("SELECT id, fullname, phone_number, created_at, is_called FROM guest ORDER BY created_at DESC LIMIT %s OFFSET %s;", (limit, offset))
        rows = cursor.fetchall()
        items = []
        count_sql = f"SELECT COUNT(*) AS total FROM guest;"
        cursor.execute(count_sql)
        total = cursor.fetchone()["total"]
        total_pages = math.ceil(total / limit) if limit > 0 else 0
        for row in rows:
            item = dict(row)
            item["created_at"] = item["created_at"].isoformat()
            items.append(item)
        
        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
        }
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def delete_guest(guest_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("Select * FROM guest Where id = %s", (guest_id,))
        row = cur_validate.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Guest with {guest_id} not exist!")
    cursor = conn.cursor()
    try:
        
        cursor.execute("DELETE FROM guest Where id = %s",  (guest_id,))
        conn.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content = {"message": "success"})
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()