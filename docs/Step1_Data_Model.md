## STEP 1 — Data Modelling
This is Step 1 of the Data Engineering Assessment: Data Modeling.

## 1. Overview

This document defines the complete data model for the Firebase-based Recipe Analytics Pipeline.
It includes:
    List of entities
    ERD (Entity Relationship Diagram)
    Schema (fields + types) for each entity
    The candidate’s own recipe as the primary dataset

This data model will be used for Firestore storage, ETL transformation, data validation, and analytics.


## 2. Entities (Collections / Tables)

The system contains the following 5 logical entities:
    Recipes
    Ingredients (derived from Recipes)
    Steps (derived from Recipes)
    Users
    User Interactions (views, likes, cook attempts)

These entities together describe a complete recipe platform with user engagement.



## 3. ERD (Entity Relationship Diagram)

+-----------+        +------------------+        +------------------+
|   users   | 1    * |   interactions   | *    1 |     recipes      |
+-----------+        +------------------+        +------------------+
| id (PK)   |<-------| user_id (FK)     |------->| id (PK)          |
| name      |        | recipe_id (FK)   |        | title            |
| email     |        | type             |        | description      |
| signup... |        | timestamp        |        | servings         |
+-----------+        | rating (opt)     |        | prep_time_min    |
                     | difficulty_used  |        | cook_time_min    |
                     +------------------+        | total_time_min   |
                                                 | difficulty       |
                                                 | tags             |
                                                 | created_at       |
                                                 +------------------+

One recipe has many ingredients         One recipe has many steps
+-------------+                              +-------------+
| ingredients |                              |    steps    |
+-------------+                              +-------------+
| recipe_id   |                              | recipe_id   |
| ingr_id (PK)|                              | step_number |
| name        |                              | description |
| quantity    |                              +-------------+
| unit        |
+-------------+


```MERMAID CODE:```
---
config:
  theme: mc
  look: neo
  layout: dagre
---
erDiagram
    USERS ||--o{ INTERACTIONS : "1-to-many"
    RECIPES ||--o{ INTERACTIONS : "1-to-many"
    RECIPES ||--o{ INGREDIENTS : "1-to-many"
    RECIPES ||--o{ STEPS : "1-to-many"
    USERS {
        string id PK
        string name
        string email
        string signup_date
    }
    RECIPES {
        string id PK
        string title
        string description
        int servings
        int prep_time_min
        int cook_time_min
        int total_time_min
        string difficulty
        string tags
        string created_at
    }
    INGREDIENTS {
        string ingredient_id PK
        string recipe_id FK
        string name
        float quantity
        string unit
    }
    STEPS {
        int step_number
        string recipe_id FK
        string description
    }
    INTERACTIONS {
        string id PK
        string user_id FK
        string recipe_id FK
        string type
        string timestamp
        int rating
        string difficulty_used
    }


## 4. Schema Definitions

Below are the field definitions for each entity.
These will guide Firestore structure and CSV outputs.

4.1 Recipes:
        FIELD	                    TYPE	                DESCRIPTION
        id	                        string (PK)          	Unique recipe ID
        title	                    string	                Recipe title
        description	                string	                Short recipe description
        servings	                integer	                Must be > 0
        prep_time_min	            integer	                Minutes, >= 0
        cook_time_min	            integer	                Minutes, >= 0
        total_time_min	            integer	                prep + cook
        difficulty	                string	                one of: easy, medium, hard
        tags	                    array[string]	        Optional (ex: “veg”, “spicy”)
        created_at	                string (ISO timestamp)	When the recipe was added

4.2 Ingredients (derived table after ETL):
        FIELD	                    TYPE	                DESCRIPTION
        recipe_id	                string	                FK → recipes.id
        ingredient_id	            string	                Unique ID per recipe
        name	                    string	                Ingredient name
        quantity	                number	                Must be >= 0
        unit	                    string	                g, tsp, tbsp, pcs, etc.

4.3 Steps (derived table after ETL):
        FIELD	                    TYPE	                DESCRIPTION
        recipe_id	                string	                FK → recipes.id
        step_number	                integer	                1,2,3,...
        description	                string	                Step instruction

4.4 Users:
        FIELD	                    TYPE	                DESCRIPTION
        id	                        string (PK)	            Unique user ID
        name	                    string	                User name
        email	                    string	                Unique email
        signup_date	                string (ISO timestamp)	When user signed up
        preferences	                array[string]	        Optional e.g. “south-indian” etc

4.5 User Interactions:
        FIELD	                    TYPE	                DESCRIPTION
        id	                        string (PK)	            Unique interaction ID
        user_id	                    string	                FK → users.id
        recipe_id	                string	                FK → recipes.id
        type	                    string	                view, like, cook
        timestamp	                string (ISO)	        Event timestamp
        rating	                    integer (optional)	    1–5, only for cook attempts
        difficulty_used	            string (optional)	    User-assigned difficulty


This enables analytics on:
        recipe popularity
        user behavior
        engagement metrics



## 5. Candidate’s Primary Recipe (Anda(Egg) Burji + Roti):

{
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
  "created_at": "2025-11-15T08:00:00Z"
}
