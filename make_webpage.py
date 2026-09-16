import json
import os

def build_html():
    shades = []
    shades_file = '/home/apv/projects/shadebook/data/shades.jsonl'
    if not os.path.exists(shades_file):
        print("Shades file not found.")
        return

    with open(shades_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    s = json.loads(line.strip())
                    if s.get('hex'):
                        shades.append(s)
                except:
                    pass

    print(f"Loaded {len(shades)} valid shades.")

    shades.sort(key=lambda x: (x.get('family', 'Other'), x.get('code', ''), x.get('name', '')))
    shades_json = json.dumps(shades)

    family_colors = {
        'all': 'conic-gradient(from 180deg, #ef4444, #f59e0b, #10b981, #06b6d4, #3b82f6, #8b5cf6, #ec4899, #ef4444)',
        'blue': '#2563eb',
        'brown': '#854d0e',
        'green': '#16a34a',
        'grey': '#64748b',
        'off-white': '#f1f5f9',
        'orange': '#ea580c',
        'pink': '#ec4899',
        'purple': '#9333ea',
        'red': '#dc2626',
        'white': '#ffffff',
        'yellow': '#eab308'
    }
    family_colors_json = json.dumps(family_colors)

    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Asian Paints Complete Shade Catalogue & Comparison Tool</title>
    <style>
        :root {
            --bg: #0b0f19;
            --surface: #151e2e;
            --surface-card: #1e293b;
            --surface-hover: #273549;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --border: #243248;
            --radius: 12px;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, system-ui, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }
        body {
            background: var(--bg);
            color: var(--text);
            padding-bottom: 70px;
            min-height: 100vh;
        }
        header {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(11, 15, 25, 0.95);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
            padding: 12px 16px;
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .brand-title {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .brand-badge {
            font-size: 0.72rem;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 2px 8px;
            border-radius: 999px;
            font-weight: 600;
        }
        .btn {
            background: var(--surface-card);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
        }
        .btn:hover {
            background: var(--surface-hover);
            border-color: var(--accent);
        }
        .btn-primary {
            background: var(--accent);
            color: #0b0f19;
            border-color: var(--accent);
        }
        .btn-primary:hover {
            background: var(--accent-hover);
        }
        .search-container {
            position: relative;
            width: 100%;
        }
        .search-input {
            width: 100%;
            padding: 11px 16px 11px 42px;
            font-size: 0.92rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            color: var(--text);
            outline: none;
            transition: all 0.2s;
        }
        .search-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        }
        .search-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }
        
        .filter-strip-wrapper {
            position: relative;
            width: 100%;
        }
        .filter-strip {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 4px 2px 6px 2px;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
        }
        .filter-strip::-webkit-scrollbar {
            display: none;
        }
        .color-chip {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 6px 12px 6px 8px;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
            user-select: none;
            flex-shrink: 0;
        }
        .color-chip:hover {
            background: var(--surface-card);
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-1px);
        }
        .color-chip.active {
            background: var(--surface-card);
            border-color: var(--accent);
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3), 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        .color-bubble {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.2);
            flex-shrink: 0;
        }
        .chip-count {
            font-size: 0.72rem;
            color: var(--text-muted);
            font-weight: 500;
            background: rgba(255, 255, 255, 0.08);
            padding: 1px 6px;
            border-radius: 999px;
        }

        main {
            max-width: 1400px;
            margin: 16px auto;
            padding: 0 16px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
            gap: 12px;
        }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
            cursor: pointer;
            position: relative;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.6);
            border-color: rgba(56, 189, 248, 0.4);
        }
        .swatch-box {
            height: 125px;
            width: 100%;
            position: relative;
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            padding: 8px;
        }
        .pin-btn {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            opacity: 0.85;
            transition: all 0.15s;
            z-index: 2;
        }
        .pin-btn:hover {
            opacity: 1;
            transform: scale(1.15);
        }
        .pin-btn.pinned {
            background: var(--accent);
            color: #0b0f19;
            border-color: var(--accent);
            opacity: 1;
        }
        .card-details {
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .shade-code {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text);
            letter-spacing: 0.02em;
        }
        .shade-name {
            font-size: 0.82rem;
            color: var(--text-muted);
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .meta-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 4px;
            padding-top: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 0.75rem;
        }
        .hex-code {
            font-family: ui-monospace, monospace;
            color: var(--accent);
            background: rgba(56, 189, 248, 0.08);
            padding: 2px 5px;
            border-radius: 4px;
        }
        .family-tag {
            color: var(--text-muted);
            text-transform: capitalize;
        }

        /* Fullscreen Shade Modal */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 500;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 24px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }
        .modal.active {
            opacity: 1;
            pointer-events: auto;
        }
        .modal-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
        }
        .close-btn {
            background: rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.4rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
        }
        .close-btn:hover {
            background: rgba(0, 0, 0, 0.7);
            transform: scale(1.1);
        }
        .modal-nav {
            display: flex;
            gap: 12px;
        }
        .nav-btn {
            background: rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
        }
        .nav-btn:hover {
            background: rgba(0, 0, 0, 0.7);
            transform: scale(1.1);
        }
        .modal-center {
            text-align: center;
            z-index: 10;
            padding: 20px;
        }
        .modal-code {
            font-size: 3.8rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.1;
            margin-bottom: 8px;
        }
        .modal-name {
            font-size: 2rem;
            font-weight: 600;
            opacity: 0.9;
            margin-bottom: 16px;
        }
        .modal-badges {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .modal-badge {
            background: rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 1rem;
            font-weight: 600;
            font-family: ui-monospace, monospace;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.15s;
        }
        .modal-badge:hover {
            background: rgba(0, 0, 0, 0.7);
            transform: scale(1.05);
        }
        .modal-bottom {
            display: flex;
            justify-content: center;
            gap: 14px;
            z-index: 10;
            flex-wrap: wrap;
        }
        .modal-action-btn {
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #fff;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.15s;
        }
        .modal-action-btn:hover {
            background: rgba(0, 0, 0, 0.8);
            transform: translateY(-2px);
        }

        /* Fullscreen Comparison View */
        .compare-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 600;
            background: var(--bg);
            display: flex;
            flex-direction: column;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }
        .compare-modal.active {
            opacity: 1;
            pointer-events: auto;
        }
        .compare-header {
            background: rgba(11, 15, 25, 0.96);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            z-index: 10;
        }
        .compare-title {
            font-size: 1.1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .compare-columns {
            flex: 1;
            display: flex;
            height: 100%;
            overflow-x: auto;
        }
        .compare-col {
            flex: 1;
            min-width: 150px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
            position: relative;
            transition: all 0.2s;
            border-right: 1px solid rgba(0, 0, 0, 0.15);
        }
        .compare-col-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
        }
        .order-btn-group {
            display: flex;
            gap: 4px;
        }
        .order-btn {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 700;
            transition: all 0.15s;
        }
        .order-btn:hover:not(:disabled) {
            background: rgba(0, 0, 0, 0.8);
            border-color: var(--accent);
            transform: scale(1.08);
        }
        .order-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        .col-remove-btn {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            transition: all 0.15s;
        }
        .col-remove-btn:hover {
            background: rgba(239, 68, 68, 0.9);
            transform: scale(1.1);
        }
        .compare-col-details {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 14px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            color: #fff;
        }
        .compare-col-code {
            font-size: 1.3rem;
            font-weight: 800;
        }
        .compare-col-name {
            font-size: 0.95rem;
            opacity: 0.85;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .compare-col-hex {
            font-family: ui-monospace, monospace;
            font-size: 0.85rem;
            color: var(--accent);
            cursor: pointer;
            margin-top: 4px;
        }

        /* Sleek Floating Comparison Pill (Non-intrusive on mobile) */
        .floating-compare-pill {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(120px);
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(56, 189, 248, 0.35);
            padding: 8px 14px 8px 10px;
            border-radius: 999px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.7), 0 0 15px rgba(56, 189, 248, 0.2);
            z-index: 300;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s;
            max-width: 92vw;
        }
        .floating-compare-pill.visible {
            transform: translateX(-50%) translateY(0);
        }
        .floating-compare-pill:hover {
            border-color: var(--accent);
            transform: translateX(-50%) translateY(-2px);
        }
        .pill-swatches-row {
            display: flex;
            gap: 5px;
            align-items: center;
        }
        .pill-mini-dot {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            border: 1.5px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4);
            flex-shrink: 0;
        }
        .pill-label {
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }
        .pill-action-tag {
            background: var(--accent);
            color: #0b0f19;
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .toast {
            position: fixed;
            top: 24px;
            left: 50%;
            transform: translateX(-50%) translateY(-100px);
            background: var(--accent);
            color: #0b0f19;
            padding: 9px 18px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.85rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 1000;
        }
        .toast.show {
            transform: translateX(-50%) translateY(0);
        }
    </style>
</head>
<body>

<header>
    <div class="header-content">
        <div class="top-bar">
            <div class="brand-title">
                🎨 Asian Paints Complete Catalogue
                <span class="brand-badge">2,200+ Shades</span>
            </div>
            <div class="action-btns">
                <button class="btn btn-primary" id="open-compare-btn" onclick="openCompareModal()">
                    ⚖️ Compare View (<span id="compare-count-top">0</span>)
                </button>
            </div>
        </div>

        <div class="search-container">
            <span class="search-icon">🔍</span>
            <input type="text" id="search" class="search-input" placeholder="Search by shade code (e.g. 8499, 0N68, L101) or name (e.g. Eclipse)...">
        </div>

        <!-- Indicative Color Filter Strip -->
        <div class="filter-strip-wrapper">
            <div class="filter-strip" id="filter-strip">
                <div class="color-chip active" data-family="all">
                    <div class="color-bubble" style="background: conic-gradient(from 180deg, #ef4444, #f59e0b, #10b981, #06b6d4, #3b82f6, #8b5cf6, #ec4899, #ef4444);"></div>
                    <span>All Colours</span>
                    <span class="chip-count" id="count-all">0</span>
                </div>
            </div>
        </div>
    </div>
</header>

<main>
    <div style="margin-bottom: 12px; font-size: 0.85rem; color: var(--text-muted);" id="stats">
        Showing shades...
    </div>
    <div class="grid" id="grid"></div>
</main>

<!-- Fullscreen Single Shade Modal -->
<div class="modal" id="modal">
    <div class="modal-top">
        <button class="close-btn" onclick="closeModal()">✕</button>
        <div class="modal-nav">
            <button class="nav-btn" onclick="prevShade()">←</button>
            <button class="nav-btn" onclick="nextShade()">→</button>
        </div>
    </div>

    <div class="modal-center">
        <div class="modal-code" id="modal-code"></div>
        <div class="modal-name" id="modal-name"></div>
        <div class="modal-badges">
            <div class="modal-badge" id="modal-hex-btn" onclick="copyModalHex()">
                <span id="modal-hex"></span> 📋
            </div>
            <div class="modal-badge" id="modal-rgb-btn" onclick="copyModalRgb()">
                <span id="modal-rgb"></span> 📋
            </div>
            <div class="modal-badge" id="modal-family"></div>
        </div>
    </div>

    <div class="modal-bottom">
        <button class="modal-action-btn" id="modal-pin-btn" onclick="toggleModalPin()">
            📌 Pin to Compare
        </button>
        <button class="modal-action-btn" onclick="shareCurrentShade()">
            🔗 Share Shade Link
        </button>
    </div>
</div>

<!-- Fullscreen Side-by-Side Comparison Modal with Re-ordering & Sharing -->
<div class="compare-modal" id="compare-modal">
    <div class="compare-header">
        <div class="compare-title">
            ⚖️ Side-by-Side Comparison (<span id="compare-modal-count">0</span> shades)
            <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted); margin-left: 8px;">(Use ← → to reorder)</span>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="btn btn-primary" onclick="shareComparisonLink()">🔗 Share Comparison Link</button>
            <button class="btn" onclick="clearPalette()">Clear All</button>
            <button class="btn" onclick="closeCompareModal()">Close ✕</button>
        </div>
    </div>
    <div class="compare-columns" id="compare-columns"></div>
