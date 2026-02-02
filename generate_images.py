#!/usr/bin/env python3
"""Gemini API 画像生成スクリプト（リトライ＋複数モデル自動切替）
バックグラウンドで実行し、クォータ回復を待ちながら全画像を生成する"""

import sys
import os
import time
import json
import re
from pathlib import Path
from datetime import datetime

from google import genai
from google.genai import types

# === 設定 ===
API_KEY = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GEMINI_API_KEY", "")
OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "generation_log.json"

# 試行するモデル（優先順）
MODELS = [
    "gemini-2.0-flash-exp-image-generation",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image-preview",
]

MAX_RETRIES = 10
BASE_WAIT = 65  # 秒

client = genai.Client(api_key=API_KEY)

# === 画像定義 ===
IMAGES = [
    {
        "id": "hero-mockup",
        "prompt": (
            "Generate an image: "
            "A sleek SaaS dashboard mockup illustration on a very dark navy background (#0a0f1e). "
            "The screen shows a clean 3-step horizontal workflow: "
            "Step 1: A red-outlined CSV file icon with small error X marks. "
            "Step 2: A glowing processing node with orange (#ff9f43) and blue (#54a0ff) gradient, gear and waveform motifs. "
            "Step 3: A green-outlined completed document icon with a checkmark. "
            "The three steps are connected by smooth flowing neon blue (#54a0ff) stream lines. "
            "Entire UI sits on a frosted glass panel (semi-transparent with blur). "
            "Very subtle dot grid in background. "
            "Style: Clean flat design like Japanese SaaS products (SmartHR, freee style). "
            "Warm, trustworthy, professional tone. No text whatsoever in the image. "
            "No 3D effects. Minimal color palette: dark background, white, orange accent, blue accent."
        ),
    },
    {
        "id": "evolution-cycle",
        "prompt": (
            "Generate an image: "
            "A horizontal cycle infographic diagram on dark navy background (#111b30). "
            "Four icons in a row, each sitting on a frosted glass card: "
            "1. A simple business person silhouette icon with soft orange (#ff9f43) glow. "
            "2. A brain / neural network icon with soft blue (#54a0ff) glow. "
            "3. An upward trending graph icon with soft teal (#00d2d3) glow. "
            "4. A globe icon, slightly larger, with bright blue neon border (#54a0ff). "
            "Smooth curved arrows in neon blue connect each step. Arrow from step 4 loops back to step 1 forming a cycle. "
            "Very subtle dot pattern in background. "
            "Style: Japanese SaaS infographic, clean and easy to understand. "
            "Warm professional tone. No text in the image."
        ),
    },
    {
        "id": "step1-import",
        "prompt": (
            "Generate an image: "
            "A SaaS file upload UI mockup on dark background (#0d1528). "
            "Center: a dashed-border drop zone area. Inside it, a glowing blue (#54a0ff) folder icon. "
            "A CSV file icon with small table/grid pattern is being dragged into the zone from above, "
            "with a subtle motion trail effect. "
            "Frosted glass panel styling (semi-transparent with blur). "
            "Clean, minimal Japanese SaaS admin panel aesthetic. Generous whitespace. "
            "Style: flat design, warm professional. No text in the image."
        ),
    },
    {
        "id": "step2-process",
        "prompt": (
            "Generate an image: "
            "A SaaS AI processing screen mockup on dark background (#0d1528). "
            "Screen split into two halves: "
            "Left half 'Attack': Orange (#ff9f43) accent color. Document icon with sparkle effects, "
            "upward arrows suggesting quality improvement. "
            "Right half 'Defense': Teal (#00d2d3) accent color. Shield with checkmark icon, "
            "magnifying glass examining a document suggesting audit/compliance check. "
            "A gradient progress bar (orange to blue) at the top, glowing. "
            "Frosted glass panels. Warm but professional tone. "
            "Japanese SaaS style, clean flat design. No text in the image."
        ),
    },
    {
        "id": "step3-approval",
        "prompt": (
            "Generate an image: "
            "A SaaS document comparison review screen mockup on dark background (#0d1528). "
            "Two document panels side by side: "
            "Left: original document with red highlighted problem areas. "
            "Right: AI-improved document with green highlighted improvement areas, looking more polished. "
            "Below: two round action buttons - a green approve button with checkmark icon, "
            "and a blue edit button with pen icon. "
            "Diff-viewer aesthetic similar to code review tools. "
            "Frosted glass card styling. Orderly Japanese business system layout. "
            "No text in the image."
        ),
    },
    {
        "id": "problem-icon-1",
        "prompt": (
            "Generate an image: "
            "A single minimalist icon on dark navy background (#0a0f1e). "
            "A document/paper icon that looks bland and deflated, nearly empty inside, "
            "representing thin/low-quality content. The document appears limp and lifeless. "
            "Thin white line art style with soft orange (#ff9f43) neon glow around edges. "
            "Circular subtle background glow. Icon centered. "
            "Clean, simple, professional. No text."
        ),
    },
    {
        "id": "problem-icon-2",
        "prompt": (
            "Generate an image: "
            "A single minimalist icon on dark navy background (#0a0f1e). "
            "A shield icon with a crack/fracture and an exclamation mark, "
            "representing account suspension risk and danger. "
            "Thin white line art style with soft red-to-orange neon glow around edges. "
            "Circular subtle background glow. Icon centered. "
            "Clean, simple, professional. No text."
        ),
    },
    {
        "id": "problem-icon-3",
        "prompt": (
            "Generate an image: "
            "A single minimalist icon on dark navy background (#0a0f1e). "
            "A simple robot/AI face icon surrounded by scattered question marks "
            "and vague speech bubbles, representing unhelpful/vague AI suggestions. "
            "Thin white line art style with soft blue (#54a0ff) neon glow around edges. "
            "Circular subtle background glow. Icon centered. "
            "Clean, simple, professional. No text."
        ),
    },
    {
        "id": "features-ba",
        "prompt": (
            "Generate an image: "
            "A document transformation before/after UI on dark background (#0d1528). "
            "Top: A faded, plain document card with a red left border bar. "
            "Gray placeholder lines representing boring text. Dull and lifeless appearance. "
            "Bottom: A vibrant, enhanced document card with a green left border bar. "
            "Some placeholder lines highlighted in orange (#ff9f43) with subtle sparkle effects. Lively feel. "
            "A downward gradient arrow (orange to green) connecting top to bottom, suggesting transformation. "
            "Frosted glass card styling. Warm professional design. "
            "Japanese SaaS aesthetic. No text in the image."
        ),
    },
    {
        "id": "usecase-staffing",
        "prompt": (
            "Generate an image: "
            "A minimalist flat illustration on dark background (#0d1528). "
            "2-3 simple business people figures (Japanese-friendly flat illustration style) "
            "efficiently managing a large stack of documents. "
            "Documents flow through an AI processing node and come out organized and neat. "
            "Blue (#54a0ff) accent color. Clean flat design. "
            "Warm, approachable, professional. No text."
        ),
    },
    {
        "id": "usecase-multistore",
        "prompt": (
            "Generate an image: "
            "A minimalist flat illustration on dark background (#0d1528). "
            "A central headquarters building icon connected to 5-6 smaller store/branch icons "
            "in a network/hub-and-spoke layout. "
            "Shield overlays suggesting compliance protection radiating from the center to each branch. "
            "Teal (#00d2d3) accent color. Clean flat design. "
            "Warm, approachable, professional. No text."
        ),
    },
    {
        "id": "usecase-agency",
        "prompt": (
            "Generate an image: "
            "A minimalist flat illustration on dark background (#0d1528). "
            "A pipeline/funnel diagram: plain documents enter from the left, "
            "premium polished documents with quality star badges come out from the right. "
            "The output side has sparkle/shine effects and quality indicators. "
            "Orange (#ff9f43) accent color. Clean flat design. "
            "Warm, approachable, professional. No text."
        ),
    },
]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def try_generate(model, prompt):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if (
                hasattr(part, "inline_data")
                and part.inline_data
                and part.inline_data.mime_type.startswith("image/")
            ):
                return part.inline_data.data
    return None


