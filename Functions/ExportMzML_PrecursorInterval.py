from pyopenms import *

def ExportMzML_PrecursorInterval(mzML_path: str,
                                 mzML_out_path: str,
                                 mz_interval: tuple[float, float],
                                 copy_chromatograms: bool = True) -> dict:
    """
    Export a new mzML containing only MS2 spectra whose precursor m/z
    lies inside mz_interval = (mz_min, mz_max).
    """

    Exp = oms.MSExperiment()
    oms.MzMLFile().load(mzML_path, Exp)

    SpectraFiltered = SliceSpectra_ByPrecursorMZ(
        Exp,
        mz_min=mz_interval[0],
        mz_max=mz_interval[1]
    )

    ExpNew = oms.MSExperiment()
    ExpNew.setExperimentalSettings(Exp.getExperimentalSettings())

    if copy_chromatograms:
        try:
            ExpNew.setChromatograms(Exp.getChromatograms())
        except Exception:
            pass

    ExpNew.setSpectra(SpectraFiltered)

    try:
        ExpNew.sortSpectra(True)
    except Exception:
        pass

    oms.MzMLFile().store(mzML_out_path, ExpNew)

    return {
        "mzML_in": mzML_path,
        "mzML_out": mzML_out_path,
        "mz_interval": mz_interval,
        "N_spectra_in": len(Exp.getSpectra()),
        "N_spectra_out": len(SpectraFiltered),
    }
