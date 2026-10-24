from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import os, json, urllib.request, urllib.error

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = str(UPLOAD_DIR)

FOODS = {
    'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4.4, 'note': 'A source of fiber and vitamin C.'},
    'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'fiber': 3.1, 'note': 'Provides carbohydrates and potassium.'},
    'rice': {'calories': 205, 'protein': 4.3, 'carbs': 45, 'fat': 0.4, 'fiber': 0.6, 'note': 'Mostly carbohydrates; pair with protein and vegetables for a balanced meal.'},
    'dal': {'calories': 180, 'protein': 11, 'carbs': 27, 'fat': 3.5, 'fiber': 8, 'note': 'A useful plant-protein and fiber source; values vary by recipe and serving.'},
    'roti': {'calories': 120, 'protein': 3.5, 'carbs': 22, 'fat': 2.5, 'fiber': 3, 'note': 'Provides carbohydrates and some fiber.'},
    'salad': {'calories': 80, 'protein': 2, 'carbs': 15, 'fat': 1, 'fiber': 4, 'note': 'Can add fiber and micronutrients; dressing changes the estimate.'},
    'pizza': {'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'fiber': 2.5, 'note': 'Nutrition varies substantially with size, toppings and crust.'},
    'egg': {'calories': 78, 'protein': 6.3, 'carbs': 0.6, 'fat': 5.3, 'fiber': 0, 'note': 'Provides protein and fat.'},
    'paneer': {'calories': 265, 'protein': 18, 'carbs': 3.5, 'fat': 20, 'fiber': 0, 'note': 'Protein and fat vary by paneer type and preparation.'},
    'unknown': {'calories': 200, 'protein': 6, 'carbs': 28, 'fat': 7, 'fiber': 3, 'note': 'Generic placeholder estimate. Select the closest food for a more useful estimate.'}
}

RECIPES = {
    'quick': {'title':'Quick Vegetable Poha', 'time':'15 min', 'ingredients':['1 cup poha','½ onion, chopped','Peas or peanuts (optional)','Mustard seeds, turmeric and lemon','1 tsp oil'], 'steps':['Rinse poha briefly and drain.','Temper mustard seeds and sauté onion with turmeric.','Add peas or peanuts, then poha and salt; heat through.','Finish with lemon. Serve hot.']},
    'protein': {'title':'Simple Dal & Rice Bowl', 'time':'25 min', 'ingredients':['¾ cup cooked dal','1 cup cooked rice','Cumin, garlic and tomato','Seasonal vegetables (optional)'], 'steps':['Warm dal with a cumin-garlic tempering.','Add tomato and simmer until soft.','Serve with rice and a side of cooked vegetables.','Adjust seasoning and portion to appetite.']},
    'snack': {'title':'Yogurt Fruit Bowl', 'time':'5 min', 'ingredients':['1 cup plain yogurt','1 fruit, chopped','A small handful of nuts or seeds (optional)'], 'steps':['Wash and chop the fruit.','Add fruit to yogurt.','Top with nuts or seeds if suitable for you.']}
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def call_llm(prompt):
    """Optional OpenAI-compatible API call. Falls back to transparent local demo logic."""
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        return None
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    payload = {'model': model, 'messages': [
        {'role':'system','content':'You are Food Verse AI, a cautious food education assistant. Avoid diagnosing illness or certifying food safety. State uncertainty. Keep answers practical and concise.'},
        {'role':'user','content':prompt}
    ], 'temperature':0.5}
    req = urllib.request.Request('https://api.openai.com/v1/chat/completions', data=json.dumps(payload).encode(), headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode())
            return data['choices'][0]['message']['content'].strip()
    except Exception:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status':'ok','app':'Food Verse AI','mode':'live-llm' if os.getenv('OPENAI_API_KEY') else 'demo','llm_enabled':bool(os.getenv('OPENAI_API_KEY'))})

@app.route('/api/analyze-food', methods=['POST'])
def analyze_food():
    food = request.form.get('food', 'unknown').lower().strip()
    serving = max(0.25, min(float(request.form.get('servings', '1') or 1), 10))
    if food not in FOODS: food = 'unknown'
    image = request.files.get('image')
    image_saved = False
    if image and image.filename and allowed_file(image.filename):
        safe = secure_filename(image.filename)
        # Prefix prevents accidental overwrite and avoids trusting the supplied path.
        from uuid import uuid4
        saved = f'{uuid4().hex[:10]}_{safe}'
        image.save(UPLOAD_DIR / saved)
        image_saved = True
    info = FOODS[food]
    return jsonify({'food':food.title(),'servings':serving,'nutrition':{k:round(v*serving,1) for k,v in info.items() if isinstance(v,(int,float))},'note':info['note'],'image_received':image_saved,'mode':'demo-estimate','disclaimer':'Estimates are approximate and based on the selected food and serving size, not validated image recognition. Recipes, portion sizes and ingredients change actual values.'})

@app.route('/api/freshness', methods=['POST'])
def freshness():
    food = request.json.get('food','produce') if request.is_json else 'produce'
    signs = request.json.get('signs',[]) if request.is_json else []
    concerns = {'mold':'Visible mold selected','slime':'Slimy surface selected','odor':'Unusual odor selected','damaged':'Significant damage selected'}
    selected = [concerns[s] for s in signs if s in concerns]
    if selected:
        level, message = 'caution', 'One or more warning signs were reported. Do not taste the food to test it; when in doubt, discard it.'
    else:
        level, message = 'uncertain', 'No listed warning signs were selected, but this does not prove the food is safe. Appearance alone cannot reliably rule out harmful microbes.'
    return jsonify({'food':food,'level':level,'message':message,'observations':selected,'disclaimer':'Preliminary checklist only. Follow official food storage guidance; do not rely on this tool to certify safety.'})

@app.route('/api/hygiene', methods=['POST'])
def hygiene():
    data = request.get_json(force=True)
    checks = data.get('checks',{})
    labels = {'handwashing':'Handwashing practice','surface':'Food-contact surfaces cleaned','separation':'Raw and ready-to-eat foods separated','temperature':'Safe storage/cooking temperature checked','pest':'No visible pest activity','waste':'Waste handled appropriately'}
    passed = [labels[k] for k,v in checks.items() if k in labels and v]
    missing = [labels[k] for k in labels if not checks.get(k)]
    score = round(100*len(passed)/len(labels))
    return jsonify({'score':score,'passed':passed,'attention':missing,'message':'Checklist completion score only; this is not a formal inspection, certification or proof of restaurant hygiene. Verify conditions in person.'})

@app.route('/api/cooking', methods=['POST'])
def cooking():
    data = request.get_json(force=True)
    ingredients = ', '.join(data.get('ingredients',[])[:20]) or 'basic pantry ingredients'
    preference = data.get('preference','quick')
    prompt = f'Suggest one practical home recipe using these ingredients: {ingredients}. Dietary preference: {preference}. Give title, estimated time, ingredients and numbered steps. Ask the user to verify allergies and cook foods to safe temperatures.'
    ai = call_llm(prompt)
    if ai:
        return jsonify({'answer':ai,'mode':'live-llm'})
    recipe = RECIPES.get(preference, RECIPES['quick'])
    return jsonify({'answer':f"{recipe['title']} ({recipe['time']})\n\nIngredients:\n"+'\n'.join('• '+x for x in recipe['ingredients'])+'\n\nMethod:\n'+'\n'.join(f'{i+1}. {x}' for i,x in enumerate(recipe['steps']))+'\n\nCheck allergens and cook ingredients thoroughly.','mode':'demo','note':'Add OPENAI_API_KEY in .env to enable optional LLM responses.'})

@app.route('/api/meal-plan', methods=['POST'])
def meal_plan():
    data = request.get_json(force=True)
    diet = data.get('diet','balanced')
    budget = data.get('budget','moderate')
    avoid = data.get('avoid','').strip()
    prompt = f'Create a one-day general meal-planning example for dietary preference {diet}, budget {budget}, foods to avoid: {avoid or "none specified"}. Give breakfast, lunch, snack, dinner and simple swaps. Do not claim to treat medical conditions; advise users with medical dietary needs to consult a qualified professional.'
    ai = call_llm(prompt)
    if ai:
        return jsonify({'plan':ai,'mode':'live-llm'})
    plan = {'balanced':[('Breakfast','Poha with peanuts and fruit'),('Lunch','Dal, rice or roti, and cooked vegetables'),('Snack','Yogurt or roasted chana'),('Dinner','Roti with paneer or dal and vegetables')], 'vegetarian':[('Breakfast','Besan chilla with yogurt'),('Lunch','Rajma or chole with rice and salad'),('Snack','Fruit and roasted chana'),('Dinner','Dal, roti and seasonal vegetables')], 'high-protein':[('Breakfast','Besan chilla or eggs, as suitable'),('Lunch','Dal plus paneer/tofu/eggs with rice or roti'),('Snack','Yogurt or roasted chana'),('Dinner','Beans/lentils with vegetables and a grain') ]}
    rows = plan.get(diet, plan['balanced'])
    if avoid:
        rows = [(meal, dish+' (adjust ingredients to avoid: '+avoid+')') for meal,dish in rows]
    return jsonify({'plan':'One-day example (adjust portions to appetite and needs):\n\n'+'\n'.join(f'{a}: {b}' for a,b in rows)+f'\n\nBudget preference: {budget}.\n\nThis is general information, not a personalized medical diet.','mode':'demo','note':'Add OPENAI_API_KEY in .env to enable optional LLM-generated plans.'})

@app.errorhandler(413)
def too_large(_):
    return jsonify({'error':'Image too large. Please upload an image under 8 MB.'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','5000')), debug=True)
