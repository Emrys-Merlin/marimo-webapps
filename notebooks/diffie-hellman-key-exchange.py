import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")

with app.setup:
    import json
    from urllib.request import urlopen

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
    lang_selector = mo.ui.dropdown(
        # label="Language",
        options={
            "Deutsch/German": "de",
            "English": "en",
        },
        value="Deutsch/German",
    )
    return (lang_selector,)


@app.cell
def _(lang_selector):
    lang_selector  # pyright: ignore[reportUnusedExpression]
    return


@app.cell
def _():
    _dir = mo.notebook_location()
    assert _dir is not None
    public_dir = _dir / "public"
    return (public_dir,)


@app.cell
def _(public_dir):
    try:
        with open(public_dir / "dhkx.json") as f:
            lang_dicts = json.load(f)
    except:  # noqa: E722
        with urlopen(public_dir / "dhkx.json") as f:
            lang_dicts = json.load(f)
    return (lang_dicts,)


@app.cell
def _(lang_dicts, lang_selector):
    try:
        lang_dict: dict[str, str] = lang_dicts[lang_selector.value]  # pyright: ignore[reportRedeclaration]
    except KeyError:
        # Hack: In WASM case need to load via URL not on local file...
        lang_dict: dict[str, str] = lang_dicts["de"]
    return (lang_dict,)


@app.cell
def _(lang_dict: dict[str, str]):
    exchange_button = mo.ui.button(
        label=lang_dict["button_exchange"],
        value=False,
        on_click=lambda value: True,
    )
    secret_button = mo.ui.button(
        label=lang_dict["button_secret"],
        value=False,
        on_click=lambda value: True,
    )
    return exchange_button, secret_button


@app.cell
def _(g_field, lang_dict: dict[str, str], p_field):
    mo.md(lang_dict["intro"].format(g_field=g_field, p_field=p_field))
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
def _(exchange_button, lang_dict: dict[str, str], secret_field):
    mo.md(
        lang_dict["secret"].format(
            secret_field=secret_field, exchange_button=exchange_button
        )
    )
    return


@app.cell
def _(g, p, secret):
    message = (g**secret) % p
    return (message,)


@app.cell
def _(RECEIVED_MESSAGE):
    received_message_field = mo.ui.text(
        value=str(RECEIVED_MESSAGE), label="Empfangene Nachricht = "
    )
    return (received_message_field,)


@app.cell
def _(
    exchange_button,
    lang_dict: dict[str, str],
    message,
    received_message_field,
    secret_button,
):
    mo.stop(not exchange_button.value and not secret_button.value)

    mo.md(
        lang_dict["exchange"].format(
            message=message,
            received_message_field=received_message_field,
            secret_button=secret_button,
        )
    )
    return


@app.cell
def _(p, received_message, secret):
    shared_secret = (received_message**secret) % p
    return (shared_secret,)


@app.cell
def _(lang_dict: dict[str, str], secret_button, shared_secret):
    mo.stop(not secret_button.value)

    mo.md(lang_dict["shared"].format(shared_secret=shared_secret))
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
