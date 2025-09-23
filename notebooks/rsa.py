import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")

with app.setup:
    from math import ceil, sqrt

    import marimo as mo


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
    n_input = mo.ui.text(value=str(N), label="n = ")
    e_input = mo.ui.text(value=str(E), label="e = ")
    c_input = mo.ui.text(value=str(C), label="c = ")

    button = mo.ui.run_button(label="Run")
    return button, c_input, e_input, n_input


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
def _(button, c_input, e_input, n_input):
    mo.md(
        f"""
    # RSA knacken

    {n_input}</br>
    {e_input}</br>
    {c_input}</br>
    {button}
    """
    )
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
def _(n, p, q):
    mo.md(
        f"""
    ## Prime factors

    The two prime factors of n = {n} are

    p = {p}</br>
    q = {q}
    """
    )
    return


@app.cell
def _(p, q):
    phi = (p - 1) * (q - 1)
    return (phi,)


@app.cell
def _(phi):
    mo.md(
        rf"""
    # Phi function
    $\varphi(N) = (p - 1) \cdot (q - 1) = {phi}$
    """
    )
    return


@app.cell
def _(e, phi):
    gcd, _d, _ = extended_euclidean(e, phi)

    assert gcd == 1

    if _d >= 0:
        d = _d
    else:
        _scale = ceil(abs(_d) / phi)
        d = _d + _scale * phi
    return (d,)


@app.cell
def _():
    mo.md(
        r"""
    # Compute the secret key $d$
    The formula is

    $$
    d = e^{-1} \operatorname{mod} \varphi(n)
    $$
    """
    )
    return


@app.cell
def _(d):
    mo.md(rf"""This leads to $d={d}$.""")
    return


@app.cell
def _(c, d, n):
    m = pow_mod(c, d, n)
    return (m,)


@app.cell
def _():
    mo.md(
        r"""
    # Decode the cypher $c$ to get the clear text message $m$

    $$
    m = c^d \operatorname{mod} N
    $$
    """
    )
    return


@app.cell
def _(m):
    mo.md(f"""This computes to $m = {m}$.""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
