import pandas as pd
import matplotlib.pyplot as plt
import os

# Output folder for charts
out_dir = "../outputs/charts"
os.makedirs(out_dir, exist_ok=True)

# Load CSVs with Windows-safe encoding
recipes = pd.read_csv("../data/processed/recipes.csv", encoding="latin1")
ingredients = pd.read_csv("../data/processed/ingredients.csv", encoding="latin1")
interactions = pd.read_csv("../data/processed/interactions.csv", encoding="latin1")

# -----------------------------------------------------------------------------
# 1. Difficulty Distribution
# -----------------------------------------------------------------------------
plt.figure()
recipes["difficulty"].value_counts().plot(kind="bar")
plt.title("Difficulty Distribution")
plt.xlabel("Difficulty")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{out_dir}/difficulty_distribution.png")
plt.close()

# -----------------------------------------------------------------------------
# 2. Top 10 Ingredients
# -----------------------------------------------------------------------------
plt.figure()
ingredients["name"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Ingredients")
plt.xlabel("Ingredient")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{out_dir}/top_ingredients.png")
plt.close()

# -----------------------------------------------------------------------------
# 3. Top Viewed Recipes
# -----------------------------------------------------------------------------
plt.figure()
view_counts = (
    interactions[interactions["type"] == "view"]
    .groupby("recipe_id")
    .size()
    .sort_values(ascending=False)
    .head(10)
)
view_counts.plot(kind="bar")
plt.title("Top Viewed Recipes")
plt.xlabel("Recipe ID")
plt.ylabel("Views")
plt.tight_layout()
plt.savefig(f"{out_dir}/top_views.png")
plt.close()

# -----------------------------------------------------------------------------
# 4. Top Liked Recipes
# -----------------------------------------------------------------------------
plt.figure()
like_counts = (
    interactions[interactions["type"] == "like"]
    .groupby("recipe_id")
    .size()
    .sort_values(ascending=False)
    .head(10)
)
like_counts.plot(kind="bar")
plt.title("Top Liked Recipes")
plt.xlabel("Recipe ID")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig(f"{out_dir}/top_likes.png")
plt.close()

# -----------------------------------------------------------------------------
# 5. Prep Time vs Likes (Scatter Plot)
# -----------------------------------------------------------------------------
likes_per_recipe = interactions[interactions["type"] == "like"] \
    .groupby("recipe_id").size().rename("likes")

prep_times = recipes.set_index("id")["prep_time_min"]

merged = prep_times.to_frame().join(likes_per_recipe, how="left").fillna(0)

plt.figure()
plt.scatter(merged["prep_time_min"], merged["likes"])
plt.title("Prep Time vs Likes")
plt.xlabel("Prep Time (min)")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig(f"{out_dir}/prep_vs_likes.png")
plt.close()

print("Charts generated successfully in outputs/charts/")
