#!/usr/bin/env python3
"""
Dante's Item Forge - Local App
Find the best items in any game optimized for damage, value, speed, etc.
"""

import http.server
import json
import urllib.request
import urllib.error
import os
import threading
import sys
import webview

PORT = 7842
CONFIG_FILE = "config.json"

def load_saved_key():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f).get("api_key", "")
        except:
            pass
    return os.environ.get("GROQ_API_KEY", "")

def save_key_locally(key):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"api_key": key}, f)
    except:
        pass

API_KEY = load_saved_key()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dante's Item Forge</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0f0f13;
    --surface: #18181f;
    --surface2: #22222c;
    --border: #2e2e3a;
    --accent: #f55036;
    --accent-dim: #4a1d15;
    --text: #e8e6f0;
    --muted: #8b8a9b;
    --gold: #f0b429;
    --silver: #a0aec0;
    --bronze: #cd7f32;
    --success: #48bb78;
    --radius: 10px;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; min-height: 100vh; padding: 2rem 1rem; }
  .container { max-width: 780px; margin: 0 auto; }
  header { display: flex; align-items: center; gap: 14px; margin-bottom: 2rem; }
  .logo { width: 44px; height: 44px; background: var(--accent-dim); border-radius: var(--radius); display: flex; align-items: center; justify-content: center; font-size: 22px; }
  h1 { font-size: 22px; font-weight: 600; }
  h1 span { color: var(--accent); }
  .subtitle { font-size: 13px; color: var(--muted); margin-top: 2px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; margin-bottom: 1rem; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .field { margin-bottom: 14px; }
  .field label { display: block; font-size: 12px; color: var(--muted); margin-bottom: 6px; letter-spacing: 0.04em; text-transform: uppercase; }
  input, select { width: 100%; background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: 14px; padding: 9px 12px; outline: none; transition: border-color 0.15s; }
  input:focus, select:focus { border-color: var(--accent); }
  input::placeholder { color: var(--muted); }
  select option { background: var(--surface2); }
  #apiKey { font-family: monospace; letter-spacing: 0.05em; }
  .api-note { font-size: 11px; color: var(--muted); margin-top: 5px; }
  .api-note a { color: var(--accent); text-decoration: none; }
  .btn { width: 100%; padding: 11px; background: var(--accent); color: #fff; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: opacity 0.15s, transform 0.1s; margin-top: 6px; }
  .btn:hover { opacity: 0.9; }
  .btn:active { transform: scale(0.99); }
  .btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .status { display: none; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.25rem; margin-bottom: 1rem; font-size: 13px; color: var(--muted); display: flex; align-items: center; gap: 10px; }
  .status.hidden { display: none; }
  .spinner { width: 16px; height: 16px; border: 2px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .results { display: none; }
  .result-header { font-size: 12px; color: var(--muted); margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
  .item-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.1rem 1.25rem; margin-bottom: 10px; transition: border-color 0.15s; }
  .item-card.top { border-color: var(--accent); }
  .item-card:hover { border-color: #3e3e52; }
  .item-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
  .item-left { display: flex; align-items: center; gap: 10px; }
  .rank { font-size: 13px; font-weight: 700; min-width: 22px; }
  .rank.gold { color: var(--gold); }
  .rank.silver { color: var(--silver); }
  .rank.bronze { color: var(--bronze); }
  .rank.other { color: var(--muted); }
  .item-name { font-size: 15px; font-weight: 600; }
  .item-type { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .badge { font-size: 11px; padding: 3px 10px; background: var(--accent-dim); color: var(--accent); border-radius: 6px; font-weight: 600; white-space: nowrap; }
  .stats-box { background: var(--surface2); border-radius: 8px; padding: 8px 12px; margin-bottom: 10px; font-size: 13px; font-weight: 500; color: var(--text); }
  .item-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 12px; margin-bottom: 10px; }
  .item-meta span { color: var(--muted); }
  .item-pros { font-size: 13px; color: var(--text); margin-bottom: 4px; }
  .item-cons { font-size: 12px; color: var(--muted); font-style: italic; }
  .honorable { font-size: 12px; color: var(--muted); margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); }
  .honorable strong { color: var(--text); }
  .tip-box { border-left: 2px solid var(--accent); padding: 8px 12px; margin-top: 14px; font-size: 13px; color: var(--muted); }
  .tip-box strong { color: var(--accent); }
  .error { background: #2a1515; border: 1px solid #5a2020; color: #f87171; border-radius: var(--radius); padding: 1rem; font-size: 13px; margin-bottom: 1rem; display: none; }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo">🗡️</div>
    <div>
      <h1>Dante's <span>Item Forge</span></h1>
      <p class="subtitle">Find the best weapon, armor, or item in any game</p>
    </div>
  </header>
  <div class="card">
    <div class="field">
      <label>Groq API Key</label>
      <input type="password" id="apiKey" placeholder="gsk_..." value="" />
      <p class="api-note">Get a free key at <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a> — saved locally for next time</p>
    </div>
  </div>
  <div class="card">
    <div class="grid-2">
      <div class="field">
        <label>Game name</label>
        <input type="text" id="game" placeholder="e.g. Elden Ring, OSRS, LoL..." />
      </div>
      <div class="field">
        <label>Item type</label>
        <select id="itemType">
          <option value="weapon">Weapon</option>
          <option value="armor">Armor</option>
          <option value="accessory">Accessory / Ring</option>
          <option value="consumable">Consumable / Potion</option>
          <option value="any">Any item</option>
        </select>
      </div>
    </div>
    <div class="grid-2">
      <div class="field">
        <label>Optimize for</label>
        <select id="stat">
          <option value="damage">Highest damage / DPS</option>
          <option value="defense">Highest defense / mitigation</option>
          <option value="value">Best value for cost</option>
          <option value="speed">Fastest attack speed</option>
          <option value="utility">Most utility / effects</option>
          <option value="early">Best early game</option>
          <option value="endgame">Best endgame / BiS</option>
        </select>
      </div>
      <div class="field">
        <label>Budget / constraint (optional)</label>
        <input type="text" id="budget" placeholder="e.g. under 50k gold, F2P only..." />
      </div>
    </div>
    <div class="field">
      <label>Extra context (optional)</label>
      <input type="text" id="extra" placeholder="e.g. melee build, no DLC, level 60 cap..." />
    </div>
    <button class="btn" id="searchBtn" onclick="runSearch()">⚔ Find Best Items</button>
  </div>
  <div class="error" id="errorBox"></div>
  <div class="status hidden" id="status">
    <div class="spinner"></div>
    <span id="statusText">Forging database query...</span>
  </div>
  <div class="results" id="results"></div>
</div>
<script>
const statLabels = {
  damage: 'highest damage / DPS',
  defense: 'highest defense / mitigation',
  value: 'best value for cost',
  speed: 'fastest attack speed',
  utility: 'most utility / effects',
  early: 'best early game option',
  endgame: 'best endgame / BiS'
};

async function runSearch() {
  const apiKey = document.getElementById('apiKey').value.trim();
  const game = document.getElementById('game').value.trim();
  const itemType = document.getElementById('itemType').value;
  const stat = document.getElementById('stat').value;
  const budget = document.getElementById('budget').value.trim();
  const extra = document.getElementById('extra').value.trim();
  const errorBox = document.getElementById('errorBox');
  errorBox.style.display = 'none';

  if (!apiKey) { showError('Please enter your Groq API key.'); return; }
  if (!game) { showError('Please enter a game name.'); document.getElementById('game').focus(); return; }

  const btn = document.getElementById('searchBtn');
  btn.disabled = true;
  btn.textContent = 'Searching...';
  const statusEl = document.getElementById('status');
  const resultsEl = document.getElementById('results');
  statusEl.classList.remove('hidden');
  resultsEl.style.display = 'none';

  const budgetLine = budget ? `\\nBudget: ${budget}` : '';
  const extraLine = extra ? `\\nContext: ${extra}` : '';

  const prompt = `User asks about game: "${game}". First, verify if it is a real video game. If not, return JSON: {"error": "Invalid game"}. If valid, find top 3-5 ${itemType} optimized for ${statLabels[stat]}.${budgetLine}${extraLine}. Return ONLY JSON: {"game":"name", "query":"desc", "topPicks":[{"rank":1, "name":"name", "type":"type", "keyStats":"stats", "cost":"cost", "pros":"pros", "cons":"cons", "bestFor":"build"}], "honorableMentions":[], "tip":"tip"}`;

  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ apiKey, prompt })
    });
    const data = await response.json();
    if (data.error) { showError(data.error); return; }
    let parsed;
    try {
      const clean = data.text.replace(/```json|```/g, '').trim();
      parsed = JSON.parse(clean);
    } catch(e) {
      const match = data.text.match(/\\{[\\s\\S]*\\}/);
      if (match) parsed = JSON.parse(match[0]);
      else throw new Error('Parsing error');
    }
    if (parsed.error) { showError(parsed.error); return; }
    statusEl.classList.add('hidden');
    renderResults(parsed);
  } catch(err) {
    showError('Error: ' + err.message);
  }
  btn.disabled = false;
  btn.textContent = '⚔ Find Best Items';
}

