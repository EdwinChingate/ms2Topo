from ExtractMS2PrecursorMetadata import *
from pyopenms import *

def PlotMS2PrecursorDistribution(DataSetName,
                                  DataFolder,
                                  RT_units='min',
                                  figsize=(14, 10),
                                  scatter_alpha=0.3,
                                  scatter_size=2,
                                  hist_bins=80,
                                  hist_color='#2E86C1',
                                  scatter_color='#2E86C1',
                                  SaveFig=False,
                                  OutputFolder=None,
                                  OutputFigName=None):
    """
    Loads an .mzML file and generates a 4-panel figure showing:
      - Top-left:     Scatter plot of precursor m/z vs RT
      - Top-right:    Histogram of precursor m/z
      - Bottom-left:  Histogram of RT
      - Bottom-right: 2D histogram (heatmap) of m/z vs RT

    RT_units: 'min' converts RT from seconds to minutes,
              'sec' keeps original seconds.
    """
    # Step 1: Load the dataset
    DataSet = ChargeDataSet_in_AnotherFolder(
        DataSetName=DataSetName,
        DataFolder=DataFolder
    )

    # Step 2: Extract precursor metadata
    PrecursorData = ExtractMS2PrecursorMetadata(DataSet=DataSet)

    if PrecursorData.shape[0] == 0:
        print("No MS2 spectra found in this file.")
        return None

    MZValues = PrecursorData[:, 0]
    RTValues = PrecursorData[:, 1]

    # Step 3: Convert RT if requested
    if RT_units == 'min':
        RTValues = RTValues / 60.0
        RT_label = 'RT (min)'
    else:
        RT_label = 'RT (sec)'

    NumSpectra = len(MZValues)
    MZ_label = 'Precursor m/z'

    # Step 4: Build the 4-panel figure
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle(f'MS2 Precursor Distribution — {DataSetName}\n'
                 f'({NumSpectra} MS2 spectra)',
                 fontsize=14, fontweight='bold')

    # --- Top-left: Scatter m/z vs RT ---
    ax_scatter = axes[0, 0]
    ax_scatter.scatter(RTValues, MZValues,
                       alpha=scatter_alpha,
                       s=scatter_size,
                       color=scatter_color,
                       edgecolors='none')
    ax_scatter.set_xlabel(RT_label)
    ax_scatter.set_ylabel(MZ_label)
    ax_scatter.set_title('Precursor m/z vs RT')

    # --- Top-right: Histogram of m/z ---
    ax_mz_hist = axes[0, 1]
    ax_mz_hist.hist(MZValues,
                    bins=hist_bins,
                    color=hist_color,
                    edgecolor='white',
                    linewidth=0.3,
                    alpha=0.85)
    ax_mz_hist.set_xlabel(MZ_label)
    ax_mz_hist.set_ylabel('Count')
    ax_mz_hist.set_title('Precursor m/z Distribution')

    # --- Bottom-left: Histogram of RT ---
    ax_rt_hist = axes[1, 0]
    ax_rt_hist.hist(RTValues,
                    bins=hist_bins,
                    color=hist_color,
                    edgecolor='white',
                    linewidth=0.3,
                    alpha=0.85)
    ax_rt_hist.set_xlabel(RT_label)
    ax_rt_hist.set_ylabel('Count')
    ax_rt_hist.set_title('RT Distribution')

    # --- Bottom-right: 2D Histogram (heatmap) ---
    ax_heatmap = axes[1, 1]
    h = ax_heatmap.hist2d(RTValues, MZValues,
                          bins=hist_bins,
                          cmap='viridis',
                          cmin=1)
    ax_heatmap.set_xlabel(RT_label)
    ax_heatmap.set_ylabel(MZ_label)
    ax_heatmap.set_title('Precursor Density (m/z vs RT)')
    fig.colorbar(h[3], ax=ax_heatmap, label='Count')

    plt.tight_layout()

    # Step 5: Save if requested
    if SaveFig and OutputFolder is not None and OutputFigName is not None:
        import os
        if not os.path.exists(OutputFolder):
            os.makedirs(OutputFolder)
        FigPath = OutputFolder + '/' + OutputFigName
        fig.savefig(FigPath, dpi=200, bbox_inches='tight')
        print(f"Figure saved to: {FigPath}")

    plt.show()

    return PrecursorData
