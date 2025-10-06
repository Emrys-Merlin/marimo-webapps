import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")

with app.setup:
    import json
    from collections import Counter
    from math import ceil

    import altair as alt
    import marimo as mo
    import pandas as pd


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
    with open(public_dir / "substitution_cipher.json") as f:
        lang_dicts = json.load(f)
    return (lang_dicts,)


@app.cell
def _(lang_dicts, lang_selector):
    try:
        lang_dict: dict[str, str] = lang_dicts[lang_selector.value]
    except KeyError:
        lang_dict: dict[str, str] = lang_dicts["de"]
    return (lang_dict,)


@app.cell
def _(lang_dict: dict[str, str]):
    CHIFFRE = lang_dict["cipher"]
    LINK = lang_dict["link"]
    LETTER_COL = lang_dict["letter_col"]
    FREQUENCY_COL = lang_dict["frequency_col"]
    N_COLS = 2
    return CHIFFRE, FREQUENCY_COL, LETTER_COL, LINK, N_COLS


@app.cell
def _(lang_dict: dict[str, str]):
    mo.md(lang_dict["title"])
    return


@app.cell
def _(CHIFFRE, clear_text, lang_dict: dict[str, str]):
    clear_text_area = mo.ui.text_area(
        value=clear_text,
        disabled=True,
        full_width=True,
        label=lang_dict["message_title"],
    ).style(width="50%")
    chiffre_text_area = mo.ui.text_area(
        value=CHIFFRE,
        disabled=False,
        full_width=True,
        label=lang_dict["cipher_title"],
    ).style(width="50%")

    mo.hstack(
        [chiffre_text_area, clear_text_area],
        align="stretch",
        justify="center",
    )
    return


@app.cell
def _():
    n_alphabet = 26
    return (n_alphabet,)


@app.cell
def _(e_subst, n_alphabet):
    _fields: dict[str, mo.ui.text] = {}

    for _i in range(n_alphabet):
        _c = chr(ord("A") + _i)
        _fields[_c] = mo.ui.text(
            max_length=1, label=f"{_c} =", value="E" if _c == e_subst else ""
        )

    fields = mo.ui.dictionary(_fields)  # pyright: ignore[reportArgumentType]
    return (fields,)


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
    ).style(max_width="60%", overflow="auto")
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
def _(CHIFFRE, FREQUENCY_COL, LETTER_COL, n_alphabet):
    _counter = Counter(CHIFFRE)
    _counts = [
        {
            LETTER_COL: chr(ord("A") + _i),
            FREQUENCY_COL: _counter.get(chr(ord("A") + _i), 0),
        }
        for _i in range(n_alphabet)
    ]

    chiffre_count = pd.DataFrame(_counts)
    return (chiffre_count,)


@app.cell
def _(FREQUENCY_COL, LETTER_COL, chiffre_count):
    _idx = chiffre_count[FREQUENCY_COL].idxmax()
    e_subst = chiffre_count.loc[_idx, LETTER_COL]
    return (e_subst,)


@app.cell
def _(FREQUENCY_COL, LETTER_COL, chiffre_count, lang_dict: dict[str, str]):
    _chart = (
        alt.Chart(chiffre_count)
        .mark_bar()
        .encode(
            x=LETTER_COL,
            y=alt.Y(FREQUENCY_COL, title=f"{FREQUENCY_COL} (absolut)"),
        )
        .properties(title=lang_dict["count_plot_title"])
    )

    chiffre_plot = mo.ui.altair_chart(_chart)
    return (chiffre_plot,)


@app.cell
def _(lang_dict: dict[str, str], public_dir):
    frequency_fn = public_dir / lang_dict["frequency_fn"]
    return (frequency_fn,)


@app.cell
def _(frequency_fn):
    df = pd.read_csv(frequency_fn)
    return (df,)


@app.cell
def _(FREQUENCY_COL, LETTER_COL, df, lang_dict: dict[str, str]):
    _chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=LETTER_COL, y=alt.Y(FREQUENCY_COL, title=f"{FREQUENCY_COL} [%]"))
        .properties(title=lang_dict["frequency_plot_title"])
    )

    frequency_plot = mo.ui.altair_chart(_chart)
    return (frequency_plot,)


@app.cell
def _(LINK, frequency_plot, lang_dict: dict[str, str]):
    _source = lang_dict["source"]
    frequency_compose = mo.md(f"""\
    {frequency_plot}
    {_source}: [Wikipedia]({LINK})
    """)
    return (frequency_compose,)


@app.cell
def _(lang_dict: dict[str, str]):
    mo.md(lang_dict["additional_infos"])
    return


@app.cell
def _(chiffre_plot, frequency_compose, lang_dict: dict[str, str]):
    mo.accordion(
        {
            lang_dict["count_plot_intro"]: chiffre_plot,
            lang_dict["frequency_plot_intro"]: frequency_compose,
        },
        multiple=True,
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