def generate_image(image_def):
    img_id = image_def["id"]
    output_path = OUTPUT_DIR / f"{img_id}.png"

    if output_path.exists():
        log(f"  [SKIP] {img_id} (already exists)")
        return True

    for attempt in range(1, MAX_RETRIES + 1):
        for model in MODELS:
            log(f"  [{img_id}] attempt {attempt}, model: {model}")
            try:
                img_data = try_generate(model, image_def["prompt"])
                if img_data:
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    log(f"  [{img_id}] SUCCESS ({len(img_data) // 1024}KB) via {model}")
                    return True
                else:
                    log(f"  [{img_id}] no image returned from {model}")
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    wait = BASE_WAIT * attempt
                    match = re.search(r"retryDelay.*?(\d+)", err)
                    if match:
                        suggested = int(match.group(1))
                        wait = max(wait, suggested + 10)
                    log(f"  [{img_id}] rate limited ({model}). waiting {wait}s...")
                    time.sleep(wait)
                    break  # 次のattempt
                else:
                    log(f"  [{img_id}] error ({model}): {str(e)[:120]}")
                    continue  # 次のmodel

    log(f"  [{img_id}] FAILED after {MAX_RETRIES} attempts")
    return False


def main():
    if not API_KEY:
        print("ERROR: API key not provided")
        sys.exit(1)

    remaining = [img for img in IMAGES if not (OUTPUT_DIR / f"{img['id']}.png").exists()]

    log(f"Models: {', '.join(MODELS)}")
    log(f"Output: {OUTPUT_DIR}")
    log(f"Total: {len(IMAGES)}, Remaining: {len(remaining)}")
    log("=" * 50)

    if not remaining:
        log("All images already generated!")
        return

    success = 0
    fail = 0
    results = {}

    for i, img in enumerate(remaining, 1):
        log(f"[{i}/{len(remaining)}] {img['id']}")
        ok = generate_image(img)
        results[img["id"]] = "ok" if ok else "failed"
        if ok:
            success += 1
        else:
            fail += 1
        if i < len(remaining):
            log("  cooldown 10s...")
            time.sleep(10)

    log("=" * 50)
    log(f"DONE: {success} success, {fail} failed")

    with open(LOG_FILE, "w") as f:
        json.dump(results, f, indent=2)

    generated = list(OUTPUT_DIR.glob("*.png"))
    log(f"Generated files ({len(generated)}):")
    for p in sorted(generated):
        log(f"  - {p.name} ({p.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
