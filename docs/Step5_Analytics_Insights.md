## STEP 5 - Analytics Insights

## Overview:
This analysis uses the cleaned CSV output from Step 3 to generate insights about recipe usage, ingredients, difficulty levels, and user engagement. The dataset includes:
    16 recipes (1 real + 15 synthetic)
    85 ingredients
    60 recipe steps
    ~150 user interactions

Insights were derived using simple aggregations on the normalized tables.

## Insight 1 — Most Common Ingredients

Across all recipes, the most frequently used ingredients were:
    Onion
    Salt
    Oil
    Tomato
    Garlic / Ginger Garlic Paste

These ingredients appear consistently across both the real and synthetic recipes and represent typical Indian home cooking ingredients.


## Insight 2 — Average Preparation & Cooking Time

Average preparation time: ~10 minutes
Average cooking time: ~15 minutes
Average total time: ~25 minutes

This shows that most recipes are quick home-style dishes.

## Insight 3 — Difficulty Distribution

From recipes.csv:
    Easy: Majority of recipes
    Medium: Moderate count
    Hard: Very few

This suggests the dataset primarily represents beginner-friendly or everyday cooking.

## Insight 4 — Most Viewed Recipes

Based on interactions:
    The top viewed recipes were typically easy and used fewer ingredients
    The candidate’s recipe (Egg Burji + Roti) had high engagement due to its simplicity and familiarity

This suggests simplicity increases user attention.

## Insight 5 — Most Liked Recipes

Recipes with:
    Fewer than 6 ingredients
    Total time under 20 minutes
    received more likes than complex or long-duration recipes.

Users prefer quick and simple dishes.

## Insight 6 — Most Frequently Cooked (Cook Attempts)

Cook attempts were highest for recipes tagged:
    “quick”
    “home-style”
    “veg”

These tags align with practical, everyday cooking needs.

## Insight 7 — Correlation Between Prep Time and Likes

A clear pattern:
    Recipes with prep_time < 10 minutes received more likes
    Recipes with prep_time > 15 minutes consistently received fewer likes

Shows users favor low-effort meals.

## Insight 8 — Ingredients Associated With High Engagement

By grouping interactions by recipe ingredients, the following ingredients correlate with higher views and likes:
    Onion
    Tomato
    Eggs
    Garlic

These are core Indian cooking ingredients, explaining their popularity.

## Insight 9 — User Behavior Patterns

Users generally:
    View more recipes than they like
    Like ~40% of viewed recipes (consistent with the synthetic model)
    Attempt to cook ~20% of liked recipes

This suggests that Users browse widely but cook selectively.

## Insight 10 — Engagement by Difficulty

Average interactions per recipe:
    Difficulty	    Avg Interactions
    Easy	        High
    Medium	        Moderate
    Hard	        Low

This confirms that easier recipes attract more views, likes, and cook attempts.

## Insight 11 — Ingredient Count vs Engagement

Recipes with 3–6 ingredients had the highest engagement.
Recipes with >8 ingredients showed a drop in interactions.

Users prefer short, simple ingredient lists.

## Insight 12 — Candidate’s Recipe Performance

The primary recipe (Egg Burji + Roti):
    Appears in top viewed
    Has high like count
    Has multiple cook attempts
    Has ingredients that appear frequently across other recipes (egg, onion, tomato)


### Difficulty Distribution
![Difficulty](../outputs/charts/difficulty_distribution.png)

### Top Ingredients
![Ingredients](../outputs/charts/top_ingredients.png)

### Top Viewed Recipes
![Views](../outputs/charts/top_views.png)

### Top Liked Recipes
![Likes](../outputs/charts/top_likes.png)

### Prep Time vs Likes
![Scatter](../outputs/charts/prep_vs_likes.png)
