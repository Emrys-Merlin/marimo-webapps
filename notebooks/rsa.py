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
    n_input = mo.ui.text(value=str(N), label="N = ")
    e_input = mo.ui.text(value=str(E), label="e = ")
    c_input = mo.ui.text(value=str(C), label="c = ")

    button = mo.ui.button(label="Weiter", value=False, on_click=lambda value: True)
    phi_button = mo.ui.button(label="Weiter", value=False, on_click=lambda value: True)
    d_button = mo.ui.button(label="Weiter", value=False, on_click=lambda value: True)
    c_button = mo.ui.button(label="Weiter", value=False, on_click=lambda value: True)
    return button, c_button, c_input, d_button, e_input, n_input, phi_button


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
def _(button, e_input, n_input):
    mo.md(
        f"""
    # RSA knacken

    Diese Website führt euch Schritt für Schritt durch den Prozess die RSA-Verschlüsselung zu knacken.

    Zunächst benötigen wir die öffentlichen Parameter der Verschlüsselung. Das sind $N$ und $e$.

    {n_input}</br>
    {e_input}</br>
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
def _(p, phi_button, q):
    mo.md(
        f"""
    ## Berechnet die Primfaktorzerlegung von $N$

    Der erste Schritt und auch der einzige Schritt, der einen Quantencomputer benötigt, ist die Primfaktorzerlegung von $N$. Für unser Beispiel haben wir ein $N$ gewählt, das noch klein genug ist, dass auch ein klassischer Algorithmus die Primfaktoren finden kann. Diese sind:

    p = {p}</br>
    q = {q}

    {phi_button}
    """
    )
    return


@app.cell
def _(p, phi_button, q):
    mo.stop(not phi_button.value)

    phi = (p - 1) * (q - 1)
    return (phi,)


@app.cell
def _(d_button, phi):
    mo.md(
        rf"""
    ## Berechnet die Phi-Funktion von $N$: $\varphi(N)$

    Die [Euler’sche Phi-Funktion](https://de.wikipedia.org/wiki/Eulersche_Phi-Funktion) zählt wie viele der Zahlen zwischen 1 und N teilerfremd zu N sind. Das ist wichtig für uns, weil $e$ teilerfremd zu N sein muss und unser privater Schlüssel $d$ auch. Diese Zahlen haben besondere Eigenscaften, die sich der RSA-Algorithmus zu Nutze macht. $\varphi(N)$ wird uns helfen aus $e$ den Schlüssel $d$ zu berechnen.

    Die Formel für $\varphi(N)$ ist Dank unserer Primfaktorzerlegung von $N$ ganz einfach zu berechnen:

    $\varphi(N) = (p - 1) \cdot (q - 1) = {phi}$

    {d_button}
    """
    )
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
def _(d):
    _text = r"""
    ## Berechnet den geheimen Schlüssel (private key) $d$

    Symbolisch ist die Formel für $d$ gegeben durch

    $$
    d = e^{{-1}} \operatorname{{mod}} \varphi(n).
    $$

    Wenn man $d$ tatsächlich berechnen möchte, benutzt man dafür den [erweiterten euklidischen Algorithmus](https://de.wikipedia.org/wiki/Erweiterter_euklidischer_Algorithmus). Damit ergibt sich

    $$
    d = {d}
    $$
    """.format(d=d)
    mo.md(_text)
    return


@app.cell
def _(c_button, c_input, d_button):
    mo.stop(not d_button.value and not c_button.value)

    mo.md(
        rf"""
    ## Entschlüsseln der geheimen Nachricht $c$

    Dazu benötigen wir zunächst die Nachricht:

    {c_input}

    {c_button}
    """
    )
    return


@app.cell
def _(c, d, n):
    m = pow_mod(c, d, n)
    return (m,)


@app.cell
def _(c_button, m):
    mo.stop(not c_button.value)

    _text = r"""
    Die Klartext-Nachricht erhalten wir durch potenzieren mit dem geheimen Schlüssel $d$ und Rest-Rechnung mit dem öffentlichen Parameter $N$. Als Formel schreibt sich das als:

    $$
    m = c^d \operatorname{{mod}} N
    $$

    In der Anwendung lässt sich diese Operation mit dem [binären Exponentations-Algorithmus](https://de.wikipedia.org/wiki/Bin%C3%A4re_Exponentiation#Bin%C3%A4re_Modulo-Exponentiation) (auch Square-and-Multiply genannt) durchführen und man erhält:

    $$
    m = {m}
    $$
    """.format(m=m)

    mo.md(_text)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
