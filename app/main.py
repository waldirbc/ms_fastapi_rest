import app.models as models
import app.schema as schema

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import engine, SessionLocal

from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS FastAPI Rest", version="1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/products/", response_model=List[schema.ProductRead])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@app.post("/api/products/", response_model=schema.ProductRead)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        creation_date=datetime.now(),
        category=product.category
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/api/products/{product_id}", response_model=schema.ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/api/products/{product_id}", response_model=schema.ProductRead)
def update_product(product_id: int, product: schema.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name or db_product.name
    db_product.price = product.price if product.price is not None else db_product.price
    db_product.quantity = product.quantity if product.quantity is not None else db_product.quantity
    db_product.category = product.category or db_product.category
    db.commit()
    return db_product


@app.delete("/api/products/{product_id}", response_model=schema.ProductRead)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
