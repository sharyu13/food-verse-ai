# Food Verse AI — Project Summary

## Problem statement
Food decisions are often fragmented: nutrition estimates are manual, freshness observations are uncertain, hygiene practices are inconsistently tracked, and cooking support may not adapt to available ingredients. This project demonstrates a unified web workspace for food-related decision support.

## Objectives
- Provide approximate nutrition information based on food selection and portion size.
- Structure freshness observations using a cautious checklist.
- Help users self-review everyday kitchen hygiene practices.
- Suggest cooking ideas from available ingredients.
- Produce general meal-plan examples from preferences and exclusions.
- Make limitations visible to encourage responsible use.

## Architecture
- **Presentation layer:** React UI rendered in the browser, JavaScript interactions and responsive CSS animations.
- **Application layer:** Python Flask routes validate inputs and coordinate module logic.
- **Data layer:** Small in-code demo nutrition dataset and recipe templates; no database is required for the prototype.
- **Optional LLM integration:** OpenAI-compatible chat completions for recipe and meal-plan text when configured with a server-side environment variable.

## Current implementation vs future work
Implemented: responsive interface, nutrition estimate endpoint, image upload/preview, freshness checklist, hygiene checklist score, demo recipe suggestions, demo meal plans, health endpoint and optional LLM text generation.

Future work: integrate a real food image classification model, use a trusted nutrition database, add calibrated portion estimation, validate freshness approaches with domain experts, build role-based restaurant inspection workflows, add user accounts and persistence, and conduct usability and safety evaluations.

## Limitations and ethics
The prototype does not perform validated visual food recognition, laboratory freshness detection or official hygiene inspections. Nutrition values are illustrative estimates. A lack of visible warning signs does not establish food safety. Meal plans are general examples and are not medical advice. Any real deployment should be reviewed by relevant food-safety and nutrition experts.
