import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")

with app.setup:
    from collections import Counter
    from math import ceil

    import altair as alt
    import marimo as mo
    import pandas as pd


@app.cell
def _():
    CHIFFRE = "BIGZATFBIP OAHIFCVHPNFB. TBG BWRS DTI WHQOWRI OIAKINS HPD IHFB DIP BTPVITN WHQ DIP PWIFBNSIP KGS JIGDTIPS. DTI NSWSTKP TNS TU CIAAIG. JTIA NEWNN HPD IGQKAO!"
    N_COLS = 2
    LINK = "https://de.wikipedia.org/wiki/Buchstabenh%C3%A4ufigkeit"
    return CHIFFRE, LINK, N_COLS


@app.cell
def _():
    mo.md(
        """
    # Substitutions-Chiffre

    Bitte entschlüsselt den folgenden Text:
    """
    )
    return


@app.cell
def _(CHIFFRE, clear_text):
    clear_text_area = mo.ui.text_area(
        value=clear_text,
        disabled=True,
        full_width=True,
        label="Klartext",
    ).style(width="50%")
    chiffre_text_area = mo.ui.text_area(
        value=CHIFFRE,
        disabled=True,
        full_width=True,
        label="Chiffre",
    ).style(width="50%")

    mo.hstack(
        [chiffre_text_area, clear_text_area],
        align="stretch",
        justify="center",
    )
    return


@app.cell
def _():
    _fields: dict[str, mo.ui.text] = {}

    n_alphabet = 26

    for _i in range(n_alphabet):
        _c = chr(ord("A") + _i)
        _fields[_c] = mo.ui.text(
            max_length=1, label=f"{_c} =", value="E" if _c == "I" else ""
        )

    fields = mo.ui.dictionary(_fields)  # pyright: ignore[reportArgumentType]
    return fields, n_alphabet


@app.cell
def _(N_COLS, fields, n_alphabet):
    _switch = ceil(n_alphabet / N_COLS)
    _cols = [list() for _ in range(N_COLS)]

    for _i in range(n_alphabet):
        _c = chr(ord("A") + _i)
        col_idx = _i // _switch
        _cols[col_idx].append(fields[_c])

    mo.hstack(
        [
            mo.vstack(
                col,
                # justify="start",
                align="end",
            )
            for col in _cols
        ],
        justify="start",
        # align="end"
    ).style(max_width="50%", overflow="auto")
    return


@app.cell
def _(fields):
    mapping = {
        c: field.value.lower() if field.value != "" else "-"
        for c, field in fields.items()
    }
    return (mapping,)


@app.cell
def _(CHIFFRE, mapping):
    clear_text = "".join(mapping.get(c, c) for c in CHIFFRE).upper()
    return (clear_text,)


@app.cell
def _(CHIFFRE, n_alphabet):
    _counter = Counter(CHIFFRE)
    _counts = [
        {
            "Buchstabe": chr(ord("A") + _i),
            "Häufigkeit": _counter.get(chr(ord("A") + _i), 0),
        }
        for _i in range(n_alphabet)
    ]

    chiffre_count = pd.DataFrame(_counts)
    return (chiffre_count,)


@app.cell
def _(chiffre_count):
    _chart = (
        alt.Chart(chiffre_count)
        .mark_bar()
        .encode(x="Buchstabe", y=alt.Y("Häufigkeit", title="Häufigkeit (absolut)"))
        .properties(title="Buchstabenhäufigkeit in der Chiffre")
    )

    chiffre_plot = mo.ui.altair_chart(_chart)
    return (chiffre_plot,)


@app.cell
def _():
    _dir = mo.notebook_location()
    assert _dir is not None
    frequency_fn = _dir / "public/frequency_german.csv"
    return (frequency_fn,)


@app.cell
def _(frequency_fn):
    df = pd.read_csv(frequency_fn)
    return (df,)


@app.cell
def _(df):
    _chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x="Buchstabe", y=alt.Y("Häufigkeit", title="Häufigkeit [%]"))
        .properties(title="Buchstabenhäufigkeit in deutschen Texten")
    )

    frequency_plot = mo.ui.altair_chart(_chart)
    return (frequency_plot,)


@app.cell
def _(LINK, frequency_plot):
    frequency_compose = mo.md(f"""\
    {frequency_plot}
    Quelle: [Wikipedia]({LINK})
    """)
    return (frequency_compose,)


@app.cell
def _():
    mo.md("Macht euch dazu gerne die folgenden Informationen zu Nutze:")
    return


@app.cell
def _(chiffre_plot, frequency_compose):
    mo.accordion(
        {
            "Buchstabenhäufigkeit in der Chiffre": chiffre_plot,
            "Buchstabenhäufigkeit in deutschen Texten": frequency_compose,
        },
        multiple=True,
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
