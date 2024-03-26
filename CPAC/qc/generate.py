"""Generate an RBC-style QC CSV."""

from io import BufferedReader
import os
import re

import numpy as np
import pandas as pd
import nibabel as nib

from CPAC.qc.qcmetrics import regisQ


# This function is for a function node for which
# Nipype will connect many other nodes as inputs
def generate_xcp_qc(  # noqa: PLR0913
    sub,
    ses,
    task,
    run,
    desc,
    regressors,
    bold2t1w_mask,
    t1w_mask,
    bold2template_mask,
    template_mask,
    original_func,
    final_func,
    movement_parameters,
    dvars,
    censor_indices,
    framewise_displacement_jenkinson,
    dvars_after,
    template,
):
    """Generate an RBC-style QC CSV.

    Parameters
    ----------
    sub : str
        subject ID

    ses : str
        session ID

    task : str
        task ID

    run : str or int
        run ID

    desc : str
        description string

    regressors : str
        'Name' of regressors in fork

    original_func : str
        path to original 'bold' image

    final_bold : str
        path to 'space-template_desc-preproc_bold' image

    bold2t1w_mask : str
        path to bold-to-T1w transform applied to space-bold_desc-brain_mask
        with space-T1w_desc-brain_mask reference

    t1w_mask : str
        path to space-T1w_desc-brain_mask

    bold2template_mask : str
        path to space-template_desc-bold_mask

    template_mask : str
        path to T1w-brain-template-mask or EPI-template-mask

    movement_parameters: str
        path to movement parameters

    dvars : str
        path to DVARS before motion correction

    censor_indices : list
        list of indices of censored volumes

    framewise_displacement_jenkinson : str
        path to framewise displacement (Jenkinson) before motion correction

    dvars_after : str
        path to DVARS on final 'bold' image

    template : str
        path to registration template

    Returns
    -------
    str
        path to space-template_desc-xcp_quality TSV
    """
    from CPAC.qc.xcp import dvcorr

    columns = (
        "sub,ses,task,run,desc,regressors,space,meanFD,relMeansRMSMotion,"
        "relMaxRMSMotion,meanDVInit,meanDVFinal,nVolCensored,nVolsRemoved,"
        "motionDVCorrInit,motionDVCorrFinal,coregDice,coregJaccard,"
        "coregCrossCorr,coregCoverage,normDice,normJaccard,normCrossCorr,"
        "normCoverage".split(",")
    )

    images = {
        "original_func": nib.load(original_func),
        "final_func": nib.load(final_func),
    }

    # `sub` through `space`
    from_bids = {
        "sub": sub,
        "ses": ses,
        "task": task,
        "run": run,
        "desc": desc,
        "regressors": regressors,
        "space": os.path.basename(template).split(".", 1)[0].split("_", 1)[0],
    }
    if from_bids["space"].startswith("tpl-"):
        from_bids["space"] = from_bids["space"][4:]

    # `nVolCensored` & `nVolsRemoved`
    n_vols_censored = len(censor_indices) if censor_indices is not None else "unknown"
    shape_params = {
        "nVolCensored": n_vols_censored,
        "nVolsRemoved": images["original_func"].shape[3]
        - images["final_func"].shape[3],
    }

    if isinstance(final_func, BufferedReader):
        final_func = final_func.name
    qc_filepath = os.path.join(os.getcwd(), "xcpqc.tsv")

    desc_span = re.search(r"_desc-.*_", final_func)
    if desc_span:
        desc_span = desc_span.span()
        final_func = "_".join([final_func[: desc_span[0]], final_func[desc_span[1] :]])
    del desc_span

    # `meanFD (Jenkinson)`
    power_params = {"meanFD": np.mean(np.loadtxt(framewise_displacement_jenkinson))}

    # `relMeansRMSMotion` & `relMaxRMSMotion`
    mot = np.genfromtxt(movement_parameters).T
    # Relative RMS of translation
    rms = np.sqrt(mot[3] ** 2 + mot[4] ** 2 + mot[5] ** 2)
    rms_params = {"relMeansRMSMotion": [np.mean(rms)], "relMaxRMSMotion": [np.max(rms)]}

    # `meanDVInit` & `meanDVFinal`
    meanDV = {"meanDVInit": np.mean(np.loadtxt(dvars))}
    try:
        meanDV["motionDVCorrInit"] = dvcorr(dvars, framewise_displacement_jenkinson)
    except ValueError as value_error:
        meanDV["motionDVCorrInit"] = f"ValueError({value_error!s})"
    meanDV["meanDVFinal"] = np.mean(np.loadtxt(dvars_after))
    try:
        meanDV["motionDVCorrFinal"] = dvcorr(
            dvars_after, framewise_displacement_jenkinson
        )
    except ValueError as value_error:
        meanDV["motionDVCorrFinal"] = f"ValueError({value_error!s})"

    # Overlap
    overlap_params = regisQ(
        bold2t1w_mask=bold2t1w_mask,
        t1w_mask=t1w_mask,
        bold2template_mask=bold2template_mask,
        template_mask=template_mask,
    )

    qc_dict = {
        **from_bids,
        **power_params,
        **rms_params,
        **shape_params,
        **overlap_params,
        **meanDV,
    }
    df = pd.DataFrame(qc_dict, columns=columns)
    df.to_csv(qc_filepath, sep="\t", index=False)
    return qc_filepath