</div>

<!-- Non-intrusive Floating Comparison Pill on Mobile/Desktop -->
<div class="floating-compare-pill" id="floating-pill" onclick="openCompareModal()">
    <div class="pill-swatches-row" id="pill-swatches"></div>
    <div class="pill-label">
        <span>Compare</span>
        <span class="pill-action-tag" id="pill-count">0</span>
    </div>
</div>

<div class="toast" id="toast">Copied to clipboard!</div>

<script>
    const allShades = __SHADES_JSON__;
    const familyColors = __FAMILY_COLORS_JSON__;

    const STORAGE_KEY = 'ap_pinned_shades';

    let activeFamily = 'all';
    let searchQuery = '';
    let pinnedShades = [];
    let currentShadeIndex = 0;
    let filteredShades = [...allShades];

    const grid = document.getElementById('grid');
    const searchInput = document.getElementById('search');
    const filterStrip = document.getElementById('filter-strip');
    const stats = document.getElementById('stats');
    const floatingPill = document.getElementById('floating-pill');
    const pillSwatches = document.getElementById('pill-swatches');
    const pillCount = document.getElementById('pill-count');
    const compareCountTop = document.getElementById('compare-count-top');
    const toast = document.getElementById('toast');
    const countAll = document.getElementById('count-all');

    // Modal elements
    const modal = document.getElementById('modal');
    const modalCode = document.getElementById('modal-code');
    const modalName = document.getElementById('modal-name');
    const modalHex = document.getElementById('modal-hex');
    const modalRgb = document.getElementById('modal-rgb');
    const modalFamily = document.getElementById('modal-family');
    const modalPinBtn = document.getElementById('modal-pin-btn');

    // Compare Modal
    const compareModal = document.getElementById('compare-modal');
    const compareColumns = document.getElementById('compare-columns');
    const compareModalCount = document.getElementById('compare-modal-count');

    // Populate family count for all
    countAll.textContent = allShades.length;

    // Extract families and counts
    const familyCounts = {};
    allShades.forEach(s => {
        const f = s.family || 'other';
        familyCounts[f] = (familyCounts[f] || 0) + 1;
    });

    const families = Object.keys(familyCounts).sort();
    families.forEach(f => {
        const chip = document.createElement('div');
        chip.className = 'color-chip';
        chip.dataset.family = f;

        const bubbleColor = familyColors[f.toLowerCase()] || '#475569';
        chip.innerHTML = `
            <div class="color-bubble" style="background: ${bubbleColor};"></div>
            <span>${f.charAt(0).toUpperCase() + f.slice(1)}</span>
            <span class="chip-count">${familyCounts[f]}</span>
        `;

        chip.onclick = () => {
            document.querySelectorAll('.color-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeFamily = f;
            render();
        };
        filterStrip.appendChild(chip);
    });

    document.querySelector('[data-family="all"]').onclick = (e) => {
        document.querySelectorAll('.color-chip').forEach(c => c.classList.remove('active'));
        document.querySelector('[data-family="all"]').classList.add('active');
        activeFamily = 'all';
        render();
    };

    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        render();
    });

    function hexToRgb(hex) {
        let c = (hex || '#ffffff').replace('#', '');
        if (c.length === 3) c = c.split('').map(x => x + x).join('');
        const num = parseInt(c, 16);
        return {
            r: (num >> 16) & 255,
            g: (num >> 8) & 255,
            b: num & 255
        };
    }

    function getLuminance(hex) {
        const {r, g, b} = hexToRgb(hex);
        return (0.299 * r + 0.587 * g + 0.114 * b);
    }

    function copyText(text, label) {
        navigator.clipboard.writeText(text);
        showToast(label ? `${label}: ${text} copied!` : `Copied ${text}!`);
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2200);
    }

    // Storage and URL persistence
    function saveState() {
        const codes = pinnedShades.map(s => s.code);
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(codes));
        } catch(e) {}

        const url = new URL(window.location.href);
        if (codes.length > 0) {
            url.searchParams.set('compare', codes.join(','));
        } else {
            url.searchParams.delete('compare');
        }
        window.history.replaceState({}, '', url.toString());
    }

    function restoreState() {
        const urlParams = new URLSearchParams(window.location.search);
        const compareParam = urlParams.get('compare') || urlParams.get('c') || urlParams.get('shades');
        const shadeParam = urlParams.get('shade') || urlParams.get('s');

        let codesToLoad = [];
        let openModalFromUrl = false;

        if (compareParam) {
            codesToLoad = compareParam.split(',').map(c => c.trim().toLowerCase());
            openModalFromUrl = true;
        } else {
            try {
                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored) {
                    codesToLoad = JSON.parse(stored).map(c => String(c).trim().toLowerCase());
                }
            } catch(e) {}
        }

        if (codesToLoad.length > 0) {
            codesToLoad.forEach(code => {
                const found = allShades.find(s => s.code && s.code.toLowerCase() === code);
                if (found && !pinnedShades.some(p => p.code === found.code)) {
                    pinnedShades.push(found);
                }
            });
            renderFloatingPill();
            if (openModalFromUrl && pinnedShades.length > 0) {
                openCompareModal();
            }
        }

        if (shadeParam && !compareParam) {
            const idx = allShades.findIndex(s => s.code && s.code.toLowerCase() === shadeParam.toLowerCase());
            if (idx > -1) {
                openModal(idx);
            }
        }
    }

    function shareComparisonLink() {
        if (pinnedShades.length === 0) {
            showToast('Pin shades to create a share link!');
            return;
        }
        const codes = pinnedShades.map(s => s.code).join(',');
        const url = new URL(window.location.href);
        url.searchParams.set('compare', codes);
        url.searchParams.delete('shade');
        
        const shareUrl = url.toString();
        if (navigator.share) {
            navigator.share({
                title: 'Asian Paints Palette Comparison',
                text: `Check out this Asian Paints color palette: ${pinnedShades.map(s => s.code + ' ' + s.name).join(', ')}`,
                url: shareUrl
            }).catch(() => {
                copyText(shareUrl, 'Share URL');
            });
        } else {
            copyText(shareUrl, 'Comparison Link');
        }
    }

    function shareCurrentShade() {
        const shade = filteredShades[currentShadeIndex];
        if (!shade) return;
        const url = new URL(window.location.href);
        url.searchParams.set('shade', shade.code);
        url.searchParams.delete('compare');
        
        const shareUrl = url.toString();
        if (navigator.share) {
            navigator.share({
                title: `Asian Paints - ${shade.code} ${shade.name}`,
                text: `${shade.code} ${shade.name} (${shade.hex})`,
                url: shareUrl
            }).catch(() => {
                copyText(shareUrl, 'Shade URL');
            });
        } else {
            copyText(shareUrl, 'Shade Link');
        }
    }

    // Open single shade fullscreen modal
    function openModal(index) {
        currentShadeIndex = index;
        const shade = filteredShades[index];
        if (!shade) return;

        const hex = shade.hex || '#475569';
        const {r, g, b} = hexToRgb(hex);
        const lum = getLuminance(hex);
        const textColor = lum > 140 ? '#0f172a' : '#f8fafc';

        modal.style.background = hex;
        modal.style.color = textColor;

        modalCode.textContent = shade.code || '—';
        modalName.textContent = shade.name || '—';
        modalHex.textContent = hex.toUpperCase();
        modalRgb.textContent = `RGB(${r}, ${g}, ${b})`;
        modalFamily.textContent = shade.family ? (shade.family.charAt(0).toUpperCase() + shade.family.slice(1)) : 'Wall Shade';

        updateModalPinState();
        modal.classList.add('active');
    }

    function closeModal() {
        modal.classList.remove('active');
    }

    function nextShade() {
        if (currentShadeIndex < filteredShades.length - 1) {
            openModal(currentShadeIndex + 1);
        } else {
            openModal(0);
        }
    }

    function prevShade() {
        if (currentShadeIndex > 0) {
            openModal(currentShadeIndex - 1);
        } else {
            openModal(filteredShades.length - 1);
        }
    }

    function copyModalHex() {
        const shade = filteredShades[currentShadeIndex];
        if (shade) copyText(shade.hex, 'HEX');
    }

    function copyModalRgb() {
        const shade = filteredShades[currentShadeIndex];
        if (shade) {
            const {r, g, b} = hexToRgb(shade.hex);
            copyText(`rgb(${r}, ${g}, ${b})`, 'RGB');
        }
    }

    function updateModalPinState() {
        const shade = filteredShades[currentShadeIndex];
        if (!shade) return;
        const isPinned = pinnedShades.some(p => p.code === shade.code);
        modalPinBtn.innerHTML = isPinned ? '✓ Pinned in Compare' : '📌 Pin to Compare';
    }

    function toggleModalPin() {
        const shade = filteredShades[currentShadeIndex];
        if (shade) {
            togglePin(shade);
            updateModalPinState();
        }
    }

    // Comparison Management & Fullscreen Comparison Mode
    function togglePin(shade) {
        const idx = pinnedShades.findIndex(s => s.code === shade.code);
        if (idx > -1) {
            pinnedShades.splice(idx, 1);
        } else {
            pinnedShades.push(shade);
            showToast(`Added ${shade.code} ${shade.name} to compare`);
        }
        saveState();
        renderFloatingPill();
        render();
    }

    function moveCompare(index, direction) {
        const newIndex = index + direction;
        if (newIndex < 0 || newIndex >= pinnedShades.length) return;
        const item = pinnedShades.splice(index, 1)[0];
        pinnedShades.splice(newIndex, 0, item);
        saveState();
        renderFloatingPill();
        renderCompareColumns();
    }

    function clearPalette() {
        pinnedShades = [];
        saveState();
        renderFloatingPill();
        render();
        renderCompareColumns();
    }

    function renderFloatingPill() {
        const count = pinnedShades.length;
        compareCountTop.textContent = count;
        pillCount.textContent = count;

        if (count > 0) {
            floatingPill.classList.add('visible');
            pillSwatches.innerHTML = pinnedShades.map(s => `
                <div class="pill-mini-dot" style="background: ${s.hex || '#ccc'};" title="${s.code} ${s.name}"></div>
            `).join('');
        } else {
            floatingPill.classList.remove('visible');
            pillSwatches.innerHTML = '';
        }
    }

    function openCompareModal() {
        if (pinnedShades.length === 0) {
            showToast('Pin at least 2 shades to compare!');
            return;
        }
        renderCompareColumns();
        compareModal.classList.add('active');
    }

    function closeCompareModal() {
        compareModal.classList.remove('active');
    }

    function renderCompareColumns() {
        compareModalCount.textContent = pinnedShades.length;
        if (pinnedShades.length === 0) {
            closeCompareModal();
            return;
        }
        compareColumns.innerHTML = pinnedShades.map((s, idx) => {
            const hex = s.hex || '#475569';
            const {r, g, b} = hexToRgb(hex);
            const lum = getLuminance(hex);
            const textColor = lum > 140 ? '#0f172a' : '#f8fafc';
            const isFirst = idx === 0;
            const isLast = idx === pinnedShades.length - 1;

            return `
                <div class="compare-col" style="background: ${hex}; color: ${textColor};">
                    <div class="compare-col-top">
                        <div class="order-btn-group">
                            <button class="order-btn" ${isFirst ? 'disabled' : ''} title="Move Left" onclick="moveCompare(${idx}, -1)">←</button>
                            <button class="order-btn" ${isLast ? 'disabled' : ''} title="Move Right" onclick="moveCompare(${idx}, 1)">→</button>
                        </div>
                        <button class="col-remove-btn" title="Remove" onclick="togglePin(${JSON.stringify(s).replace(/"/g, '&quot;')}); renderCompareColumns();">✕</button>
                    </div>
                    <div class="compare-col-details">
                        <div class="compare-col-code">${s.code || '—'}</div>
                        <div class="compare-col-name">${s.name || '—'}</div>
                        <div class="compare-col-hex" onclick="copyText('${hex}', 'HEX')">${hex.toUpperCase()}</div>
                        <div style="font-size: 0.75rem; opacity: 0.85;">RGB(${r}, ${g}, ${b})</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    window.addEventListener('keydown', (e) => {
        if (modal.classList.contains('active')) {
            if (e.key === 'Escape') closeModal();
            if (e.key === 'ArrowRight') nextShade();
            if (e.key === 'ArrowLeft') prevShade();
        }
        if (compareModal.classList.contains('active')) {
            if (e.key === 'Escape') closeCompareModal();
        }
    });

    function render() {
        filteredShades = allShades.filter(s => {
            const matchesFamily = (activeFamily === 'all' || s.family === activeFamily);
            const matchesSearch = !searchQuery || 
                (s.name && s.name.toLowerCase().includes(searchQuery)) || 
                (s.code && s.code.toLowerCase().includes(searchQuery)) ||
                (s.hex && s.hex.toLowerCase().includes(searchQuery));
            return matchesFamily && matchesSearch;
        });

        stats.textContent = `Showing ${filteredShades.length.toLocaleString()} of ${allShades.length.toLocaleString()} shades (Tap card for fullscreen view)`;

        grid.innerHTML = filteredShades.map((s, idx) => {
            const isPinned = pinnedShades.some(p => p.code === s.code);
            const hex = s.hex || '#475569';
            return `
                <div class="card" onclick="openModal(${idx})">
                    <div class="swatch-box" style="background: ${hex};">
                        <button class="pin-btn ${isPinned ? 'pinned' : ''}" title="Pin to Compare" onclick="event.stopPropagation(); togglePin(${JSON.stringify(s).replace(/"/g, '&quot;')})">
                            📌
                        </button>
                    </div>
                    <div class="card-details">
                        <div class="shade-code">${s.code || '—'}</div>
                        <div class="shade-name" title="${s.name || ''}">${s.name || '—'}</div>
                        <div class="meta-row">
                            <span class="hex-code" onclick="event.stopPropagation(); copyText('${hex}', 'HEX')">${hex.toUpperCase()}</span>
                            <span class="family-tag">${s.family || ''}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    render();
    restoreState();
</script>
</body>
</html>
"""
    html_content = template.replace('__SHADES_JSON__', shades_json).replace('__FAMILY_COLORS_JSON__', family_colors_json)

    out_path = '/home/apv/projects/shadebook/asian_paints_catalogue.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Updated interactive webpage built at {out_path} ({len(html_content)} bytes)")

if __name__ == '__main__':
    build_html()
