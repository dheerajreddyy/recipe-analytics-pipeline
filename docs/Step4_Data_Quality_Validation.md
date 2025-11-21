## STEP 4 — Data Quality Validation

## Overview:
This step validates the normalized CSV output produced by the ETL pipeline.
The goal is to ensure that the data is complete, consistent, and adheres to the defined schema.
Validation is performed using a Python script that checks required fields, numeric constraints, allowed values, and the structure of arrays that were flattened during transformation.

## Validation Scope:

The following files are validated:
    data/processed/recipes.csv
    data/processed/ingredients.csv
    data/processed/steps.csv
    data/processed/interactions.csv

Each file corresponds to a normalized table in the project.

## Validation Rules:

Recipes:

    id and title must be present
    servings must be > 0
    prep_time_min, cook_time_min, total_time_min must be ≥ 0
    difficulty must be one of: easy, medium, hard
    created_at must be present

Ingredients:
    recipe_id, ingredient_id, name must be present
    quantity must be ≥ 0
    unit must be present

Steps:
    recipe_id must be present
    step_number must be ≥ 1
    description must be present

Interactions:
    id, user_id, recipe_id, timestamp must be present
    type must be one of: view, like, cook
    rating (if present) must be an integer between 1 and 5
    difficulty_used (if present) must be easy, medium, or hard

## Validation Script:
The script used for validation is:
    scripts/validate_data.py

It performs the following tasks:
    Loads all processed CSV files
    Applies rule-based validation checks
    Aggregates valid and invalid records
    Outputs a structured JSON report

## Execution Command:
Run the validator from the project root:
    python scripts/validate_data.py

## Output:

A validation report is generated at:
    outputs/validation_report.json


This report contains:
    Count of valid rows
    List of invalid records with error messages
    Validation breakdown per table

Example Output:
{
  "recipes": {
    "valid": 16,
    "invalid": []
  },
  "ingredients": {
    "valid": 85,
    "invalid": []
  },
  "steps": {
    "valid": 60,
    "invalid": []
  },
  "interactions": {
    "valid": 145,
    "invalid": []
  }
}

## Invalid Records with Reasons:

For any row that fails validation, the validator script records:
    the full record
    an array of error messages explaining why the record is invalid

These appear inside the JSON report like:
"ingredients": {
  "valid": 82,
  "invalid": [
    {
      "record": {
        "recipe_id": "",
        "ingredient_id": "recipe_1_ing_1",
        "name": "",
        "quantity": -1,
        "unit": ""
      },
      "errors": [
        "missing recipe_id",
        "missing name",
        "quantity must be >= 0",
        "missing unit"
      ]
    }
  ]
}

This provides:
    full traceability
    clear error causes
    useful debugging guidance
    compliance with assignment requirements

## Result:
All datasets passed validation and contain no schema inconsistencies.
This confirms that the ETL pipeline produced clean, normalized, and high-quality data suitable for analytics.