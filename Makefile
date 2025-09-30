.PHONY: build
build:
	uv run python build.py

.PHONY: serve
serve:
	uv run python -m http.server 8000 -d _site


.PHONY: install-uv
install-uv:
	@command -v uv >/dev/null 2>&1 && echo "uv already installed" || curl -LsSf https://astral.sh/uv/install.sh | sh


.PHONY: build-cloudflare
build-cloudflare: install-uv build
