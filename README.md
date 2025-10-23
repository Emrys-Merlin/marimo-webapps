# My marimo-based web app collection

For some of my projects, I like to share visualizations or simple computations. As I am most familiar with the python ecosystem, I was really excited when I first came across [marimo](https://marimo.io), which is a notebook tool for work in python, but the notebooks [can be compiled to WebAssembly](https://docs.marimo.io/guides/wasm/). This simplifies deployment a lot, because you can simply use GitHub or Cloudflare pages to host the notebooks.

As a proof-of-concept, I created some notebooks that I used during a cryptography-inspired scavenger hunt my wife and I organized in May 2025. You can find an accompanying blog post [here](https://commutativewith.one/blog-posts/crypto-scavenger-hunt).

You can find the deployed webapps under `https://notebooks.commutativewith.one/<notebook_name>` (without the file extension). Currently, there is no index.

## Building the WASM notebooks

This project uses [uv](https://github.com/astral-sh/uv). If it is already installed on your system, the build process is as easy as `make build`, which internally simply calls `uv run python build.py`. Marimo does all the heavy lifting. The WASM notebooks will be stored in `./_site`, which is excluded from version control.

I automated my deployment using [cloudflare pages](https://pages.cloudflare.com/). The build worker does not have `uv` installed by default, so there is an extra build command `make build-cloudflare`, which installs `uv` first.

## Local deployment

For local testing, you can serve the WASM notebooks stored in `./_site` via `make serve`. Afterward, they are available on https://localhost:8000. You need to make sure that port 8000 is free or tweak the make subcommand.
