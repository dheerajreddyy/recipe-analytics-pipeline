import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

os.makedirs("data/raw", exist_ok=True)

def export_collection(collection_name):
    docs = db.collection(collection_name).stream()
    data = [doc.to_dict() for doc in docs]

    out_path = f"data/raw/{collection_name}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Exported {collection_name} → {out_path}")

# Export collections
export_collection("recipes")
export_collection("users")
export_collection("interactions")
