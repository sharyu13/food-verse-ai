# Food Verse AI

**A multimodule food-intelligence academic prototype** built with React (CDN), JavaScript, CSS animations, Python and Flask.

## Modules

1. **Nutrition insights** — approximate macro/calorie estimates from a manually selected food type and serving size; supports optional image upload/preview.
2. **Freshness checklist** — records visible warning signs and returns cautious guidance. It does not certify food safety.
3. **Kitchen hygiene checklist** — tracks self-reported practices and displays a checklist completion score, not an official inspection score.
4. **Smart cooking assistant** — creates a recipe suggestion from ingredients. Includes offline demo recipes.
5. **Meal planner** — creates a general one-day example based on preferences, budget and exclusions.
6. **Responsible AI notes** — explains the prototype's limitations and uncertainty.

## Important scope note

This repository is a working **academic prototype**, not a validated food-safety product. In the default configuration, food photos are uploaded and previewed but are **not analysed by a computer-vision model**. Nutrition is based on the user's selected food type. Freshness and hygiene results are checklist-based. The recipe and meal-plan modules use built-in demo logic unless an API key is configured. Do not use the app to determine whether food is safe, diagnose health conditions or replace qualified advice.

## Requirements

- Python 3.8+ (Python 3.10+ recommended)
- Internet connection for the React/Babel/font CDN resources used by the web page
- Git (for GitHub upload)

## Run locally on Windows

1. Extract this folder.
2. Open the `food_verse_ai` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment (recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `py -m pip install -r requirements.txt` without activating, or use Command Prompt activation: `.venv\Scripts\activate.bat`.

5. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   py app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

If `py` is unavailable, try `python` instead. If Python is not installed, install it from https://www.python.org/downloads/ and enable **Add Python to PATH** during setup.

## Optional live LLM mode

The project works without a key. To enable live recipe and meal-plan generation:

1. Copy `.env.example` to `.env`.
2. Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`.
3. Set the environment variables in your terminal before starting the app. The sample `.env` is provided for reference; the app does not automatically load `.env` files. Never publish your API key to GitHub.

PowerShell example for the current terminal:

```powershell
$env:OPENAI_API_KEY="your-key-here"
$env:OPENAI_MODEL="gpt-4o-mini"
py app.py
```

API keys may incur charges. Do not add a real key to source code or commit it.

## API routes

- `GET /api/health`
- `POST /api/analyze-food` — multipart form: `food`, `servings`, optional `image`
- `POST /api/freshness` — JSON: `food`, `signs`
- `POST /api/hygiene` — JSON: `checks`
- `POST /api/cooking` — JSON: `ingredients`, `preference`
- `POST /api/meal-plan` — JSON: `diet`, `budget`, `avoid`

## GitHub upload

Create an empty repository on GitHub, for example `food-verse-ai`. From this folder, run:

```bash
git init
git add .
git commit -m "Build Food Verse AI academic prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/food-verse-ai.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not commit `.env`, secrets or private data.

## Demo link / deployment

A GitHub repository link is not a live demo link. For a public demo, deploy this Flask app to a Python-compatible host (for example Render) using build command `pip install -r requirements.txt` and start command `python app.py`. A `render.yaml` blueprint is included. In Render, create a new Blueprint from your GitHub repository or create a Web Service with build command `pip install -r requirements.txt` and start command `gunicorn app:app --bind 0.0.0.0:$PORT`. Add the resulting public URL to the course portal only after checking that it opens. Free hosting availability and sleep limits can change.

## Academic evaluation suggestions

- Test nutrition estimates for each included food and multiple serving sizes.
- Test freshness checklist outputs with each warning sign independently and in combination.
- Test all possible hygiene checklist combinations and verify the score.
- Test recipe generation with blank ingredients, familiar ingredients and unusual combinations.
- Test mobile and desktop layouts.
- Document that checklist completion is not the same as scientific validation.

## License

Educational use. Review any third-party service terms before deploying publicly.
