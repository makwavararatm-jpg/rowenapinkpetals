import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 1. Standard Setup
cred = credentials.Certificate("firebase_key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

print("Connection successful. Initiating factory production run...")

# 2. The Production Function
def log_production_run():
    # We point to the exact items in our database
    jumbo_roll_ref = db.collection('raw_materials').document('RM-JUMBO-001')
    retail_pack_ref = db.collection('finished_goods').document('FG-9PACK-001')
    
    # Let's pretend the factory just used 50kg of the jumbo roll to make 100 packs of tissues.
    
    # Action A: Deduct 50kg from the Jumbo Roll
    # 'firestore.Increment(-50)' is a smart tool that does the math for us safely in the cloud
    jumbo_roll_ref.update({
        "current_stock_kg": firestore.Increment(-50)
    })
    
    # Action B: Create the retail packs and add 100 units to the shop inventory
    # 'merge=True' means it will create the product if it doesn't exist yet, or just update the stock if it does
    retail_pack_ref.set({
        "item_name": "Pink Petals 2-Ply (9-Roll Pack)",
        "sku": "PP-2P-09",
        "current_stock_units": firestore.Increment(100),
        "retail_price_usd": 4.50,
        "wholesale_price_usd": 3.80
    }, merge=True)
    
    print("Success! 50kg of raw material was converted into 100 retail packs.")

# 3. Run the function
log_production_run()