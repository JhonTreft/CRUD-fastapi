from fastapi import APIRouter
from schemas.product import Product
from redis_client.crud import delete_hash, get_hash, save_hash, save_multiple_products

routes_product = APIRouter()

fake_db = [{
  "id": "93c38f5e-d75d-415d-8ebb-60521881c320",
  "name": "treft",
  "price": 10,
  "date": "2023-09-02 14:18:41.333164"
},
        {
  "id": "188d7634-bb7d-45c4-9e80-1620099ded61",
  "name": "brutus",
  "price": 8,
  "date": "2023-09-02 15:21:27.921153"
}
           ]

@routes_product.post("/create", response_model=Product)
async def create(product: Product):
    try:
        fake_db.append(product.model_dump())
        
        save_hash(key=product.model_dump()["id"], data=product.model_dump())
        
        return product
    except Exception as e:
        return {"error": str(e)}

@routes_product.get("/product/{id}")
def get_product_by_id(id:str):
    try:
        data = get_hash(key=id)
        
        if(len(data) == 0):
            product = list(filter(lambda field: field["id"] == id,fake_db))[0]
            
            save_hash(key=id, data=product)
            
            return product
        
        
        return data
    except Exception as e:
        return {"error": str(e)}
    
@routes_product.delete("/product/{id}")
def get_product_delete(id:str):
    try:
        keys=Product.__fields__.keys()
        
        delete_hash(key=id,keys=keys)
        
        product = list(filter(lambda field: field["id"] == id,fake_db))

        if len(product) != 0 :
            fake_db.remove(product)
        return {
            "messages":"success"
        }    
    
    except Exception as e:
        return {"error": str(e)}
    

@routes_product.get("/products/")
def get_all_products():
    try:
        products = get_hash("all_products")

        # Si los productos no están en Redis, guárdalos y luego obténlos de fake_db
        if not products:
            save_multiple_products(fake_db)
            products = fake_db

        return products
        
    except Exception as e:
        return {"error": str(e)}
