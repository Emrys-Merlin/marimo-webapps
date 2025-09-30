.PHONY: build
build:
	uv run python build.py

.PHONY: serve
serve:
	uv run python -m http.server 8000 -d _site
