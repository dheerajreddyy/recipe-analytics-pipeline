import json
import os
import random
from datetime import datetime, timedelta

# Output folder
os.makedirs("data", exist_ok=True)

OUTPUT_FILE = "data/firestore_export.json"


# My main recipe

def get_primary_recipe():
    return {
        "id": "recipe_egg_burji_roti",
        "title": "Egg Burji + Roti (South Indian style) for 2",
        "description": "Spicy scrambled eggs served with soft rotis — South Indian home style, no sauces.",
        "servings": 2,
        "prep_time_min": 12,
        "cook_time_min": 10,
        "total_time_min": 22,
        "difficulty": "easy",
        "ingredients": [
            { "name": "eggs", "quantity": 4, "unit": "pcs" },
            { "name": "onion", "quantity": 1, "unit": "medium" },
            { "name": "tomato", "quantity": 1, "unit": "medium" },
            { "name": "green chili", "quantity": 1, "unit": "pcs" },
            { "name": "curry leaves", "quantity": 6, "unit": "leaves" },
            { "name": "ginger garlic paste", "quantity": 1, "unit": "tsp" },
            { "name": "mustard seeds", "quantity": 0.25, "unit": "tsp" },
            { "name": "turmeric powder", "quantity": 0.25, "unit": "tsp" },
            { "name": "red chili powder", "quantity": 0.5, "unit": "tsp" },
            { "name": "coriander powder", "quantity": 0.5, "unit": "tsp" },
            { "name": "pepper powder (optional)", "quantity": 0.25, "unit": "tsp" },
            { "name": "salt", "quantity": 0.5, "unit": "tsp" },
            { "name": "oil", "quantity": 1, "unit": "tbsp" },
            { "name": "lemon (optional)", "quantity": 0.25, "unit": "pcs" },
            { "name": "onion (for serving, optional)", "quantity": 0.25, "unit": "medium" },
            { "name": "coriander (optional garnish)", "quantity": 2, "unit": "tbsp" },
            { "name": "roti/chapati", "quantity": 4, "unit": "pcs" }
        ],
        "steps": [
            "Chop onion, tomato and green chili.",
            "Heat oil in a pan and add mustard seeds. Let them splutter.",
            "Add curry leaves and chopped onions. Sauté until translucent.",
            "Add ginger garlic paste and sauté for 30 seconds.",
            "Add tomato, green chili, turmeric, red chili, coriander powder, and pepper powder (optional). Cook until tomatoes soften.",
            "Beat eggs with salt and pour into the pan. Scramble gently until cooked.",
            "Garnish with coriander. Serve hot with rotis, lemon, and sliced onions (optional)."
        ],
        "tags": ["south-indian", "breakfast", "eggs"],
        "created_at": datetime.now(datetime.UTC).isoformat()
    }

# synthetic recipes

def generate_synthetic_recipe(i):
    ingredients_list = ["salt", "onion", "tomato", "garlic", "oil", "rice", "chicken", "carrot"]
    return {
        "id": f"recipe_{i}",
        "title": f"Synthetic Recipe {i}",
        "description": "Auto-generated recipe",
        "servings": random.choice([1,2,3,4]),
        "prep_time_min": random.randint(5,20),
        "cook_time_min": random.randint(5,30),
        "total_time_min": 0,  # filled later
        "difficulty": random.choice(["easy", "medium", "hard"]),
        "ingredients": [
            {
                "name": random.choice(ingredients_list),
                "quantity": random.randint(1,5),
                "unit": random.choice(["pcs", "tsp", "tbsp", "g"])
            }
            for _ in range(random.randint(3,6))
        ],
        "steps": [f"Step {x+1} of recipe {i}" for x in range(random.randint(2,5))],
        "tags": random.sample(["veg", "quick", "non-veg", "home-style"], 2),
        "created_at": (datetime.now() - timedelta(days=random.randint(1,300))).isoformat() + "Z"
    }


# generate users

def generate_users(count=10):
    return [
        {
            "id": f"user_{i}",
            "name": f"User {i}",
            "email": f"user{i}@gmail.com",
            "signup_date": (datetime.now() - timedelta(days=random.randint(1,500))).isoformat() + "Z"
        }
        for i in range(1, count+1)
    ]


# generate interactions

def generate_interactions(users, recipes):
    interactions = []
    int_id = 1
    for user in users:
        for recipe in random.sample(recipes, random.randint(5,10)):
            # view
            interactions.append({
                "id": f"int_{int_id}",
                "user_id": user["id"],
                "recipe_id": recipe["id"],
                "type": "view",
                "timestamp": datetime.now(datetime.UTC).isoformat()
            })
            int_id += 1

            # like
            if random.random() < 0.4:
                interactions.append({
                    "id": f"int_{int_id}",
                    "user_id": user["id"],
                    "recipe_id": recipe["id"],
                    "type": "like",
                    "timestamp": datetime.now(datetime.UTC).isoformat()
                })
                int_id += 1

            # cook attempt
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
                int_id += 1
    return interactions


# Build dataset

recipes = [get_primary_recipe()]
for i in range(1, 16):
    r = generate_synthetic_recipe(i)
    r["total_time_min"] = r["prep_time_min"] + r["cook_time_min"]
    recipes.append(r)

users = generate_users()
interactions = generate_interactions(users, recipes)

full_export = {
    "recipes": recipes,
    "users": users,
    "interactions": interactions
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(full_export, f, indent=2)

print("Generated Firestore-like dataset at:", OUTPUT_FILE)
