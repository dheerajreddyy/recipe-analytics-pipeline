## STEP 3 — ETL Pipeline

## Overview:
This step extracts data from Firestore, transforms it into normalized tabular structures, and loads the final output into CSV files.
The output tables will be used for validation and analytics.

The ETL process consists of:
    Extract Firestore collections to JSON
    Transform the JSON into normalized tables
    Load the results into CSV files

## 3.1 Extract — Export Firestore Collections

Firestore source data is exported using:
    codes/export_from_firestore.py


This script connects to Firestore through the Firebase Admin SDK and exports:
    recipes
    users
    interactions

The exported files are stored in:
    data/raw/recipes.json
    data/raw/users.json
    data/raw/interactions.json

## 3.2 Transform — JSON to Normalized Tables

Transformation is implemented in Python using the script:
    codes/transform_to_csv.py

The script performs the following actions:
    Recipes:
        Extracts flat recipe fields
        Removes nested arrays
        Stores results in recipes.csv

    Ingredients:
        Extracts each ingredient from the nested list
        Generates a unique ingredient_id
        Stores results in ingredients.csv

    Steps:
        Flattens the steps array
        Generates sequential step_number per recipe
        Stores results in steps.csv

    Interactions:
        Ensures a consistent schema for event records
        Adds missing optional fields (rating, difficulty_used) as None
        Stores results in interactions.csv

## 3.3 Load — Write Clean CSV Output

Normalized CSV output files are written to:
    data/processed/
        recipes.csv
        ingredients.csv
        steps.csv
        interactions.csv

Each file is flat, consistent, and free of schema inconsistencies.

## Output Schema Summary:

recipes.csv:

column	        description
id	            recipe ID
title	        recipe name
description	    summary text
servings	    numeric
prep_time_min	numeric
cook_time_min	numeric
total_time_min	numeric
difficulty	    easy/medium/hard
created_at	    timestamp

ingredients.csv:
column	        description
recipe_id	    FK → recipes.id
ingredient_id	unique per ingredient
name	        ingredient name
quantity	    numeric
unit	        measurement unit

steps.csv:
column	        description
recipe_id	    FK → recipes.id
step_number	    sequential number
description	    step instruction

interactions.csv:
column	        description
id	            event ID
user_id	        FK → users.id
recipe_id	    FK → recipes.id
type	        view/like/cook
timestamp	    event timestamp
rating	        optional numeric rating
difficulty_used	optional difficulty

## Result

The ETL pipeline produces:
    Clean, fully normalized CSVs
    Consistent column definitions
    Flattened nested arrays
    Validated and ready-for-analytics output

This completes Step 3 of the pipeline.
