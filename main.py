import os
import joblib
import pandas as pd
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify

# ==========================================
# 1. KONFIGURASI & HTML CONTENT
# ==========================================
TEMPLATE_FOLDER = 'templates'
HTML_FILE = 'index.html'
MODEL_PATH = 'model_forecast.pkl'

# Kode HTML Frontend (Tailwind + Lucide)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Retail Prediction</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --primary: #4f46e5; 
            --primary-hover: #4338ca;
            --bg-soft: #eef2ff;
        }
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        .input-field { transition: all 0.2s; }
        .input-field:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
    </style>
</head>
<body class="text-slate-800 min-h-screen flex items-center justify-center p-4">

    <div class="w-full max-w-4xl bg-white rounded-2xl shadow-xl overflow-hidden">
        
        <div class="bg-indigo-600 p-6 text-white flex items-center justify-between">
            <div class="flex items-center gap-3">
                <i data-lucide="cpu" class="w-8 h-8"></i>
                <div>
                    <h1 class="text-xl font-bold">Retail AI Forecaster</h1>
                    <p class="text-indigo-200 text-sm">Machine Learning Prediction System</p>
                </div>
            </div>
            <div class="hidden md:block text-indigo-200 text-xs uppercase tracking-widest font-semibold">V.1.0 ULTIMATE</div>
        </div>

        <div class="flex flex-col md:flex-row">
            
            <div class="w-full md:w-2/3 p-8">
                <form id="predictForm" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <div class="col-span-1 md:col-span-2 border-b pb-2 mb-2 border-slate-100 text-slate-400 text-xs font-bold uppercase tracking-wider">General Info</div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="calendar" class="w-3 h-3"></i> Month (1-24)
                        </label>
                        <input type="number" id="month" value="25" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium" required>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="cloud-sun" class="w-3 h-3"></i> Season
                        </label>
                        <select id="season" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium">
                            <option value="Winter">Winter</option>
                            <option value="Spring">Spring</option>
                            <option value="Summer">Summer</option>
                            <option value="Autumn">Autumn</option>
                        </select>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="tag" class="w-3 h-3"></i> Category
                        </label>
                        <select id="category" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium">
                            <option value="Smartphone">Smartphone</option>
                            <option value="Laptop">Laptop</option>
                            <option value="Fashion">Fashion</option>
                            <option value="Home_IoT">Home IoT</option>
                        </select>
                    </div>

                    <div class="col-span-1 md:col-span-2 border-b pb-2 mb-2 mt-4 border-slate-100 text-slate-400 text-xs font-bold uppercase tracking-wider">Pricing & Competition</div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="dollar-sign" class="w-3 h-3"></i> My Price ($)
                        </label>
                        <input type="number" id="price" step="0.01" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium" required>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="users" class="w-3 h-3"></i> Competitor ($)
                        </label>
                        <input type="number" id="competitor_price" step="0.01" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium" required>
                    </div>

                    <div class="col-span-1 md:col-span-2 border-b pb-2 mb-2 mt-4 border-slate-100 text-slate-400 text-xs font-bold uppercase tracking-wider">Metrics & Quality</div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="activity" class="w-3 h-3"></i> Tech Score (1-100)
                        </label>
                        <input type="number" id="tech_score" max="100" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium">
                    </div>
                    
                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="trending-up" class="w-3 h-3"></i> Social Hype (0-100)
                        </label>
                        <input type="range" id="social_hype" min="0" max="100" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                        <div class="text-xs text-right text-indigo-600 font-bold" id="hype_val">50</div>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="history" class="w-3 h-3"></i> Prev. Sales (Unit)
                        </label>
                        <input type="number" id="prev_sales" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium">
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-semibold text-slate-500 flex items-center gap-2">
                            <i data-lucide="megaphone" class="w-3 h-3"></i> Ad Spend ($)
                        </label>
                        <input type="number" id="ad_spend" class="input-field w-full p-3 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium">
                    </div>

                    <div class="col-span-1 md:col-span-2 mt-6">
                        <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-indigo-200 transition-all flex justify-center items-center gap-2">
                            <i data-lucide="sparkles" class="w-4 h-4"></i> Calculate Prediction
                        </button>
                    </div>
                </form>
            </div>

            <div class="w-full md:w-1/3 bg-slate-50 border-l border-slate-100 p-8 flex flex-col justify-center items-center text-center relative">
                
                <div id="empty-state" class="opacity-100 transition-opacity duration-300">
                    <div class="bg-white p-4 rounded-full inline-block shadow-sm mb-4">
                        <i data-lucide="bar-chart-2" class="w-8 h-8 text-slate-300"></i>
                    </div>
                    <h3 class="text-slate-400 font-medium text-sm">Ready to Process</h3>
                    <p class="text-slate-300 text-xs mt-1">Enter data to see prediction</p>
                </div>

                <div id="result-state" class="hidden opacity-0 transition-opacity duration-500 transform translate-y-4">
                    <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Forecast Result</p>
                    <div class="text-6xl font-black text-indigo-600 mb-2" id="pred-value">0</div>
                    <p class="text-slate-500 text-sm font-medium">Units Sold</p>
                    
                    <div class="mt-8 w-full bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-left">
                        <div class="flex items-center gap-2 text-xs text-emerald-600 font-bold mb-1">
                            <i data-lucide="check-circle" class="w-3 h-3"></i> Analysis Complete
                        </div>
                        <p class="text-slate-400 text-xs leading-relaxed">
                            Based on market patterns, competition, and seasonality logic.
                        </p>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
        const slider = document.getElementById('social_hype');
        const output = document.getElementById('hype_val');
        slider.oninput = function() { output.innerHTML = this.value; }

        document.getElementById('predictForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const btn = this.querySelector('button');
            const originalText = btn.innerHTML;
            btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Processing...`;
            lucide.createIcons();
            btn.disabled = true;

            const data = {
                month: document.getElementById('month').value,
                category: document.getElementById('category').value,
                season: document.getElementById('season').value,
                price: document.getElementById('price').value,
                competitor_price: document.getElementById('competitor_price').value,
                tech_score: document.getElementById('tech_score').value,
                social_hype: document.getElementById('social_hype').value,
                prev_sales: document.getElementById('prev_sales').value,
                ad_spend: document.getElementById('ad_spend').value
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                document.getElementById('empty-state').classList.add('hidden');
                const resDiv = document.getElementById('result-state');
                resDiv.classList.remove('hidden');
                setTimeout(() => {
                    resDiv.classList.remove('opacity-0', 'translate-y-4');
                    document.getElementById('pred-value').innerText = result.prediction;
                }, 100);
            } catch (error) {
                alert("Error: " + error);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
                lucide.createIcons();
            }
        });
    </script>
</body>
</html>
"""

# ==========================================
# 2. SETUP SYSTEM (AUTO-GENERATE FILES)
# ==========================================
def setup_environment():
    # Buat folder templates jika belum ada
    if not os.path.exists(TEMPLATE_FOLDER):
        os.makedirs(TEMPLATE_FOLDER)
        print(f"📂 Folder '{TEMPLATE_FOLDER}' berhasil dibuat.")
    
    # Tulis file HTML
    file_path = os.path.join(TEMPLATE_FOLDER, HTML_FILE)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f"📄 File '{file_path}' berhasil dibuat/diupdate.")

# ==========================================
# 3. FLASK BACKEND LOGIC
# ==========================================
app = Flask(__name__)

# Load Model
model = None
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model '{MODEL_PATH}' berhasil dimuat. Web siap!")
except FileNotFoundError:
    print(f"⚠️ PERINGATAN: File '{MODEL_PATH}' tidak ditemukan.")
    print("   Jalankan script generator model terlebih dahulu.")

@app.route('/')
def home():
    return render_template(HTML_FILE)

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model belum dimuat. Cek server log.'}), 500

    try:
        data = request.json
        # Input data sesuai urutan training
        input_df = pd.DataFrame({
            'Month': [int(data['month'])],
            'Category': [data['category']],
            'Season': [data['season']],
            'Price': [float(data['price'])],
            'Competitor_Price': [float(data['competitor_price'])],
            'Tech_Score': [float(data['tech_score'])],
            'Social_Hype': [float(data['social_hype'])],
            'Prev_Sales': [float(data['prev_sales'])],
            'Ad_Spend': [float(data['ad_spend'])]
        })

        prediction = model.predict(input_df)
        result = int(prediction[0])
        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

# ==========================================
# 4. RUN APP
# ==========================================
if __name__ == '__main__':
    setup_environment()
    
    # Timer untuk membuka browser otomatis setelah 1 detik
    if model:
        Timer(1, open_browser).start()
        app.run(debug=True, use_reloader=False)
    else:
        print("❌ Gagal memulai server karena model tidak ditemukan.")
