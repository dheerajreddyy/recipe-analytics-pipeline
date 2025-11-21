import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Output directory
out_dir = "../outputs/charts"
os.makedirs(out_dir, exist_ok=True)

# Load CSVs
recipes = pd.read_csv("../data/processed/recipes.csv", encoding="latin1")
ingredients = pd.read_csv("../data/processed/ingredients.csv", encoding="latin1")
interactions = pd.read_csv("../data/processed/interactions.csv", encoding="latin1")

# ---------------------------
# Global premium styling
# ---------------------------
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "axes.titlesize": 18,
    "axes.labelsize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.edgecolor": "#444",
    "axes.linewidth": 1.2,
    "grid.color": "#DDDDDD",
    "grid.linestyle": "--",
    "grid.alpha": 0.6
})

def rounded_bar(ax, x, height, color):
    ax.bar(x, height, color=color, edgecolor="#333", linewidth=1.2)

def save(name):
    plt.tight_layout()
    plt.savefig(f"{out_dir}/{name}.png", dpi=200, bbox_inches="tight")
    plt.close()


# ================================
# 1️⃣ Difficulty Distribution
# ================================
plt.figure()
ax = plt.gca()

counts = recipes["difficulty"].value_counts()
colors = ["#7FA8FF", "#9CD39C", "#F4B183"]

rounded_bar(ax, counts.index, counts.values, colors[:len(counts)])

ax.set_title("Difficulty Distribution")
ax.set_xlabel("Difficulty Level")
ax.set_ylabel("Number of Recipes")
ax.grid(axis="y")

# Add values on top
for i, v in enumerate(counts.values):
    ax.text(i, v + 0.5, str(v), ha="center", fontsize=12)

save("difficulty_distribution")


# ================================
# 2️⃣ Top Ingredients
# ================================
plt.figure()
ax = plt.gca()

top_ing = ingredients["name"].value_counts().head(10)
rounded_bar(ax, top_ing.index, top_ing.values, "#8FAADC")

ax.set_title("Top 10 Most Common Ingredients")
ax.set_xlabel("Ingredient")
ax.set_ylabel("Count")
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y")

save("top_ingredients")


# ================================
# 3️⃣ Top Viewed Recipes
# ================================
plt.figure()
ax = plt.gca()

views = interactions[interactions["type"] == "view"] \
        .groupby("recipe_id").size().sort_values(ascending=False).head(10)

rounded_bar(ax, views.index, views.values, "#FFD966")

ax.set_title("Top 10 Viewed Recipes")
ax.set_xlabel("Recipe ID")
ax.set_ylabel("Views")
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y")

save("top_views")


# ================================
# 4️⃣ Top Liked Recipes
# ================================
plt.figure()
ax = plt.gca()

likes = interactions[interactions["type"] == "like"] \
        .groupby("recipe_id").size().sort_values(ascending=False).head(10)

rounded_bar(ax, likes.index, likes.values, "#F7A77F")

ax.set_title("Top 10 Liked Recipes")
ax.set_xlabel("Recipe ID")
ax.set_ylabel("Likes")
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y")

save("top_likes")


# ================================
# 5️⃣ Prep Time vs Likes
# ================================
plt.figure()
ax = plt.gca()

likes_per_recipe = interactions[interactions["type"] == "like"] \
                    .groupby("recipe_id").size().rename("likes")

prep_times = recipes.set_index("id")["prep_time_min"]
merged = prep_times.to_frame().join(likes_per_recipe, how="left").fillna(0)

plt.scatter(
    merged["prep_time_min"],
    merged["likes"],
    s=140,
    color="#6EC1E4",
    edgecolor="#2A5775",
    linewidth=1.0,
    alpha=0.85
)

ax.set_title("Prep Time vs Likes")
ax.set_xlabel("Prep Time (minutes)")
ax.set_ylabel("Likes")
ax.grid(True)

save("prep_vs_likes")

print("✨ Premium A1 corporate charts generated successfully!")
