# qcs-model-zoo

**Independently measured models for the Qualcomm QCS6490 (Dragonwing RB3 Gen 2).**

Qualcomm's AI Hub tells you which models are *supported*. This zoo tells you what they
actually *measured* — every entry profiled on real RB3 Gen 2 silicon via AI Hub
Workbench, under one stated protocol per entry, with job IDs you can look up. Failures
are recorded as failures, with the root cause when known. Several entries are the
first public RB3 measurements for their model; where upstream already publishes
numbers, the card says so and states the protocol difference.

## The zoo

| Model | Task | Input | RB3 Gen 2 result | Details |
|---|---|---|---|---|
| InternVL3.5-2B | genai | — | partial — 6 of 9 graphs measured; model not supported on RB3 Gen 2 (see card) | [card](https://huggingface.co/anguoyang/internvl3.5-2b-qcs6490) |
| Llama 3.2 1B Instruct | genai | — | prefill 1,024 tok/s · decode 16.4 tok/s (w4a16, cl512) | [card](https://huggingface.co/anguoyang/llama-3.2-1b-qcs6490) |
| Qwen3-0.6B | genai | — | prefill 1,555 tok/s · decode 24.6 tok/s (w4a16, cl512) | [card](https://huggingface.co/anguoyang/qwen3-0.6b-qcs6490) |
| all-MiniLM-L6-v2 | text_embedding | 1x128 tokens | 39.6 ms (float) | [card](https://huggingface.co/anguoyang/minilm-v2-qcs6490) |
| Nomic Embed Text v1 | text_embedding | 1x128 tokens | 423.9 ms (float) | [card](https://huggingface.co/anguoyang/nomic-embed-text-qcs6490) |
| NetVLAD | image_retrieval | 1x3x480x640 | 218.9 ms (float) | [card](https://huggingface.co/anguoyang/netvlad-qcs6490) |
| EfficientNet-Lite4 | image_classification | 1x3x300x300 | 28.0 ms (float) | [card](https://huggingface.co/anguoyang/efficientnet-lite4-qcs6490) |
| DAMO-YOLO-S | object_detection | 1x3x640x640 | 13.3 ms (w8a8) | [card](https://huggingface.co/anguoyang/damoyolo) |
| NanoDet-Plus-m 416 | object_detection | 1x3x416x416 | 6.5 ms (w8a8) | [card](https://huggingface.co/anguoyang/nanodet) |
| PicoDet-M 416 | object_detection | 1x3x416x416 | 42.2 ms (float) | data row |
| YOLOv11-N | object_detection | 1x3x640x640 | 5.0 ms (w8a8) | [card](https://huggingface.co/anguoyang/yolo11n) |
| YOLOv8-S | object_detection | 1x3x640x640 | 5.0 ms (w8a8) | data row |
| DeepLabV3+ MobileNet | segmentation | 1x3x520x520 | 154.7 ms (float) | [card](https://huggingface.co/anguoyang/deeplabv3-plus-mobilenet-qcs6490) |
| Depth Anything V2 | depth_estimation | 1x3x518x518 | 1,589.6 ms (float) | [card](https://huggingface.co/anguoyang/depth-anything-v2-qcs6490) |
| MoveNet | pose_estimation | 1x3x192x192 | 17.7 ms (float) | [card](https://huggingface.co/anguoyang/movenet-qcs6490) |
| SESR-M5 | super_resolution | 1x3x128x128 | 40.4 ms (float) | [card](https://huggingface.co/anguoyang/sesr-m5-qcs6490) |
| TrOCR | ocr | 1x3x384x384 | 476.1 ms (float) | [card](https://huggingface.co/anguoyang/trocr-qcs6490) |

Full data (all precisions, runtimes, per-cell job IDs, failure notes):
[qcs-bench leaderboard](https://github.com/anguoyang/qcs-bench) — `data/leaderboard.json` is the single source of truth;
this table is generated from it by `gen_readme.py`. The Hugging Face shelf for the same
collection: [Edge AI on Qualcomm — Measured Recipes](https://huggingface.co/collections/anguoyang/edge-ai-on-qualcomm-measured-recipes-6af6783416f932ebae149279).

## How entries are measured

- Device: Dragonwing RB3 Gen 2 Vision Kit (QCS6490), profiled through Qualcomm AI Hub Workbench (cloud device).
- Breadth-sweep entries (2026-11): fp32 ONNX exported from `qai-hub-models` 0.66.0 definitions, AI Hub default compile options, single-graph profile; the number is the profile job's `estimated_inference_time`. Same harness, same protocol, every model.
- GenAI entries: per-graph profiles of the vendor pre-quantized assets (w4a16, context 512), converted to tok/s; not Genie end-to-end runs. Each card states its exact method.
- Detection entries: the headline number is the best measured cell; the leaderboard carries every precision/runtime cell, including the ones that failed (marked UNKNOWN with the reason).

## What you can take

- **Tier A (redistributable licenses — Apache-2.0 / MIT / BSD):** the HF card carries the recipe and, where the sweep produced one, the exported ONNX.
- **Tier B (restricted licenses — e.g. Llama Community License, AGPL):** numbers, method and job IDs only. No weights, no compiled artifacts. The card states the license.

## License & affiliation

Measurement data in this repo: CC BY 4.0. Generator code: MIT. Model weights and names
belong to their respective owners under their own licenses. This is an independent
community project — **not affiliated with or endorsed by Qualcomm Technologies, Inc.**
Qualcomm, Snapdragon and Dragonwing are trademarks of Qualcomm Incorporated.
