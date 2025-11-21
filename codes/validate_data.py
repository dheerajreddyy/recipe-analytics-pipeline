import csv
import os
import json

INPUT_FOLDER = "../data/processed"
REPORT_FILE = "../outputs/validation_report.json"

os.makedirs("../outputs", exist_ok=True)

def load_csv(filename):
    path = os.path.join(INPUT_FOLDER, filename)
    with open(path, "r") as f:
        return list(csv.DictReader(f))

def validate_recipes(rows):
    valid = []
    invalid = []

    for r in rows:
        errors = []

        # Required fields
        if not r["id"]: errors.append("Missing id")
        if not r["title"]: errors.append("Missing title")

        # Numeric fields
        try:
            if int(r["servings"]) <= 0:
                errors.append("servings must be > 0")
        except:
            errors.append("invalid servings")

        for field in ["prep_time_min", "cook_time_min", "total_time_min"]:
            try:
                if int(r[field]) < 0:
                    errors.append(f"{field} must be >= 0")
            except:
                errors.append(f"invalid {field}")

        # Difficulty
        if r["difficulty"] not in ["easy", "medium", "hard"]:
            errors.append("invalid difficulty")

        # Timestamp
        if not r["created_at"]:
            errors.append("missing created_at")

        if errors:
            invalid.append({"record": r, "errors": errors})
        else:
            valid.append(r)

    return valid, invalid

def validate_ingredients(rows):
    valid = []
    invalid = []

    for ing in rows:
        errors = []

        if not ing["recipe_id"]: errors.append("missing recipe_id")
        if not ing["ingredient_id"]: errors.append("missing ingredient_id")
        if not ing["name"]: errors.append("missing name")

        try:
            if float(ing["quantity"]) < 0:
                errors.append("quantity must be >= 0")
        except:
            errors.append("invalid quantity")

        if not ing["unit"]:
            errors.append("missing unit")

        if errors:
            invalid.append({"record": ing, "errors": errors})
        else:
            valid.append(ing)

    return valid, invalid

def validate_steps(rows):
    valid = []
    invalid = []

    for s in rows:
        errors = []

        if not s["recipe_id"]:
            errors.append("missing recipe_id")

        try:
            if int(s["step_number"]) < 1:
                errors.append("step_number must be >= 1")
        except:
            errors.append("invalid step_number")

        if not s["description"]:
            errors.append("missing description")

        if errors:
            invalid.append({"record": s, "errors": errors})
        else:
            valid.append(s)

    return valid, invalid

def validate_interactions(rows):
    valid = []
    invalid = []

    for it in rows:
        errors = []

        if not it["id"]: errors.append("missing id")
        if not it["user_id"]: errors.append("missing user_id")
        if not it["recipe_id"]: errors.append("missing recipe_id")

        if it["type"] not in ["view", "like", "cook"]:
            errors.append("invalid type")

        if not it["timestamp"]:
            errors.append("missing timestamp")

        # Optional: rating only for cook
        if it["rating"]:
            try:
                r = int(it["rating"])
                if r < 1 or r > 5:
                    errors.append("rating must be 1–5")
            except:
                errors.append("invalid rating")

        # Optional difficulty_used
        if it["difficulty_used"]:
            if it["difficulty_used"] not in ["easy", "medium", "hard"]:
                errors.append("invalid difficulty_used")

        if errors:
            invalid.append({"record": it, "errors": errors})
        else:
            valid.append(it)

    return valid, invalid


# Load data
recipes = load_csv("recipes.csv")
ingredients = load_csv("ingredients.csv")
steps = load_csv("steps.csv")
interactions = load_csv("interactions.csv")

# Validate all
valid_recipes, invalid_recipes = validate_recipes(recipes)
valid_ingredients, invalid_ingredients = validate_ingredients(ingredients)
valid_steps, invalid_steps = validate_steps(steps)
valid_interactions, invalid_interactions = validate_interactions(interactions)

# Build report
report = {
    "recipes": {"valid": len(valid_recipes), "invalid": invalid_recipes},
    "ingredients": {"valid": len(valid_ingredients), "invalid": invalid_ingredients},
    "steps": {"valid": len(valid_steps), "invalid": invalid_steps},
    "interactions": {"valid": len(valid_interactions), "invalid": invalid_interactions},
}

# Save JSON report
with open(REPORT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print("Validation complete. Report saved to outputs/validation_report.json")
