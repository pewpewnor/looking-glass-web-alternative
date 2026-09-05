# Looking Glass Web Alternative

Looking Glass Web Alternative is an alternative web-based implementation of the original Looking Glass objective: a user provides one or more example images of an object, points a camera at a real-world scene, and asks the system to find that object.

It returns whether the target was found, its bounding box, an approximate distance and direction, and optional spoken guidance. The original Looking Glass combines a Flutter client, Go backend, and custom ONNX few-shot pipeline; this project pursues similar objectives and results with a browser client, Flask backend, and a different model pipeline.

## How it works

1. The browser captures or uploads a scene image. The user types a target or records it as speech.
2. The Flask backend sends the target and image through an open-vocabulary GroundingDINO detector.
3. An optional named reference image is used by a Siamese matcher built on a pretrained ResNet-18 embedding to rerank ambiguous detections.
4. Depth Anything 3 estimates depth. The backend combines the detected box, depth, and image geometry to estimate distance, walking steps, direction, and simple surface relationships.
5. faster-whisper transcribes speech, Flan-T5 generates the instruction text, and Coqui TTS produces audio.
6. The browser displays the result and can read the instruction aloud.

The pipeline is implemented in [`backend/pipeline.py`](backend/pipeline.py). The browser client is in [`frontend/`](frontend/), and the API is in [`backend/app.py`](backend/app.py).

## Quick start

Requirements: Python 3.10, enough disk space for model downloads, and a CUDA-capable GPU if available. CPU mode is supported but slower.

The GroundingDINO checkpoint is not stored in Git. Put it at:

```text
models/groundingdino_swint_ogc.pth
```

Then install dependencies and start the server from the project root:

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
python -m pip install -r backend/requirements.txt
python app.py
```

Open <http://localhost:5001>. Hugging Face and TTS models may download on first start.

Docker is also supported after the checkpoint is present:

```bash
docker compose up --build
```

## Using references

Choose **Add Reference** in the web interface, give the image a name, and save it. When a search target has the same name, the reference can help rerank close detector candidates. Runtime references and uploads are kept out of Git under `backend/references/` and `backend/uploads/`.

## API

- `GET /health` — health check
- `POST /api/upload` — upload a scene image
- `POST /api/process` — detect a target and estimate navigation data
- `POST /api/transcribe` — transcribe recorded speech
- `POST /api/generate-instruction` — create text and audio guidance
- `GET/POST /api/references` — list or save named references
- `DELETE /api/references/<reference_name>` — remove a reference

## Evaluation

Evaluation images and YOLO labels live in `data/test_images/`. Optional evaluation references live in `data/reference_images/`. Generated reports go to `artifacts/evaluation_runs/`.

```bash
python scripts/evaluate_test_images.py --device cpu
python scripts/generate_evaluation_report.py
```

Use `--image`, `--target`, or `--reference-dir` to narrow an evaluation run. Evaluation loads the full model pipeline and can be slow.

## Repository layout

```text
backend/        Flask API and inference pipeline
frontend/       Static browser client
models/         GroundingDINO config and local checkpoint location
data/           Evaluation images, labels, and reference fixtures
scripts/        Environment, server, evaluation, and report utilities
artifacts/      Generated evaluation output (ignored by Git)
app.py          Root WSGI/development entry point
Dockerfile      Single-container deployment
docker-compose.yml
```

Distance and step counts are estimates, not precise measurements. This is an experimental alternative implementation, not a replacement for normal mobility or safety tools.
