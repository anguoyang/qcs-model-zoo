#!/usr/bin/env python3
"""Generate qcs-model-zoo README.md from the qcs-bench leaderboard (single source of truth)."""
import json, pathlib

SRC = pathlib.Path(__file__).parent.parent / "qcs-bench" / "data" / "leaderboard.json"

CARD = {
    "yolo11n": "anguoyang/yolo11n",
    "nanodet-plus-m-416": "anguoyang/nanodet",
    "damoyolo-s": "anguoyang/damoyolo",
    "qwen3-0.6b": "anguoyang/qwen3-0.6b-qcs6490",
    "llama-3.2-1b-instruct": "anguoyang/llama-3.2-1b-qcs6490",
    "internvl3.5-2b": "anguoyang/internvl3.5-2b-qcs6490",
    "nomic-embed-text-v1": "anguoyang/nomic-embed-text-qcs6490",
    "netvlad": "anguoyang/netvlad-qcs6490",
    "all-minilm-l6-v2": "anguoyang/minilm-v2-qcs6490",
    "efficientnet-lite4": "anguoyang/efficientnet-lite4-qcs6490",
    "deeplabv3-plus-mobilenet": "anguoyang/deeplabv3-plus-mobilenet-qcs6490",
    "depth-anything-v2": "anguoyang/depth-anything-v2-qcs6490",
    "movenet": "anguoyang/movenet-qcs6490",
    "sesr-m5": "anguoyang/sesr-m5-qcs6490",
    "posenet-mobilenet": "anguoyang/posenet-mobilenet-qcs6490",
    "quicksrnet-medium": "anguoyang/quicksrnet-medium-qcs6490",
    "real-esrgan-x4plus": "anguoyang/real-esrgan-x4plus-qcs6490",
    "segformer-base": "anguoyang/segformer-base-qcs6490",
    "trocr": "anguoyang/trocr-qcs6490",
    "openai-clip": "anguoyang/openai-clip-qcs6490",
}
GENAI_TEXT = {
    "qwen3-0.6b": "prefill 1,555 tok/s · decode 24.6 tok/s (w4a16, cl512)",
    "llama-3.2-1b-instruct": "prefill 1,024 tok/s · decode 16.4 tok/s (w4a16, cl512)",
    "internvl3.5-2b": "partial — 6 of 9 graphs measured; model not supported on RB3 Gen 2 (see card)",
}
TASK_ORDER = ["genai", "text_embedding", "image_retrieval", "multimodal_retrieval", "image_classification",
              "object_detection", "segmentation", "depth_estimation", "pose_estimation",
              "super_resolution", "ocr"]

def headline(e):
    if e["model"] in GENAI_TEXT:
        return GENAI_TEXT[e["model"]]
    cells = [c for c in e["cells"] if c["device"] == "rb3-gen2" and c.get("latency_ms_estimate")]
    if not cells:
        return "—"
    best = min(cells, key=lambda c: c["latency_ms_estimate"])
    return f"{best['latency_ms_estimate']:,.1f} ms ({best.get('precision') or 'float'})"

def main():
    d = json.loads(SRC.read_text())
    entries = sorted(d["entries"], key=lambda e: (TASK_ORDER.index(e["task"]) if e["task"] in TASK_ORDER else 99, e["model"]))
    lines = []
    lines.append("# qcs-model-zoo")
    lines.append("")
    lines.append("**Independently measured models for the Qualcomm QCS6490 (Dragonwing RB3 Gen 2).**")
    lines.append("")
    lines.append("Qualcomm's AI Hub tells you which models are *supported*. This zoo tells you what they")
    lines.append("actually *measured* — every entry profiled on real RB3 Gen 2 silicon via AI Hub")
    lines.append("Workbench, under one stated protocol per entry, with job IDs you can look up. Failures")
    lines.append("are recorded as failures, with the root cause when known. Several entries are the")
    lines.append("first public RB3 measurements for their model; where upstream already publishes")
    lines.append("numbers, the card says so and states the protocol difference.")
    lines.append("")
    lines.append("## The zoo")
    lines.append("")
    lines.append("| Model | Task | Input | RB3 Gen 2 result | Details |")
    lines.append("|---|---|---|---|---|")
    for e in entries:
        card = CARD.get(e["model"])
        link = f"[card](https://huggingface.co/{card})" if card else "data row"
        name = e["model_full"].split(" — ")[0].split(" (")[0]
        lines.append(f"| {name} | {e['task']} | {e.get('input', '—')} | {headline(e)} | {link} |")
    lines.append("")
    lines.append("Full data (all precisions, runtimes, per-cell job IDs, failure notes):")
    lines.append("[qcs-bench leaderboard](https://github.com/anguoyang/qcs-bench) — `data/leaderboard.json` is the single source of truth;")
    lines.append("this table is generated from it by `gen_readme.py`. The Hugging Face shelf for the same")
    lines.append("collection: [qcs-model-zoo](https://huggingface.co/collections/anguoyang/qcs-model-zoo-6af6783416f932ebae149279).")
    lines.append("")
    lines.append("## How entries are measured")
    lines.append("")
    lines.append("- Device: Dragonwing RB3 Gen 2 Vision Kit (QCS6490), profiled through Qualcomm AI Hub Workbench (cloud device).")
    lines.append("- Breadth-sweep entries (2026-11): fp32 ONNX exported from `qai-hub-models` 0.66.0 definitions, AI Hub default compile options, single-graph profile; the number is the profile job's `estimated_inference_time`. Same harness, same protocol, every model.")
    lines.append("- GenAI entries: per-graph profiles of the vendor pre-quantized assets (w4a16, context 512), converted to tok/s; not Genie end-to-end runs. Each card states its exact method.")
    lines.append("- Detection entries: the headline number is the best measured cell; the leaderboard carries every precision/runtime cell, including the ones that failed (marked UNKNOWN with the reason).")
    lines.append("")
    lines.append("## What you can take")
    lines.append("")
    lines.append("- **Tier A (redistributable licenses — Apache-2.0 / MIT / BSD):** the HF card carries the recipe and, where the sweep produced one, the exported ONNX.")
    lines.append("- **Tier B (restricted licenses — e.g. Llama Community License, AGPL):** numbers, method and job IDs only. No weights, no compiled artifacts. The card states the license.")
    lines.append("")
    lines.append("## License & affiliation")
    lines.append("")
    lines.append("Measurement data in this repo: CC BY 4.0. Generator code: MIT. Model weights and names")
    lines.append("belong to their respective owners under their own licenses. This is an independent")
    lines.append("community project — **not affiliated with or endorsed by Qualcomm Technologies, Inc.**")
    lines.append("Qualcomm, Snapdragon and Dragonwing are trademarks of Qualcomm Incorporated.")
    lines.append("")
    pathlib.Path(__file__).with_name("README.md").write_text("\n".join(lines))
    print("README generated:", len(entries), "entries")

if __name__ == "__main__":
    main()
