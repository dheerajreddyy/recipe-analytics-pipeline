import json
import csv
import os

# Ensure processed folder exists
os.makedirs("../data/processed", exist_ok=True)

# Load JSON files
with open("../data/raw/recipes.json") as f:
    recipes = json.load(f)

with open("../data/raw/interactions.json") as f:
    interactions = json.load(f)

# 1. recipes.csv 

recipe_rows = []
ingredient_rows = []
steps_rows = []

for r in recipes:
    recipe_rows.append({
        "id": r.get("id"),
        "title": r.get("title"),
        "description": r.get("description", ""),
        "servings": r.get("servings", None),
        "prep_time_min": r.get("prep_time_min", None),
        "cook_time_min": r.get("cook_time_min", None),
        "total_time_min": r.get("total_time_min", None),
        "difficulty": r.get("difficulty", None),
        "created_at": r.get("created_at", None)
    })

    # Ingredients → ingredients.csv
    for i, ing in enumerate(r.get("ingredients", [])):
        ingredient_rows.append({
            "recipe_id": r.get("id"),
            "ingredient_id": f"{r.get('id')}_ing_{i+1}",
            "name": ing.get("name"),
            "quantity": ing.get("quantity"),
            "unit": ing.get("unit")
        })

    # Steps → steps.csv
    for i, step in enumerate(r.get("steps", [])):
        steps_rows.append({
            "recipe_id": r.get("id"),
            "step_number": i + 1,
            "description": step
        })


# Write recipes.csv
with open("../data/processed/recipes.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=recipe_rows[0].keys())
    writer.writeheader()
    writer.writerows(recipe_rows)


# Write ingredients.csv

with open("../data/processed/ingredients.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=ingredient_rows[0].keys())
    writer.writeheader()
    writer.writerows(ingredient_rows)


# Write steps.csv
with open("../data/processed/steps.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=steps_rows[0].keys())
    writer.writeheader()
    writer.writerows(steps_rows)

# 2. interactions.csv 

interaction_fields = [
    "id",
    "user_id",
    "recipe_id",
    "type",
    "timestamp",
    "rating",
    "difficulty_used"
]

# Normalize each interaction so all fields exist
normalized_interactions = []
for it in interactions:
    row = {
        "id": it.get("id"),
        "user_id": it.get("user_id"),
        "recipe_id": it.get("recipe_id"),
        "type": it.get("type"),
        "timestamp": it.get("timestamp"),
        "rating": it.get("rating", None),
        "difficulty_used": it.get("difficulty_used", None)
    }
    normalized_interactions.append(row)

# Write interactions.csv
with open("../data/processed/interactions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=interaction_fields)
    writer.writeheader()
    writer.writerows(normalized_interactions)


print("ETL transformation complete. CSV files saved in data/processed/")
