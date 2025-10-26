from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
	name:str
	price:float
	brand: Optional[str] = None

class UpdateItem(BaseModel):
	name: Optional[str] = None
	price: Optional[float] = None
	brand: Optional[str] = None


@app.get("/")
def home():
	return {"data": "Testing"}


@app.get("/about/")
def about():
	return {"data": "About"}


inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The Id of the Item you would like to view.", gt=0, lt=10)):
	if item_id not in inventory:
		# return {"data": "Not found"}
		raise HTTPException(status_code=404, detail="Item Id not found.")

	return inventory[item_id]


@app.get("/get-by-name/")
def get_by_name(*, name: Optional[str] = None, test: int):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]
	# return {"data": "Not found"}
	raise HTTPException(status_code=404, detail="Item name not found.")

@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
	if item_id in inventory:
		# return {"error": "Item Id already exists."}
		raise HTTPException(status_code=400, detail="Item Id already exists.")

	# inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
	inventory[item_id] = item
	return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
	if item_id not in inventory:
		# return {"error": "Item Id does not exist."}
		raise HTTPException(status_code=404, detail="Item Id does not exist.")

	if item.name != None:
		inventory[item_id].name = item.name

	if item.price != None:
		inventory[item_id].price = item.price

	if item.brand != None:
		inventory[item_id].brand = item.brand

	return inventory[item_id]


@app.delete("/delete-item/")
def delete_item(item_id: int = Query(..., description="The Id of the Item to delete.", gt=0)):
	if item_id not in inventory:
		# return {"error": "Item Id does not exist."}
		raise HTTPException(status_code=404, detail="Item Id does not exist.")

	del inventory[item_id]
	return {"success": "Item deleted!"}

# uvicorn working:app --reload