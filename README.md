# InderAI — Complete Starter Package
This package expands the InderAI project with:
- LLM wrapper (OpenAI placeholder + local fallback)
- Full frontend using React + Tailwind via CDN (Chat, Draft Board, Simulator, Admin)
- Admin UI for uploading game modules and managing FAISS index
- Starter annotated dataset (200 synthetic matches for MLBB-like schema)
- Deployment stubs: Dockerfile, docker-compose, Kubernetes manifests, GitHub Actions CI
- More scripts: fine-tune/notebooks placeholders, utilities

**Important**: This is a full-featured starter — not a finished commercial product.
To enable OpenAI integration, set the environment variable `OPENAI_API_KEY` or adjust the wrapper to use another provider.


## Updates in final package
- JWT auth demo (username: admin/adminpass, user/userpass)
- Login & token storage in frontend
- Chat history saved in localStorage
- Dataset generator (CSV) at backend/scripts/generate_dataset.py
- Monitoring endpoint /metrics (Prometheus)
- Basic pytest tests in tests/ and CI updated to run them
