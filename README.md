# RECIPE ANALYTICS PIPELINE (Firebase + Python ETL)

**Name:** R Dheeraj Reddy  
**Batch:** Data Engineer  
**Email:** dheerajr.ramireddy@gmail.com 


## Table Of Contents:
[1. Data Model Overview](#1-data-model-overview)

- [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)

[2. Running the End-to-End Pipeline](#2-running-the-end-to-end-pipeline)

- [Step 2 — Populate Firestore](#step-2--populate-firestore)

- [Step 3 — Export Firestore and Run ETL](#step-3--export-firestore-and-run-etl)

- [Step 4 — Data Quality Validation](#step-4--data-quality-validation)

[3. ETL Process Summary](#3-etl-process-summary)

[4. Analytics Summary (10+ Insights)](#4-analytics-summary-10-insights)

- [Analytics Visualizations](#analytics-visualizations)

[5. Known Constraints / Limitations](#5-known-constraints--limitations)

[6. Technologies Used](#6-technologies-used)

[7. How to Extend](#7-how-to-extend)



This project implements a complete data engineering pipeline using Firebase Firestore as the source system.
It demonstrates data modeling, data ingestion, ETL/ELT processing, data validation, analytics, and reporting.

The dataset includes the candidate’s own recipe (Egg Burji + Roti) and synthetic supporting data.

## 1. DATA MODEL OVERVIEW

The system contains five logical entities:
-    Recipes
-    Ingredients
-   Steps
-    Users
-    User Interactions (views, likes, cook attempts)

Entity Relationships
-    A recipe has many ingredients
-    A recipe has many steps
-    A user generates many interactions
-    An interaction belongs to one user and one recipe

Key Fields

Recipe:
-    id, title, description
-    prep_time, cook_time, total_time
-    difficulty (easy, medium, hard)
-    tags
-    ingredients[]
-    steps[]
-    created_at

User:
-    id, name, email, signup_date

Interaction:
-    id, user_id, recipe_id
-   type (view, like, cook)
-    rating (optional)
-    difficulty_used (optional)
-    timestamp

A full schema and ERD-style diagram is included in:
-    ../docs/Step1_Data_Model.md

## Entity Relationship Diagram (ERD)
```Mermaid```
![ER Diagram](./outputs/png/erd_recipe.png)


## 2. RUNNING THE END-TO-END PIPELINE

The project uses a simple directory layout:
```
de_recipe_pipeline/
    codes/
    data/
        raw/
        processed/
    outputs/
    docs/
    README.md
```
### Step 2 — Populate Firestore

Add your service account:
-    serviceAccountKey.json

Install dependencies:
-   pip install firebase-admin

Run the ingestion script:
-    python codes/upload_to_firestore.py

This creates:
-    Primary recipe
-    15 synthetic recipes
-    10 users
-    100–200 interactions

Stored in Firestore as:
- recipes/
- users/
- interactions/

### Step 3 — Export Firestore and Run ETL

Export Firestore → JSON:
-    python codes/export_from_firestore.py

Produces:
-    data/raw/recipes.json
-    data/raw/users.json
-    data/raw/interactions.json

Transform JSON → Normalized CSV:
-    python codes/transform_to_csv.py


Outputs:
-    data/processed/recipes.csv
-    data/processed/ingredients.csv
-    data/processed/steps.csv
-    data/processed/interactions.csv


### Step 4 — Data Quality Validation

Run the validator:
-    python codes/validate_data.py

Produces:
-    outputs/validation_report.json

Contains:
-    Valid record count
-    Invalid records
-    Error messages for each invalid field

Validation rules are documented in:
-    docs/Step4_Data_Quality_Validation.md

## 3. ETL PROCESS SUMMARY

Extract:
-    Read Firestore collections using Firebase Admin SDK
-    Save each collection as JSON

Transform:
-    Flatten nested recipe structures (ingredients, steps)
-    Normalize into separate tables
-    Enforce consistent schemas
-    Default missing optional fields to None
-    Prepare for validation and analytics

Load:
-    Store normalized tables in data/processed/*.csv

This pipeline ensures the data is clean, well-structured, and analytics-ready.

## 4. ANALYTICS SUMMARY (10+ INSIGHTS)

Using the normalized tables, the following insights were generated:
-    Most common ingredients: onion, salt, tomato, oil
-    Average prep time: ~10 minutes
-    Average cook time: ~15 minutes
-    Difficulty distribution: mostly “easy” recipes
-    Most viewed recipes: dominated by simple synthetic dishes
-    Most liked recipes: recipes with <6 ingredients 
-    Cook attempts: highest for “quick” and “home-style” recipes
-    Prep time vs likes: shorter prep time → more likes
-    Ingredients linked to high engagement: onion, tomato, eggs, garlic
-    User behavior: users view many recipes but attempt to cook fewer
-    Ingredient count vs popularity: simple recipes get more engagement
-    Egg Burji performs well but not the highest interacted (expected due to random sampling)

Full insight descriptions:
-    docs/Step5_Analytics_Insights.md


Charts (optional) will be placed in:
-   outputs/charts/

### Analytics Visualizations

Below are optional charts illustrating insights generated from the dataset:
- **Difficulty distribution**  
  ![](./outputs/charts/difficulty_distribution.png)

- **Most common ingredients**  
  ![](./outputs/charts/top_ingredients.png)

- **Top viewed recipes**  
  ![](./outputs/charts/top_views.png)

- **Top liked recipes**  
  ![](./outputs/charts/top_likes.png)

- **Prep time vs likes**  
  ![](./outputs/charts/prep_vs_likes.png)

## 5. KNOWN CONSTRAINTS/ LIMITATIONS

The constraints/limitations are:
- Synthetic recipes are randomly generated and not real dishes
- Interaction data is synthetic and probabilistic
- Analytics are based on small sample sizes
- Firestore export is not the full Google Cloud “export/import” format
- Synthetic randomness may result in some recipes dominating interactions
- These limitations are expected and acceptable given the project scope.

## 6. TECHNOLOGIES USED
The technologies used in the project are:
- Firebase Firestore (source system)
- Python 3
- Firebase Admin SDK
- CSV-based normalized tables
- Pandas
- Matplotlib

## 7. HOW TO EXTEND

Optional future enhancements:
-    Add a dashboard (PowerBI)
-    Generate more realistic synthetic recipes
-    Add storage layers(SQL)




## 8. Conclusion 

This project demonstrates my ability to design end-to-end data engineering workflows, including data modeling, ETL, validation, and analytics using Firebase and Python. It is a complete pipeline that reflects real-world data engineering tasks.

