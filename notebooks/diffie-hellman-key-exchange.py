import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo


@app.cell
def _():
    P = 17
    G = 5
    SECRET = 0
    RECEIVED_MESSAGE = 8
    return G, P, RECEIVED_MESSAGE, SECRET


@app.cell
def _():
    lang_switch = mo.ui.dropdown(
        label="Language",
        options={"Deutsch/German": "de", "English": "en"},
        value="Deutsch/German",
    )
    return (lang_switch,)


@app.cell
def _(g_field, lang_switch, p_field):
    mo.md(
        f"""
    # Diffie-Hellman Schlüsselaustausch
    {lang_switch}

    Diese App soll euch bei den Berechnungen zum Austausch eines Schlüssels nach Diffie-Hellman unterstützen. Tragt einfach die jeweiligen Werte in die Textfelder ein. Die App berechnet dann die Nachricht für euren Partner und das gemeinsame Geheimnis für euch.

    ## Öffentliche Parameter
    {g_field}</br>
    {p_field}
    """
    )
    return


@app.cell
def _(G, P):
    p_field = mo.ui.text(
        value=str(P),
        label="p = ",
    )
    g_field = mo.ui.text(
        value=str(G),
        label="g = ",
    )
    return g_field, p_field


@app.cell
def _(SECRET):
    secret_field = mo.ui.text(value=str(SECRET), label="Geheimnis = ")
    return (secret_field,)


@app.cell
def _(secret_field):
    mo.md(
        f"""
    ## Geheimnis
    {secret_field}

    Das Geheimnis wird euch an der Station mitgeteilt
    """
    )
    return


@app.cell
def _(g, p, secret):
    message = (g**secret) % p
    return (message,)


@app.cell
def _(message):
    mo.md(
        f"""
    ## Nachricht für Partner

    Die Nachricht für euren Partner lautet: **{message}**. Diese Nachricht kann über den unsicheren Kanal an euren Partner weitergegeben werden.
    """
    )
    return


@app.cell
def _(RECEIVED_MESSAGE):
    received_message_field = mo.ui.text(
        value=str(RECEIVED_MESSAGE), label="Empfangene Nachricht = "
    )
    return (received_message_field,)


@app.cell
def _(p, received_message, secret):
    shared_secret = (received_message**secret) % p
    return (shared_secret,)


@app.cell
def _(received_message_field, shared_secret):
    mo.md(
        f"""
    ## Geteiltes Geheimnis
    Bitte tragt hier die Nachricht ein, die ihr von eurem Partner erhalten habt:

    {received_message_field}

    Euer geteiltes Geheimnis ist damit: **{shared_secret}**. Dieses geteilte Geheimnis kann nun als Schlüssel für weitere kryptographische Verfahren verwendet werden.
    """
    )
    return


@app.cell
def _(P, p_field):
    try:
        p = int(p_field.value)
        _message = None
    except ValueError:
        p = P
        _message = mo.callout(
            value=f"p konnte nichg eingelesen werden. Es wird der Default ({P}) verwendet.",
            kind="danger",
        )

    _message  # pyright: ignore[reportUnusedExpression]
    return (p,)


@app.cell
def _(G, g_field):
    try:
        g = int(g_field.value)
        _message = None
    except ValueError:
        g = G
        _message = mo.callout(
            value=f"g konnte nichg eingelesen werden. Es wird der Default ({G}) verwendet.",
            kind="danger",
        )

    _message  # pyright: ignore[reportUnusedExpression]
    return (g,)


@app.cell
def _(SECRET, secret_field):
    try:
        secret = int(secret_field.value)
        _message = None
    except ValueError:
        secret = SECRET
        _message = mo.callout(
            value=f"Das Geheimnis konnte nichg eingelesen werden. Es wird der Default ({SECRET}) verwendet.",
            kind="danger",
        )

    _message  # pyright: ignore[reportUnusedExpression]
    return (secret,)


@app.cell
def _(RECEIVED_MESSAGE, received_message_field):
    try:
        received_message = int(received_message_field.value)
        _message = None
    except ValueError:
        received_message = RECEIVED_MESSAGE
        _message = mo.callout(
            value=f"Die empfangene Nachricht konnte nichg eingelesen werden. Es wird der Default ({RECEIVED_MESSAGE}) verwendet.",
            kind="danger",
        )

    _message  # pyright: ignore[reportUnusedExpression]
    return (received_message,)


if __name__ == "__main__":
    app.run()
