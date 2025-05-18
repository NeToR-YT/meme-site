from fastapi import APIRouter, HTTPException
from backend.database import get_db
from backend.models import Category, Meme
from datetime import datetime

router = APIRouter()

# GET: Список усіх категорій
@router.get("/categories", response_model=list[Category])
async def get_categories():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = [{"id": row["id"], "name": row["name"]} for row in cursor.fetchall()]
    return categories

# GET: Список мемів (з опціональною фільтрацією за категорією та сортуванням)
@router.get("/memes", response_model=list[Meme])
async def get_memes(category_id: int = None, sort_by: str = "created_at"):
    query = "SELECT id, title, image_url, category_id, created_at FROM memes"
    params = []
    if category_id:
        query += " WHERE category_id = ?"
        params.append(category_id)
    if sort_by == "created_at":
        query += " ORDER BY created_at DESC"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        memes = [
            {
                "id": row["id"],
                "title": row["title"],
                "image_url": row["image_url"],
                "category_id": row["category_id"],
                "created_at": row["created_at"]
            }
            for row in cursor.fetchall()
        ]
    return memes

# GET: Отримати мем за ID
@router.get("/memes/{meme_id}", response_model=Meme)
async def get_meme(meme_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, image_url, category_id, created_at FROM memes WHERE id = ?",
            (meme_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Meme not found")
        return {
            "id": row["id"],
            "title": row["title"],
            "image_url": row["image_url"],
            "category_id": row["category_id"],
            "created_at": row["created_at"]
        }

# POST: Додати новий мем
@router.post("/memes", response_model=Meme)
async def create_meme(meme: Meme):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO memes (title, image_url, category_id, created_at) VALUES (?, ?, ?, ?)",
            (meme.title, meme.image_url, meme.category_id, datetime.now())
        )
        conn.commit()
        meme_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, title, image_url, category_id, created_at FROM memes WHERE id = ?",
            (meme_id,)
        )
        row = cursor.fetchone()
        return {
            "id": row["id"],
            "title": row["title"],
            "image_url": row["image_url"],
            "category_id": row["category_id"],
            "created_at": row["created_at"]
        }

# DELETE: Видалити мем за ID
@router.delete("/memes/{meme_id}")
async def delete_meme(meme_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM memes WHERE id = ?", (meme_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Meme not found")
        cursor.execute("DELETE FROM memes WHERE id = ?", (meme_id,))
        conn.commit()
    return {"message": f"Meme {meme_id} deleted"}