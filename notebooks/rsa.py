import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")

with app.setup:
    import json
    from math import ceil, sqrt

    import marimo as mo


@app.cell
def _():
    lang_selector = mo.ui.dropdown(
        options={
            "Deutsch/German": "de",
            "English": "en",
        },
        value="Deutsch/German",
    )
    return (lang_selector,)


@app.cell
def _(lang_selector):
    lang_selector
    return


@app.cell
def _():
    _dir = mo.notebook_location()
    assert _dir is not None
    public_dir = _dir / "public"
    return (public_dir,)


@app.cell
def _(public_dir):
    with open(public_dir / "rsa.json") as f:
        lang_dicts = json.load(f)
    return (lang_dicts,)


@app.cell
def _(lang_dicts, lang_selector):
    try:
        lang_dict = lang_dicts[lang_selector.value]
    except KeyError:
        lang_dict = lang_dicts["de"]
    return (lang_dict,)


@app.cell
def _():
    N = 2463519511
    E = 84673
    C = 2031691875
    return C, E, N


@app.function
def factorize(n: int) -> list[int]:
    threshold = ceil(sqrt(n))
    for i in [2] + list(range(3, threshold + 1, 2)):
        if n % i == 0:
            return factorize(n // i) + [i]

    return [n]


@app.function
def extended_euclidean(m: int, n: int) -> tuple[int, int, int]:
    if m == 0:
        return n, 0, 1

    gcd, x1, y1 = extended_euclidean(n % m, m)

    x = y1 - (n // m) * x1
    y = x1

    return gcd, x, y


@app.function
def pow_mod(base: int, exp: int, mod: int) -> int:
    exp_binary = bin(exp)[2:]  # Ignor '0b' prefix
    res = 1
    for c in exp_binary:
        res = (res * res) % mod
        if c == "1":
            res = (res * base) % mod

    return res


@app.cell
def _(C, E, N):
    n_input = mo.ui.text(value=str(N), label="N = ")
    e_input = mo.ui.text(value=str(E), label="e = ")
    c_input = mo.ui.text(value=str(C), label="c = ")
    return c_input, e_input, n_input


@app.cell
def _(lang_dict):
    button = mo.ui.button(
        label=lang_dict["next"], value=False, on_click=lambda value: True
    )
    phi_button = mo.ui.button(
        label=lang_dict["next"], value=False, on_click=lambda value: True
    )
    d_button = mo.ui.button(
        label=lang_dict["next"], value=False, on_click=lambda value: True
    )
    c_button = mo.ui.button(
        label=lang_dict["next"], value=False, on_click=lambda value: True
    )
    return button, c_button, d_button, phi_button


@app.cell
def _(C, E, N, c_input, e_input, n_input):
    try:
        n = int(n_input.value)
    except ValueError:
        n = N

    try:
        e = int(e_input.value)
    except ValueError:
        e = E

    try:
        c = int(c_input.value)
    except ValueError:
        c = C
    return c, e, n


@app.cell
def _(button, e_input, lang_dict, n_input):
    mo.md(lang_dict["title"].format(n_input=n_input, e_input=e_input, button=button))
    return


@app.cell
def _(button, n):
    mo.stop(not button.value)

    primes = factorize(n)

    res = None
    if len(primes) != 2:
        res = mo.callout(
            f"n has {len(primes)} instead of 2 prime factors. Please check n.",
            kind="danger",
        )
        p, q = 0, 0
    else:
        p, q = primes

    res  # pyright: ignore[reportUnusedExpression]
    return p, q


@app.cell
def _(lang_dict, p, phi_button, q):
    mo.md(lang_dict["prime_factors"].format(p=p, q=q, phi_button=phi_button))
    return


@app.cell
def _(p, phi_button, q):
    mo.stop(not phi_button.value)

    phi = (p - 1) * (q - 1)
    return (phi,)


@app.cell
def _(d_button, lang_dict, phi):
    mo.md(lang_dict["phi_function"].format(d_button=d_button, phi=phi))
    return


@app.cell
def _(d_button, e, phi):
    mo.stop(not d_button.value)

    gcd, _d, _ = extended_euclidean(e, phi)

    assert gcd == 1

    if _d >= 0:
        d = _d
    else:
        _scale = ceil(abs(_d) / phi)
        d = _d + _scale * phi
    return (d,)


@app.cell
def _(d, lang_dict):
    mo.md(lang_dict["private_key"].format(d=d))
    return


@app.cell
def _(c_button, c_input, d_button, lang_dict):
    mo.stop(not d_button.value and not c_button.value)

    mo.md(lang_dict["cipher"].format(c_input=c_input, c_button=c_button))
    return


@app.cell
def _(c, d, n):
    m = pow_mod(c, d, n)
    return (m,)


@app.cell
def _(c_button, lang_dict, m):
    mo.stop(not c_button.value)

    mo.md(lang_dict["solution"].format(m=m))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
