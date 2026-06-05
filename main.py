import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 1. Standard Setup
cred = credentials.Certificate("firebase_key.json") # Ensure this file is never uploaded to the public web!
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

print("Connection successful. Initiating secure factory production run...")

# 2. The Production Function
def log_production_run():
    # Setup document references
    jumbo_roll_ref = db.collection('raw_materials').document('RM-JUMBO-001')
    retail_pack_ref = db.collection('finished_goods').document('FG-9PACK-001')
    audit_log_ref = db.collection('production_logs').document() # Generates a random ID for the ledger entry

    # CRITICAL FIX: Initialize an atomic batch
    batch = db.batch()
    
    # Action A: Deduct 50kg from the Jumbo Roll
    batch.update(jumbo_roll_ref, {
        "current_stock_kg": firestore.Increment(-50)
    })
    
    # Action B: Create the retail packs and add 100 units to the shop inventory
    # FIX: Matched retail price to the $3.00 advertised on the public website
    batch.set(retail_pack_ref, {
        "item_name": "Pink Petals 2-Ply (9-Roll Pack)",
        "sku": "PP-2P-09",
        "current_stock_units": firestore.Increment(100),
        "retail_price_usd": 3.00, 
        "wholesale_price_usd": 2.50
    }, merge=True)

    # Action C: Write to the Audit Ledger so the MIS Dashboard registers the profit
    batch.set(audit_log_ref, {
        "product_sku": "9-pack",
        "units_added": 100,
        "logged_by": "python_automation_script",
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    
    # Commit the batch (Executes all actions perfectly simultaneously)
    batch.commit()
    
    print("Success! Batch committed. 50kg deducted, 100 packs added, and ledger updated.")

# 3. Run the function
log_production_run()