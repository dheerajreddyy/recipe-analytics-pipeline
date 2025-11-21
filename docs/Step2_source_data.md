## STEP 2 — Firebase Source Data Setup

## Overview:
This step inserts all required source data directly into Firebase Firestore.

The dataset includes:
    The candidate’s primary recipe
    15 synthetic recipes
    10 synthetic users

User interactions:
    views
    likes
    cook attempts

All records are inserted programmatically using the Firebase Admin SDK.

## Objectives:
    Connect Python to Firebase using a service account key
    Insert the primary recipe into the recipes collection
    Generate and insert synthetic recipes
    Generate and insert users
    Generate and insert interactions
    Ensure Firestore contains clean, structured source data for ETL

## Prerequisites:
    Firebase project created
    Service Account Key downloaded
    File placed at:
        de_recipe_pipeline/serviceAccountKey.json


Install dependencies:
    pip install firebase-admin

All data is populated using the script:
    scripts/upload_to_firestore.py

This script:
    Initializes Firebase Admin
    Inserts the candidate’s recipe
    Generates 15 synthetic recipes
    Generates 10 users
    Creates user interactions
    Saves each record into Firestore

## How to Run the Script

Run the script from the project root:
    python scripts/upload_to_firestore.py


## Expected output:

Inserted primary recipe.
Inserted synthetic recipes.
Inserted users.
Inserted user interactions.
Firestore data setup completed.

## Result:
After execution, Firestore contains three collections:

recipes/         → Primary + synthetic recipes
users/           → Synthetic users
interactions/    → User views, likes, and cook attempts


This completes the required Firestore source data setup.