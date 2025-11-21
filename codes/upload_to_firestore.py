import firebase_admin
from firebase_admin import credentials, firestore
import random
from datetime import datetime, timedelta
import json

# 1. Initialize Firebase Admin

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


# 2. Primary recipe 

primary_recipe = {
    "id": "recipe_egg_burji_roti",
    "title": "Egg Burji + Roti (South Indian style) for 2",
    "description": "Spicy scrambled eggs served with soft rotis — South Indian home style, no sauces.",
    "servings": 2,
    "prep_time_min": 12,
    "cook_time_min": 10,
    "total_time_min": 22,
    "difficulty": "easy",
    "tags": ["south-indian", "breakfast", "eggs"],
    "created_at": datetime.now(datetime.UTC).isoformat(),
    "ingredients": [
        {"name": "eggs", "quantity": 4, "unit": "pcs"},
        {"name": "onion", "quantity": 1, "unit": "medium"},
        {"name": "tomato", "quantity": 1, "unit": "medium"},
        {"name": "green chili", "quantity": 1, "unit": "pcs"},
        {"name": "curry leaves", "quantity": 6, "unit": "leaves"},
        {"name": "ginger garlic paste", "quantity": 1, "unit": "tsp"},
        {"name": "mustard seeds", "quantity": 0.25, "unit": "tsp"},
        {"name": "turmeric powder", "quantity": 0.25, "unit": "tsp"},
        {"name": "red chili powder", "quantity": 0.5, "unit": "tsp"},
        {"name": "coriander powder", "quantity": 0.5, "unit": "tsp"},
        {"name": "pepper powder (optional)", "quantity": 0.25, "unit": "tsp"},
        {"name": "salt", "quantity": 0.5, "unit": "tsp"},
        {"name": "oil", "quantity": 1, "unit": "tbsp"},
        {"name": "lemon (optional)", "quantity": 0.25, "unit": "pcs"},
        {"name": "onion (for serving, optional)", "quantity": 0.25, "unit": "medium"},
        {"name": "coriander (optional garnish)", "quantity": 2, "unit": "tbsp"},
        {"name": "roti/chapati", "quantity": 4, "unit": "pcs"}
    ],
    "steps": [
        "Chop onion, tomato and green chili.",
        "Heat oil in a pan and add mustard seeds. Let them splutter.",
        "Add curry leaves and chopped onions. Sauté until translucent.",
        "Add ginger garlic paste and sauté for 30 seconds.",
        "Add tomato, green chili, turmeric, red chili, coriander powder, pepper powder (optional) and cook until soft.",
        "Beat eggs with salt and pour into the pan. Scramble until cooked.",
        "Garnish with coriander. Serve with rotis, lemon, and sliced onions."
    ]
}

# Insert primary recipe
db.collection("recipes").document(primary_recipe["id"]).set(primary_recipe)
print("Inserted primary recipe.")

# 3. Synthetic recipes

def generate_synthetic_recipe(i):
    ingredients_list = ["salt", "onion", "tomato", "garlic", "oil", "rice", "carrot", "potato"]
    recipe = {
        "id": f"recipe_{i}",
        "title": f"Synthetic Recipe {i}",
        "description": "Auto-generated test recipe",
        "servings": random.randint(1,4),
        "prep_time_min": random.randint(5,15),
        "cook_time_min": random.randint(5,25),
        "difficulty": random.choice(["easy","medium","hard"]),
        "tags": random.sample(["veg","quick","non-veg","home-style"], 2),
        "created_at": datetime.now(datetime.UTC).isoformat(),
        "ingredients": [
            {
                "name": random.choice(ingredients_list),
                "quantity": random.randint(1,4),
                "unit": random.choice(["pcs","tsp","tbsp","g"])
            }
            for _ in range(random.randint(3,6))
        ],
        "steps": [f"Step {x+1} of recipe {i}" for x in range(random.randint(2,5))]
    }
    recipe["total_time_min"] = recipe["prep_time_min"] + recipe["cook_time_min"]
    return recipe

# Insert 15 synthetic recipes
synthetic_recipes = []
for i in range(1, 16):
    recipe = generate_synthetic_recipe(i)
    synthetic_recipes.append(recipe)
    db.collection("recipes").document(recipe["id"]).set(recipe)

print("Inserted synthetic recipes.")

# 4. Users

users = []
for i in range(1, 11):
    user = {
        "id": f"user_{i}",
        "name": f"User {i}",
        "email": f"user{i}@gmail.com",
        "signup_date": datetime.now(datetime.UTC).isoformat()
    }
    users.append(user)
    db.collection("users").document(user["id"]).set(user)

print("Inserted users.")


# 5. Interactions

interactions = []
int_id = 1

for user in users:
    for recipe in random.sample([primary_recipe] + synthetic_recipes, random.randint(5,10)):

        # View
        interactions.append({
            "id": f"int_{int_id}",
            "user_id": user["id"],
            "recipe_id": recipe["id"],
            "type": "view",
            "timestamp": datetime.now(datetime.UTC).isoformat()
        })
        db.collection("interactions").document(f"int_{int_id}").set(interactions[-1])
        int_id += 1

        # Like
        if random.random() < 0.4:
            interactions.append({
                "id": f"int_{int_id}",
                "user_id": user["id"],
                "recipe_id": recipe["id"],
                "type": "like",
                "timestamp": datetime.now(datetime.UTC).isoformat()
            })
            db.collection("interactions").document(f"int_{int_id}").set(interactions[-1])
            int_id += 1

        # Cook attempt
        if random.random() < 0.2:
            interactions.append({
                "id": f"int_{int_id}",
                "user_id": user["id"],
                "recipe_id": recipe["id"],
                "type": "cook",
                "rating": random.choice([3,4,5]),
                "difficulty_used": random.choice(["easy","medium","hard"]),
                "timestamp": datetime.now(datetime.UTC).isoformat()
            })
            db.collection("interactions").document(f"int_{int_id}").set(interactions[-1])
            int_id += 1

print("Inserted user interactions.")
print("Firestore data setup completed.")