function showError(msg) {
  const eb = document.getElementById('errorBox');
  eb.textContent = msg;
  eb.style.display = 'block';
  document.getElementById('status').classList.add('hidden');
  document.getElementById('searchBtn').disabled = false;
}

function renderResults(data) {
  const el = document.getElementById('results');
  el.style.display = 'block';
  const rc = ['gold', 'silver', 'bronze', 'other', 'other'];
  let html = `<div class="result-header">Results for: ${data.game}</div>`;
  (data.topPicks || []).forEach((item, i) => {
    html += `<div class="item-card ${i===0?'top':''}">
      <div class="item-top"><div class="item-left"><span class="rank ${rc[i]}">#${i+1}</span>
      <div><div class="item-name">${item.name}</div><div class="item-type">${item.type}</div></div></div></div>
      <div class="stats-box">${item.keyStats}</div>
      <div class="item-meta"><div><span>Cost: </span>${item.cost}</div><div><span>Best for: </span>${item.bestFor}</div></div>
      <div class="item-pros">${item.pros}</div><div class="item-cons">Note: ${item.cons}</div></div>`;
  });
  if (data.tip) html += `<div class="tip-box"><strong>Tip:</strong> ${data.tip}</div>`;
  el.innerHTML = html;
  el.scrollIntoView({ behavior: 'smooth' });
}

function escHtml(str) { return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

window.addEventListener('DOMContentLoaded', () => {
  const key = document.getElementById('apiKey');
  if (window.__API_KEY__) key.value = window.__API_KEY__;
});
</script>
</body>
</html>
""".replace("window.__API_KEY__", f"window.__API_KEY__ = '{API_KEY}'")

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path != "/api/search": return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        api_key = body.get("apiKey", "").strip()
        prompt = body.get("prompt", "")
        if not api_key: return

        save_key_locally(api_key)
        global API_KEY
        API_KEY = api_key

        try:
            payload = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }).encode()
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            self._json({"text": text})
        except Exception as e:
            self._json({"error": str(e)})

    def _json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

def main():
    def start_server():
        with http.server.HTTPServer(("127.0.0.1", PORT), Handler) as httpd:
            httpd.serve_forever()
    threading.Thread(target=start_server, daemon=True).start()
    webview.create_window("Dante's Item Forge", f'http://127.0.0.1:{PORT}', width=850, height=750)
    webview.start()

if __name__ == "__main__":
    main()
