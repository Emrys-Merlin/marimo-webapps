import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")

with app.setup:
    import json
    from urllib.request import urlopen

    import marimo as mo


@app.cell
def _():
    _dir = mo.notebook_location()
    assert _dir is not None

    public_dir = _dir / "public"
    return (public_dir,)


@app.cell
def _(public_dir):
    # This throws a FileNotFound error after the WASM export
    with open(public_dir / "test.json") as _f:
        _ = json.load(_f)
    return


@app.cell
def _(public_dir):
    # This is my current workaround
    try:
        with open(public_dir / "test.json") as _f:
            _ = json.load(_f)
    except FileNotFoundError:
        with urlopen(public_dir / "test.json") as _f:
            _ = json.load(_f)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
