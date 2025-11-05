import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")

with app.setup:
    from typing import Annotated
    from math import isnan

    import marimo as mo


@app.cell
def _():
    sensitivity_field = mo.ui.text(
        label="Sensitivity",
        value="0.995",
    )
    return (sensitivity_field,)


@app.cell
def _():
    specificity_field = mo.ui.text(
        label="Specificity",
        value="0.9",
    )
    return (specificity_field,)


@app.cell
def _():
    prevalence_field = mo.ui.text(
        label="Prevalence",
        value="0.005",
    )
    return (prevalence_field,)


@app.cell
def _(sensitivity_field):
    try:
        sensitivity: float | None = min(max(float(sensitivity_field.value), 0.0), 1.0)
    except ValueError:
        sensitivity = None
    return (sensitivity,)


@app.cell
def _(specificity_field):
    try:
        specificity: float | None = min(max(float(specificity_field.value), 0.0), 1.0)
    except ValueError:
        specificity = None
    return (specificity,)


@app.cell
def _(prevalence_field):
    try:
        prevalence: float | None = min(max(float(prevalence_field.value), 0.0), 1.0)
    except ValueError:
        prevalence = None
    return (prevalence,)


@app.function
def to_ppv_npv(
    *,
    sensitivity: float | None,
    specificity: float | None,
    prevalence: float | None,
) -> tuple[
    Annotated[float, "PPV"],
    Annotated[float, "NPV"],
]:
    if sensitivity is None or specificity is None or prevalence is None:
        return float("nan"), float("nan")

    ppv = (
        sensitivity
        * prevalence
        / (sensitivity * prevalence + (1 - specificity) * (1 - prevalence))
    )
    npv = (
        specificity
        * (1 - prevalence)
        / (specificity * (1 - prevalence) + (1 - sensitivity) * prevalence)
    )
    return ppv, npv


@app.cell
def _(
    prevalence: float | None,
    sensitivity: float | None,
    specificity: float | None,
):
    ppv, npv = to_ppv_npv(
        sensitivity=sensitivity,
        specificity=specificity,
        prevalence=prevalence,
    )
    return npv, ppv


@app.cell
def _(
    npv,
    ppv,
    prevalence: float | None,
    prevalence_field,
    sensitivity: float | None,
    sensitivity_field,
    specificity: float | None,
    specificity_field,
):
    mo.md(
        f"""
    # Positive and negative predictive values

    Please enter the sensitivity, specificity, and prevalence as a value between 0 and 1. Values outside that range will be clamped to that range.

    ## Inputs
    {sensitivity_field} = {sensitivity:.1%}

    {specificity_field} = {specificity:.1%}

    {prevalence_field} = {prevalence:.1%}

    ## Outputs
    Positive predictive value (PPV): {ppv:.3f} = {ppv:.1%}

    Negative predictive value (NPV): {npv:.3f} = {npv:.1%}
    """
    )
    return


@app.cell
def _():
    def test_to_ppv_npv_none_input():
        for sens, spec, prev in [
            (None, 0.9, 0.05),
            (0.99, None, 0.05),
            (0.99, 0.9, None),
        ]:
            ppv, npv = to_ppv_npv(
                sensitivity=sens,
                specificity=spec,
                prevalence=prev,
            )

            assert isnan(ppv)
            assert isnan(npv)

    def test_to_ppv_npv_valid():
        sens = 0.5
        spec = 0.5
        prev = 0.5
        ref_ppv = 0.5
        ref_npv = 0.5

        ppv, npv = to_ppv_npv(
            sensitivity=sens,
            specificity=spec,
            prevalence=prev,
        )

        assert ppv == ref_ppv
        assert npv == ref_npv

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
