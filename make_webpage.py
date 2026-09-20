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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#0b0f19">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
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
        html, body {
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            min-height: 100dvh;
            text-rendering: optimizeLegibility;
            overflow-x: hidden;
        }

        /* Views */
        .app-view {
            display: none;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
        }
        .app-view.active-view {
            display: block;
        }

        /* ---------------- CATALOGUE VIEW ---------------- */
        #view-catalogue {
            padding-bottom: 80px;
        }
        header {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(11, 15, 25, 0.96);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
            padding: calc(12px + env(safe-area-inset-top, 0px)) 16px 12px 16px;
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
            padding: 8px 14px;
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
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 12px;
        }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.15s, border-color 0.15s;
            cursor: pointer;
            position: relative;
            content-visibility: auto;
            contain-intrinsic-size: 160px 190px;
        }
        .card:hover {
            transform: translateY(-3px);
            border-color: rgba(56, 189, 248, 0.4);
        }
        .swatch-box {
            height: 120px;
            width: 100%;
            position: relative;
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            padding: 8px;
        }
        .pin-btn {
            background: rgba(0, 0, 0, 0.55);
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
            opacity: 0.9;
            transition: transform 0.15s, background 0.15s;
            z-index: 2;
        }
        .pin-btn:hover {
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

        #scroll-sentinel {
            height: 40px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 20px;
        }

        /* ---------------- DEDICATED COMPARISON VIEW ---------------- */
        #view-compare.active-view {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            min-height: 100dvh;
            background: var(--bg);
        }
        .compare-page-header {
            position: sticky;
            top: 0;
            z-index: 100;
            background: #0b0f19;
            border-bottom: 1px solid var(--border);
            padding: calc(10px + env(safe-area-inset-top, 0px)) 16px 10px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            flex-shrink: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .compare-header-left {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .back-btn {
            background: var(--surface-card);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: all 0.15s;
        }
        .back-btn:hover {
            border-color: var(--accent);
            background: var(--surface-hover);
        }
        .compare-header-actions {
            display: flex;
            gap: 6px;
            align-items: center;
            flex-wrap: wrap;
        }

        .compare-content-container {
            flex: 1;
            display: flex;
            width: 100%;
            overflow: auto;
            -webkit-overflow-scrolling: touch;
            padding-bottom: env(safe-area-inset-bottom, 0px);
        }

        /* Desktop / Columnar Mode: Horizontal Side-by-Side Columns */
        .compare-content-container.layout-horizontal {
            flex-direction: row;
            height: calc(100vh - 65px);
            height: calc(100dvh - 65px);
            overflow-x: auto;
            overflow-y: hidden;
        }
        .compare-content-container.layout-horizontal .compare-col {
            flex: 1;
            min-width: 140px;
            max-width: 240px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 16px 10px;
            position: relative;
            border-right: 1px solid rgba(0, 0, 0, 0.15);
            flex-shrink: 0;
        }
        .compare-content-container.layout-horizontal .compare-col-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 4px;
            width: 100%;
        }
        /* In Columnar Mode: Stack the details neatly to prevent ANY horizontal overflow */
        .compare-content-container.layout-horizontal .compare-col-details {
            width: 100%;
            max-width: 100%;
            padding: 8px 10px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .compare-content-container.layout-horizontal .compare-title-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 2px;
        }
        .compare-content-container.layout-horizontal .compare-col-name {
            max-width: 100%;
            font-size: 0.78rem;
        }
        .compare-content-container.layout-horizontal .compare-inline-specs {
            flex-direction: column;
            align-items: stretch;
            gap: 3px;
            margin-top: 2px;
        }
        .compare-content-container.layout-horizontal .spec-chip {
            text-align: center;
            font-size: 0.7rem;
            padding: 2px 4px;
        }

        /* Mobile & Vertical: Full-Width Stacked Horizontal Bands */
        .compare-content-container.layout-vertical {
            flex-direction: column;
            overflow-y: auto;
            overflow-x: hidden;
            min-height: calc(100vh - 65px);
            min-height: calc(100dvh - 65px);
        }
        .compare-content-container.layout-vertical .compare-col {
            flex: 1;
            min-height: 95px;
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            padding: 10px 14px;
            position: relative;
            border-bottom: 2px solid rgba(0, 0, 0, 0.2);
            flex-shrink: 0;
        }
        .compare-content-container.layout-vertical .compare-col-details {
            max-width: 75%;
        }
        .compare-content-container.layout-vertical .compare-col-top {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 6px;
        }

        .order-btn-group {
            display: flex;
            gap: 3px;
        }
        .order-btn {
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 4px 8px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.82rem;
            font-weight: 700;
            transition: all 0.15s;
        }
        .order-btn:hover:not(:disabled) {
            background: rgba(0, 0, 0, 0.85);
            border-color: var(--accent);
        }
        .order-btn:disabled {
            opacity: 0.2;
            cursor: not-allowed;
        }
        .col-remove-btn {
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            transition: all 0.15s;
        }
        .col-remove-btn:hover {
            background: rgba(239, 68, 68, 0.9);
        }

        /* Sleek, Non-Obtrusive Ultra-Compact Details Pill */
        .compare-col-details {
            background: rgba(11, 15, 25, 0.75);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.22);
            padding: 6px 10px;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            gap: 3px;
            color: #fff;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            width: fit-content;
        }
        .compare-title-row {
            display: flex;
            align-items: baseline;
            gap: 6px;
            flex-wrap: nowrap;
        }
        .compare-col-code {
            font-size: 1.05rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            color: #fff;
        }
        .compare-col-name {
            font-size: 0.82rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 150px;
        }
        .compare-col-family {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 1px 6px;
            border-radius: 999px;
            backdrop-filter: blur(4px);
            white-space: nowrap;
        }
        .compare-family-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        
        /* Inline specs chips */
        .compare-inline-specs {
            display: flex;
            align-items: center;
            gap: 5px;
            font-family: ui-monospace, monospace;
            font-size: 0.72rem;
            white-space: nowrap;
        }
        .spec-chip {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 1px 5px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .spec-chip:hover {
            background: rgba(56, 189, 248, 0.25);
            border-color: var(--accent);
            color: var(--accent);
        }
        .spec-chip-hex {
            color: var(--accent);
            font-weight: 700;
        }

        /* Minimal Swatch Mode (Toggled) */
        .compare-content-container.minimal-mode .compare-col-name,
        .compare-content-container.minimal-mode .compare-inline-specs,
        .compare-content-container.minimal-mode .compare-col-family {
            display: none !important;
        }
        .compare-content-container.minimal-mode .compare-col-details {
            padding: 4px 8px;
        }
        .compare-content-container.minimal-mode .compare-col-code {
            font-size: 0.95rem;
        }

        /* Fullscreen Single Shade Modal */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100vw;
            height: 100vh;
            height: 100dvh;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: calc(20px + env(safe-area-inset-top, 0px)) 24px calc(24px + env(safe-area-inset-bottom, 0px)) 24px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
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

        /* Sleek Floating Comparison Pill */
        .floating-compare-pill {
            position: fixed;
            bottom: calc(20px + env(safe-area-inset-bottom, 0px));
            left: 50%;
            transform: translateX(-50%) translateY(120px);
            background: rgba(15, 23, 42, 0.94);
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
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s;
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
            top: calc(24px + env(safe-area-inset-top, 0px));
            left: 50%;
            transform: translateX(-50%) translateY(-100px);
            background: var(--accent);
            color: #0b0f19;
            padding: 9px 18px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.85rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 20000;
        }
        .toast.show {
            transform: translateX(-50%) translateY(0);
        }
    </style>
</head>
<body>

<!-- ================= 1. CATALOGUE VIEW ================= -->
<div class="app-view active-view" id="view-catalogue">
    <header>
        <div class="header-content">
            <div class="top-bar">
                <div class="brand-title">
                    🎨 Asian Paints Complete Catalogue
                    <span class="brand-badge">2,200+ Shades</span>
                </div>
                <div class="action-btns">
                    <button class="btn btn-primary" id="open-compare-btn" onclick="openCompareScreen()">
                        ⚖️ Compare View (<span id="compare-count-top">0</span>)
                    </button>
                </div>
            </div>

            <div class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" id="search" class="search-input" placeholder="Search by shade code (e.g. 8499, 0N68, L101) or name (e.g. Eclipse)...">
            </div>

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
        <div id="scroll-sentinel"></div>
    </main>

    <!-- Floating Compare Button on Catalogue -->
    <div class="floating-compare-pill" id="floating-pill" onclick="openCompareScreen()">
        <div class="pill-swatches-row" id="pill-swatches"></div>
        <div class="pill-label">
            <span>Compare</span>
            <span class="pill-action-tag" id="pill-count">0</span>
        </div>
    </div>
</div>

<!-- ================= 2. DEDICATED FULL-SCREEN COMPARISON VIEW ================= -->
<div class="app-view" id="view-compare">
    <div class="compare-page-header">
        <div class="compare-header-left">
            <button class="back-btn" onclick="openCatalogueScreen()">
                ← Browse
            </button>
            <div style="font-size: 0.95rem; font-weight: 700;">
                ⚖️ (<span id="compare-page-count">0</span>)
            </div>
            <button class="btn" id="layout-toggle-btn" onclick="toggleCompareLayout()" style="padding: 4px 8px; font-size: 0.75rem;">
                📱 Stack
            </button>
            <button class="btn" id="minimal-toggle-btn" onclick="toggleMinimalMode()" style="padding: 4px 8px; font-size: 0.75rem;" title="Toggle compact/pure swatch view">
                👁️ Full Swatch
            </button>
        </div>
        <div class="compare-header-actions">
            <button class="btn btn-primary" onclick="shareComparisonLink()" style="padding: 5px 10px; font-size: 0.78rem;">🔗 Share</button>
            <button class="btn" onclick="clearPalette()" style="padding: 5px 10px; font-size: 0.78rem;">Clear</button>
        </div>
    </div>
    <div class="compare-content-container layout-vertical" id="compare-container"></div>
</div>

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

<div class="toast" id="toast">Copied to clipboard!</div>

<script>
    const allShades = __SHADES_JSON__;
    const familyColors = __FAMILY_COLORS_JSON__;

    const STORAGE_KEY = '***';
    const PAGE_SIZE = 60;

    let activeFamily = 'all';
    let searchQuery = '';
    let pinnedShades = [];
    let currentShadeIndex = 0;
    let filteredShades = [...allShades];
    let renderedCount = 0;
    let activeView = 'catalogue';
    let isMinimalMode = false;
    
    let compareLayout = window.innerWidth <= 768 ? 'vertical' : 'horizontal';

    const viewCatalogue = document.getElementById('view-catalogue');
    const viewCompare = document.getElementById('view-compare');
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
    const sentinel = document.getElementById('scroll-sentinel');
    const layoutToggleBtn = document.getElementById('layout-toggle-btn');
    const minimalToggleBtn = document.getElementById('minimal-toggle-btn');
    const compareContainer = document.getElementById('compare-container');
    const comparePageCount = document.getElementById('compare-page-count');

    // Modal elements
    const modal = document.getElementById('modal');
    const modalCode = document.getElementById('modal-code');
    const modalName = document.getElementById('modal-name');
    const modalHex = document.getElementById('modal-hex');
    const modalRgb = document.getElementById('modal-rgb');
    const modalFamily = document.getElementById('modal-family');
    const modalPinBtn = document.getElementById('modal-pin-btn');

    countAll.textContent = allShades.length;

    // Precalculate RGBs for all shades
    allShades.forEach(s => {
        let c = (s.hex || '#ffffff').replace('#', '');
        if (c.length === 3) c = c.split('').map(x => x + x).join('');
        const num = parseInt(c, 16);
        s._r = (num >> 16) & 255;
        s._g = (num >> 8) & 255;
        s._b = num & 255;
        s._lum = 0.299 * s._r + 0.587 * s._g + 0.114 * s._b;
    });

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
            applyFilter();
        };
        filterStrip.appendChild(chip);
    });

    document.querySelector('[data-family="all"]').onclick = (e) => {
        document.querySelectorAll('.color-chip').forEach(c => c.classList.remove('active'));
        document.querySelector('[data-family="all"]').classList.add('active');
        activeFamily = 'all';
        applyFilter();
    };

    let searchDebounceTimer;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
            searchQuery = e.target.value.toLowerCase().trim();
            applyFilter();
        }, 60);
    });

    function getFamilyColor(fam) {
        const key = (fam || '').toLowerCase();
        return familyColors[key] || '#94a3b8';
    }

    function copyText(text, label) {
        navigator.clipboard.writeText(text);
        showToast(label ? `${label}: ${text} copied!` : `Copied ${text}!`);
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2000);
    }

    /* Screen Navigation (SPA) */
    function openCompareScreen() {
        if (pinnedShades.length === 0) {
            showToast('Pin at least 2 shades to compare!');
            return;
        }
        activeView = 'compare';
        viewCatalogue.classList.remove('active-view');
        viewCompare.classList.add('active-view');
        window.scrollTo(0, 0);
        renderCompareScreen();
    }

    function openCatalogueScreen() {
        activeView = 'catalogue';
        viewCompare.classList.remove('active-view');
        viewCatalogue.classList.add('active-view');
    }

    window.addEventListener('popstate', () => {
        restoreState();
    });

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
        let openCompareFromUrl = false;

        if (compareParam) {
            codesToLoad = compareParam.split(',').map(c => c.trim().toLowerCase());
            openCompareFromUrl = true;
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
            if (openCompareFromUrl && pinnedShades.length > 0) {
                openCompareScreen();
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

    function openModal(index) {
        currentShadeIndex = index;
        const shade = filteredShades[index];
        if (!shade) return;

        const hex = shade.hex || '#475569';
        const textColor = shade._lum > 140 ? '#0f172a' : '#f8fafc';

        modal.style.background = hex;
        modal.style.color = textColor;

        modalCode.textContent = shade.code || '—';
        modalName.textContent = shade.name || '—';
        modalHex.textContent = hex.toUpperCase();
        modalRgb.textContent = `RGB: ${shade._r}, ${shade._g}, ${shade._b}`;
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
            copyText(`rgb(${shade._r}, ${shade._g}, ${shade._b})`, 'RGB');
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
        updateCardPinStyles();
    }

    function moveCompare(index, direction) {
        const newIndex = index + direction;
        if (newIndex < 0 || newIndex >= pinnedShades.length) return;
        const item = pinnedShades.splice(index, 1)[0];
        pinnedShades.splice(newIndex, 0, item);
        saveState();
        renderFloatingPill();
        renderCompareScreen();
    }

    function clearPalette() {
        pinnedShades = [];
        saveState();
        renderFloatingPill();
        updateCardPinStyles();
        renderCompareScreen();
    }

    function renderFloatingPill() {
        const count = pinnedShades.length;
        compareCountTop.textContent = count;
        pillCount.textContent = count;

        if (count > 0) {
            floatingPill.classList.add('visible');
            pillSwatches.innerHTML = pinnedShades.map(s => `
                <div class="pill-mini-dot" style="background: ${s.hex || '#ccc'};" title="${s.code} ${s.name} (${s.family || ''})"></div>
            `).join('');
        } else {
            floatingPill.classList.remove('visible');
            pillSwatches.innerHTML = '';
        }
    }

    function toggleCompareLayout() {
        compareLayout = compareLayout === 'vertical' ? 'horizontal' : 'vertical';
        renderCompareScreen();
    }

    function toggleMinimalMode() {
        isMinimalMode = !isMinimalMode;
        minimalToggleBtn.textContent = isMinimalMode ? '🏷️ Show Details' : '👁️ Full Swatch';
        if (isMinimalMode) {
            compareContainer.classList.add('minimal-mode');
        } else {
            compareContainer.classList.remove('minimal-mode');
        }
    }

    function renderCompareScreen() {
        const count = pinnedShades.length;
        comparePageCount.textContent = count;
        if (count === 0) {
            openCatalogueScreen();
            return;
        }

        const isVert = compareLayout === 'vertical';
        compareContainer.className = `compare-content-container layout-${compareLayout} ${isMinimalMode ? 'minimal-mode' : ''}`;
        layoutToggleBtn.textContent = isVert ? '📱 Stack' : '💻 Columns';

        const prevIcon = isVert ? '↑' : '←';
        const nextIcon = isVert ? '↓' : '→';

        compareContainer.innerHTML = pinnedShades.map((s, idx) => {
            const hex = s.hex || '#475569';
            const isFirst = idx === 0;
            const isLast = idx === pinnedShades.length - 1;
            const fam = (s.family || 'other').toLowerCase();
            const familyName = s.family ? (s.family.charAt(0).toUpperCase() + s.family.slice(1)) : 'Wall';
            const famBaseHex = getFamilyColor(fam);
            
            const badgeBg = `rgba(${s._r}, ${s._g}, ${s._b}, 0.38)`;
            const badgeBorder = `rgba(${s._r}, ${s._g}, ${s._b}, 0.75)`;
            const dotColor = famBaseHex.startsWith('#') ? famBaseHex : '#38bdf8';

            return `
                <div class="compare-col" style="background: ${hex};">
                    ${isVert ? `
                        <!-- Vertical Stacked Mode: Clean 2-Line Inline Badge -->
                        <div class="compare-col-details">
                            <div class="compare-title-row">
                                <span class="compare-col-code">${s.code || '—'}</span>
                                <span class="compare-col-name" title="${s.name || ''}">${s.name || '—'}</span>
                                <span class="compare-col-family" style="background: ${badgeBg}; border: 1px solid ${badgeBorder};">
                                    <span class="compare-family-dot" style="background: ${dotColor};"></span>
                                    <span>${familyName}</span>
                                </span>
                            </div>
                            <div class="compare-inline-specs">
                                <span class="spec-chip spec-chip-hex" onclick="copyText('${hex}', 'HEX')" title="Copy HEX">${hex.toUpperCase()}</span>
                                <span class="spec-chip" onclick="copyText('rgb(${s._r}, ${s._g}, ${s._b})', 'RGB')" title="Copy RGB">RGB ${s._r}, ${s._g}, ${s._b}</span>
                            </div>
                        </div>
                    ` : `
                        <!-- Columnar Mode: Dedicated Vertical Stacked Card (No Horizontal Overflow) -->
                        <div class="compare-col-details">
                            <div style="font-size: 1.1rem; font-weight: 800; line-height: 1.1;">${s.code || '—'}</div>
                            <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.95; white-space: normal; line-height: 1.2;">${s.name || '—'}</div>
                            <div class="compare-col-family" style="background: ${badgeBg}; border: 1px solid ${badgeBorder}; margin: 2px 0;">
                                <span class="compare-family-dot" style="background: ${dotColor};"></span>
                                <span>${familyName}</span>
                            </div>
                            <div class="compare-inline-specs">
                                <span class="spec-chip spec-chip-hex" onclick="copyText('${hex}', 'HEX')" title="Copy HEX" style="width: 100%; display: block; text-align: center;">${hex.toUpperCase()}</span>
                                <span class="spec-chip" onclick="copyText('rgb(${s._r}, ${s._g}, ${s._b})', 'RGB')" title="Copy RGB" style="width: 100%; display: block; text-align: center;">RGB ${s._r}, ${s._g}, ${s._b}</span>
                            </div>
                        </div>
                    `}
                    <div class="compare-col-top">
                        <div class="order-btn-group">
                            <button class="order-btn" ${isFirst ? 'disabled' : ''} title="Move ${isVert ? 'Up' : 'Left'}" onclick="moveCompare(${idx}, -1)">${prevIcon}</button>
                            <button class="order-btn" ${isLast ? 'disabled' : ''} title="Move ${isVert ? 'Down' : 'Right'}" onclick="moveCompare(${idx}, 1)">${nextIcon}</button>
                        </div>
                        <button class="col-remove-btn" title="Remove" onclick="togglePin(${JSON.stringify(s).replace(/"/g, '&quot;')}); renderCompareScreen();">✕</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    function createCardHTML(s, idx) {
        const isPinned = pinnedShades.some(p => p.code === s.code);
        const hex = s.hex || '#475569';
        return `
            <div class="card" onclick="openModal(${idx})" data-code="${s.code}">
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
    }

    function updateCardPinStyles() {
        document.querySelectorAll('.card').forEach(card => {
            const code = card.dataset.code;
            const btn = card.querySelector('.pin-btn');
            if (btn) {
                const isPinned = pinnedShades.some(p => p.code === code);
                btn.classList.toggle('pinned', isPinned);
            }
        });
    }

    function renderMoreCards() {
        if (renderedCount >= filteredShades.length) {
            sentinel.style.display = 'none';
            return;
        }

        const nextBatch = filteredShades.slice(renderedCount, renderedCount + PAGE_SIZE);
        const fragmentHTML = nextBatch.map((s, i) => createCardHTML(s, renderedCount + i)).join('');
        grid.insertAdjacentHTML('beforeend', fragmentHTML);
        renderedCount += nextBatch.length;

        sentinel.style.display = renderedCount >= filteredShades.length ? 'none' : 'flex';
        sentinel.textContent = `Loaded ${renderedCount} of ${filteredShades.length}...`;
    }

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            renderMoreCards();
        }
    }, { rootMargin: '400px' });
    observer.observe(sentinel);

    function applyFilter() {
        filteredShades = allShades.filter(s => {
            const matchesFamily = (activeFamily === 'all' || s.family === activeFamily);
            const matchesSearch = !searchQuery || 
                (s.name && s.name.toLowerCase().includes(searchQuery)) || 
                (s.code && s.code.toLowerCase().includes(searchQuery)) ||
                (s.hex && s.hex.toLowerCase().includes(searchQuery));
            return matchesFamily && matchesSearch;
        });

        stats.textContent = `Showing ${filteredShades.length.toLocaleString()} of ${allShades.length.toLocaleString()} shades (Tap card for fullscreen view)`;

        grid.innerHTML = '';
        renderedCount = 0;
        window.scrollTo({ top: 0, behavior: 'instant' });
        renderMoreCards();
    }

    window.addEventListener('keydown', (e) => {
        if (modal.classList.contains('active')) {
            if (e.key === 'Escape') closeModal();
            if (e.key === 'ArrowRight') nextShade();
            if (e.key === 'ArrowLeft') prevShade();
        } else if (activeView === 'compare') {
            if (e.key === 'Escape') openCatalogueScreen();
        }
    });

    applyFilter();
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
