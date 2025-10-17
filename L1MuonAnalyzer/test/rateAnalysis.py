import uproot
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.colors as mcolors

prefix = "./"
input_files = [
    #prefix + "minBias_omtfNN_allMu.root"
    "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/crab/crab_omtf_Phase2Spring24_MinBias__t36/results/minBias_omtfNN_allMu.root"
]

tree_path = "events_omtfNN"

data = uproot.concatenate(
    [f"{file_path}:{tree_path}" for file_path in input_files],
    expressions=['muonPt', 'omtfPt', 'omtfUPt', 'omtfQuality', 'nnPt0', 'nnPt1', 'p_prompt', 'p_displ1', 'p_displ2'],
    library="pd"
)
# data = data.head(10000)

ptCuts = np.linspace(0, 100, 101)

# rate
rate = {'ptCut': ptCuts,
        'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
        'omtfPt': [data.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
        'omtfUPt': [data.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
        'nnPt0': [data.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}

rate = pd.DataFrame(rate)


# data with omtf quality >= 8
data_qual8 = data.query('omtfQuality >= 8')
rate_qual8 = {'ptCut': ptCuts,
              'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
              'omtfPt': [data_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
              'omtfUPt': [data_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
              'nnPt0': [data_qual8.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_qual8 = pd.DataFrame(rate_qual8)


# data with omtf quality >= 12
data_qual12 = data.query('omtfQuality >= 12')
rate_qual12 = {'ptCut': ptCuts,
               'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
               'omtfPt': [data_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
               'omtfUPt': [data_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
               'nnPt0': [data_qual12.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_qual12 = pd.DataFrame(rate_qual12)


# data with nnPt1 >= 5
data_nnPt1_5 = data.query('nnPt1 >= 5 and omtfQuality >= 8 and p_prompt > 0.5')
rate_nnPt1_5 = {'ptCut': ptCuts,
                'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfPt': [data_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfUPt': [data_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'nnPt0': [data_nnPt1_5.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_nnPt1_5 = pd.DataFrame(rate_nnPt1_5)


# data with nnPt1 >= 4
data_nnPt1_4 = data.query('nnPt1 >= 4 and omtfQuality >= 8')
rate_nnPt1_4 = {'ptCut': ptCuts,
                'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfPt': [data_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfUPt': [data_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'nnPt0': [data_nnPt1_4.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_nnPt1_4 = pd.DataFrame(rate_nnPt1_4)

# data with nnPt1 >= 6
data_nnPt1_6 = data.query('nnPt1 >= 6 and omtfQuality >= 8')
rate_nnPt1_6 = {'ptCut': ptCuts,
                'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfPt': [data_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfUPt': [data_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'nnPt0': [data_nnPt1_6.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_nnPt1_6 = pd.DataFrame(rate_nnPt1_6)

# date with quality >= 12 and nnPt1 >= 5
data_qual12_nnPt1_5 = data.query('nnPt1 >= 5 and omtfQuality >= 12')
rate_qual12_nnPt1_5 = {'ptCut': ptCuts,
                'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfPt': [data_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfUPt': [data_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'nnPt0': [data_qual12_nnPt1_5.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_qual12_nnPt1_5 = pd.DataFrame(rate_qual12_nnPt1_5)

# date with quality >= 12 and nnPt1 >= 4
data_qual12_nnPt1_4 = data.query('nnPt1 >= 4 and omtfQuality >= 12')
rate_qual12_nnPt1_4 = {'ptCut': ptCuts,
                'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfPt': [data_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfUPt': [data_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'nnPt0': [data_qual12_nnPt1_4.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_qual12_nnPt1_4 = pd.DataFrame(rate_qual12_nnPt1_4)

# date with quality >= 12 and nnPt1 >= 6
data_qual12_nnPt1_6 = data.query('nnPt1 >= 6 and omtfQuality >= 12')
rate_qual12_nnPt1_6 = {'ptCut': ptCuts,
                'muonPt': [data.query(f'muonPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfPt': [data_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'omtfUPt': [data_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts],
                'nnPt0': [data_qual12_nnPt1_6.query(f'nnPt0 >= {ptCut}').shape[0] / data.shape[0] for ptCut in ptCuts]}
rate_qual12_nnPt1_6 = pd.DataFrame(rate_qual12_nnPt1_6)


# efficiency

prefix = "./"
input_files = [
    #prefix + "OneOverPt_pt2_omtfN_t36.root"
    "/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_2_0_pre2/src/usercode/L1MuonAnalyzer/test/OMTF_phase2/rootDump/OneOverPt_pt2_omtfNN_t36.root"
]

tree_path = "events_omtfNN"

data_signal = uproot.concatenate(
    [f"{file_path}:{tree_path}" for file_path in input_files],
    expressions=['muonPt', 'omtfPt', 'omtfUPt', 'omtfQuality', 'nnPt0', 'nnPt1', 'muonEta', 'p_prompt', 'p_displ1', 'p_displ2'],
    library="pd"
)
# data_signal = data_signal.head(10000)


efficiency = {'ptCut': ptCuts,
              'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
              'omtfPt': [data_signal.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
              'omtfUPt': [data_signal.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
              'nnPt0': [data_signal.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency = pd.DataFrame(efficiency)

data_signal_qual8 = data_signal.query('omtfQuality >= 8')
efficiency_qual8 = {'ptCut': ptCuts,
                    'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                    'omtfPt': [data_signal_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                    'omtfUPt': [data_signal_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                    'nnPt0': [data_signal_qual8.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_qual8 = pd.DataFrame(efficiency_qual8)

data_signal_qual12 = data_signal.query('omtfQuality >= 12')
efficiency_qual12 = {'ptCut': ptCuts,
                        'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfPt': [data_signal_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfUPt': [data_signal_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'nnPt0': [data_signal_qual12.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_qual12 = pd.DataFrame(efficiency_qual12)

data_signal_nnPt1_5 = data_signal.query('nnPt1 >= 5 and omtfQuality >= 8 and p_prompt > 0.5')
efficiency_nnPt1_5 = {'ptCut': ptCuts,
                        'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfPt': [data_signal_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfUPt': [data_signal_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'nnPt0': [data_signal_nnPt1_5.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_nnPt1_5 = pd.DataFrame(efficiency_nnPt1_5)

data_signal_nnPt1_4 = data_signal.query('nnPt1 >= 4 and omtfQuality >= 8')
efficiency_nnPt1_4 = {'ptCut': ptCuts,
                        'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfPt': [data_signal_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfUPt': [data_signal_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'nnPt0': [data_signal_nnPt1_4.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_nnPt1_4 = pd.DataFrame(efficiency_nnPt1_4)

data_signal_nnPt1_6 = data_signal.query('nnPt1 >= 6 and omtfQuality >= 8')
efficiency_nnPt1_6 = {'ptCut': ptCuts,
                        'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfPt': [data_signal_qual8.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'omtfUPt': [data_signal_qual8.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                        'nnPt0': [data_signal_nnPt1_6.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_nnPt1_6 = pd.DataFrame(efficiency_nnPt1_6)

# data with quality >= 12 and nnPt1 >= 5
data_signal_qual12_nnPt1_5 = data_signal.query('nnPt1 >= 5 and omtfQuality >= 12')
efficiency_qual12_nnPt1_5 = {'ptCut': ptCuts,
                             'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'omtfPt': [data_signal_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'omtfUPt': [data_signal_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'nnPt0': [data_signal_qual12_nnPt1_5.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_qual12_nnPt1_5 = pd.DataFrame(efficiency_qual12_nnPt1_5)

# data with quality >= 12 and nnPt1 >= 4
data_signal_qual12_nnPt1_4 = data_signal.query('nnPt1 >= 4 and omtfQuality >= 12')
efficiency_qual12_nnPt1_4 = {'ptCut': ptCuts,
                             'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'omtfPt': [data_signal_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'omtfUPt': [data_signal_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'nnPt0': [data_signal_qual12_nnPt1_4.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_qual12_nnPt1_4 = pd.DataFrame(efficiency_qual12_nnPt1_4)

# data with quality >= 12 and nnPt1 >= 6
data_signal_qual12_nnPt1_6 = data_signal.query('nnPt1 >= 6 and omtfQuality >= 12')
efficiency_qual12_nnPt1_6 = {'ptCut': ptCuts,
                             'muonPt': [data_signal.query(f'muonPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'omtfPt': [data_signal_qual12.query(f'omtfPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'omtfUPt': [data_signal_qual12.query(f'omtfUPt >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts],
                             'nnPt0': [data_signal_qual12_nnPt1_6.query(f'nnPt0 >= {ptCut}').shape[0] / data_signal.shape[0] for ptCut in ptCuts]}
efficiency_qual12_nnPt1_6 = pd.DataFrame(efficiency_qual12_nnPt1_6)


# rate and efficiency for ptCut = 20 and changing cut on nnPt1

nnPt1Cuts = np.linspace(0, 10, 101)

dataPt20 = data.query('omtfQuality >= 8 and nnPt0 >= 20')[['nnPt0', 'nnPt1']]

rate_nnPt0_20 = {'nnPt1Cut': nnPt1Cuts,
                'nnPt0': [dataPt20.query(f'nnPt1 >= {nnPt1Cut}').shape[0] / data.shape[0] for nnPt1Cut in nnPt1Cuts]}
rate_nnPt0_20 = pd.DataFrame(rate_nnPt0_20)

data_signalPt20 = data_signal.query('omtfQuality >= 8 and nnPt0 >= 20')[['nnPt0', 'nnPt1']]
efficiency_nnPt0_20 = {'nnPt1Cut': nnPt1Cuts,
                'nnPt0': [data_signalPt20.query(f'nnPt1 >= {nnPt1Cut}').shape[0] / data_signal.shape[0] for nnPt1Cut in nnPt1Cuts]}
efficiency_nnPt0_20 = pd.DataFrame(efficiency_nnPt0_20)

######
# Plot
######

#Increase plots font size
params = {'font.size': 12,
        'legend.fontsize': 'xx-large',
          'figure.figsize': (10, 7),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'axes.grid': True,
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large',
         'lines.linewidth': 3,
         'lines.markersize': 10,}
plt.rcParams.update(params)

# rate

fig, ax = plt.subplots(3, 3, figsize=(30, 30))
ax[0,0].plot(rate['ptCut'], rate['muonPt'], label='muonPt')
ax[0,0].plot(rate['ptCut'], rate['omtfPt'], label='omtfPt')
ax[0,0].plot(rate['ptCut'], rate['omtfUPt'], label='omtfUPt')
ax[0,0].plot(rate['ptCut'], rate['nnPt0'], label='nnPt0')
ax[0,0].legend()
ax[0,0].set_yscale('log')
ax[0,0].set_xlabel('ptCut [GeV]')
ax[0,0].set_ylabel('rate')
ax[0,0].set_title('no quality cut')

ax[0,1].plot(rate_qual8['ptCut'], rate_qual8['muonPt'], label='muonPt')
ax[0,1].plot(rate_qual8['ptCut'], rate_qual8['omtfPt'], label='omtfPt, quality>=8')
ax[0,1].plot(rate_qual8['ptCut'], rate_qual8['omtfUPt'], label='omtfUPt, quality>=8')
ax[0,1].plot(rate_qual8['ptCut'], rate_qual8['nnPt0'], label='nnPt0, quality>=8')
ax[0,1].legend()
ax[0,1].set_yscale('log')
ax[0,1].set_xlabel('ptCut [GeV]')
ax[0,1].set_ylabel('rate')
ax[0,1].set_title('omtfQuality >= 8')

ax[0,2].plot(rate_qual12['ptCut'], rate_qual12['muonPt'], label='muonPt')
ax[0,2].plot(rate_qual12['ptCut'], rate_qual12['omtfPt'], label='omtfPt, quality>=12')
ax[0,2].plot(rate_qual12['ptCut'], rate_qual12['omtfUPt'], label='omtfUPt, quality>=12')
ax[0,2].plot(rate_qual12['ptCut'], rate_qual12['nnPt0'], label='nnPt0, quality>=12')
ax[0,2].legend()
ax[0,2].set_yscale('log')
ax[0,2].set_xlabel('ptCut [GeV]')
ax[0,2].set_ylabel('rate')
ax[0,2].set_title('omtfQuality >= 12')

ax[1,0].plot(rate_nnPt1_4['ptCut'], rate_nnPt1_4['muonPt'], label='muonPt')
ax[1,0].plot(rate_nnPt1_4['ptCut'], rate_nnPt1_4['omtfPt'], label='omtfPt, quality>=8')
ax[1,0].plot(rate_nnPt1_4['ptCut'], rate_nnPt1_4['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,0].plot(rate_nnPt1_4['ptCut'], rate_nnPt1_4['nnPt0'], label='nnPt0, quality>=8, nnPt1>=4')
ax[1,0].legend()
ax[1,0].set_yscale('log')
ax[1,0].set_xlabel('ptCut [GeV]')
ax[1,0].set_ylabel('rate')
ax[1,0].set_title('nnPt1 >= 4')

ax[1,1].plot(rate_nnPt1_5['ptCut'], rate_nnPt1_5['muonPt'], label='muonPt')
ax[1,1].plot(rate_nnPt1_5['ptCut'], rate_nnPt1_5['omtfPt'], label='omtfPt, quality>=8')
ax[1,1].plot(rate_nnPt1_5['ptCut'], rate_nnPt1_5['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,1].plot(rate_nnPt1_5['ptCut'], rate_nnPt1_5['nnPt0'], label='nnPt0, quality>=8, nnPt1>=5')
ax[1,1].legend()
ax[1,1].set_yscale('log')
ax[1,1].set_xlabel('ptCut [GeV]')
ax[1,1].set_ylabel('rate')
ax[1,1].set_title('nnPt1 >= 5')

ax[1,2].plot(rate_nnPt1_6['ptCut'], rate_nnPt1_6['muonPt'], label='muonPt')
ax[1,2].plot(rate_nnPt1_6['ptCut'], rate_nnPt1_6['omtfPt'], label='omtfPt, quality>=8')
ax[1,2].plot(rate_nnPt1_6['ptCut'], rate_nnPt1_6['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,2].plot(rate_nnPt1_6['ptCut'], rate_nnPt1_6['nnPt0'], label='nnPt0, quality>=8, nnPt1>=6')
ax[1,2].legend()
ax[1,2].set_yscale('log')
ax[1,2].set_xlabel('ptCut [GeV]')
ax[1,2].set_ylabel('rate')
ax[1,2].set_title('nnPt1 >= 6')

fig.tight_layout()
fig.savefig('rate.png')
ax[2,0].plot(rate_qual12_nnPt1_4['ptCut'], rate_qual12_nnPt1_4['muonPt'], label='muonPt')
ax[2,0].plot(rate_qual12_nnPt1_4['ptCut'], rate_qual12_nnPt1_4['omtfPt'], label='omtfPt, quality>=12')
ax[2,0].plot(rate_qual12_nnPt1_4['ptCut'], rate_qual12_nnPt1_4['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,0].plot(rate_qual12_nnPt1_4['ptCut'], rate_qual12_nnPt1_4['nnPt0'], label='nnPt0, quality>=12, nnPt1>=4')
ax[2,0].legend()
ax[2,0].set_yscale('log')
ax[2,0].set_xlabel('ptCut [GeV]')
ax[2,0].set_ylabel('rate')
ax[2,0].set_title('nnPt1 >= 4, quality >= 12')

ax[2,1].plot(rate_qual12_nnPt1_5['ptCut'], rate_qual12_nnPt1_5['muonPt'], label='muonPt')
ax[2,1].plot(rate_qual12_nnPt1_5['ptCut'], rate_qual12_nnPt1_5['omtfPt'], label='omtfPt, quality>=12')
ax[2,1].plot(rate_qual12_nnPt1_5['ptCut'], rate_qual12_nnPt1_5['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,1].plot(rate_qual12_nnPt1_5['ptCut'], rate_qual12_nnPt1_5['nnPt0'], label='nnPt0, quality>=12, nnPt1>=5')
ax[2,1].legend()
ax[2,1].set_yscale('log')
ax[2,1].set_xlabel('ptCut [GeV]')
ax[2,1].set_ylabel('rate')
ax[2,1].set_title('nnPt1 >= 5, quality >= 12')

ax[2,2].plot(rate_qual12_nnPt1_6['ptCut'], rate_qual12_nnPt1_6['muonPt'], label='muonPt')
ax[2,2].plot(rate_qual12_nnPt1_6['ptCut'], rate_qual12_nnPt1_6['omtfPt'], label='omtfPt, quality>=12')
ax[2,2].plot(rate_qual12_nnPt1_6['ptCut'], rate_qual12_nnPt1_6['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,2].plot(rate_qual12_nnPt1_6['ptCut'], rate_qual12_nnPt1_6['nnPt0'], label='nnPt0, quality>=12, nnPt1>=6')
ax[2,2].legend()
ax[2,2].set_yscale('log')
ax[2,2].set_xlabel('ptCut [GeV]')
ax[2,2].set_ylabel('rate')
ax[2,2].set_title('nnPt1 >= 6, quality >= 12')

fig.tight_layout()
fig.savefig('rate.png')


# efficiency
fig, ax = plt.subplots(3, 3, figsize=(30, 30))
ax[0,0].plot(efficiency['ptCut'], efficiency['muonPt'], label='muonPt')
ax[0,0].plot(efficiency['ptCut'], efficiency['omtfPt'], label='omtfPt')
ax[0,0].plot(efficiency['ptCut'], efficiency['omtfUPt'], label='omtfUPt')
ax[0,0].plot(efficiency['ptCut'], efficiency['nnPt0'], label='nnPt0')
ax[0,0].legend()
ax[0,0].set_yscale('log')
ax[0,0].set_xlabel('ptCut [GeV]')
ax[0,0].set_ylabel('efficiency')
ax[0,0].set_title('no quality cut')

ax[0,1].plot(efficiency_qual8['ptCut'], efficiency_qual8['muonPt'], label='muonPt')
ax[0,1].plot(efficiency_qual8['ptCut'], efficiency_qual8['omtfPt'], label='omtfPt, quality>=8')
ax[0,1].plot(efficiency_qual8['ptCut'], efficiency_qual8['omtfUPt'], label='omtfUPt, quality>=8')
ax[0,1].plot(efficiency_qual8['ptCut'], efficiency_qual8['nnPt0'], label='nnPt0, quality>=8')
ax[0,1].legend()
ax[0,1].set_yscale('log')
ax[0,1].set_xlabel('ptCut [GeV]')
ax[0,1].set_ylabel('efficiency')
ax[0,1].set_title('omtfQuality >= 8')

ax[0,2].plot(efficiency_qual12['ptCut'], efficiency_qual12['muonPt'], label='muonPt')
ax[0,2].plot(efficiency_qual12['ptCut'], efficiency_qual12['omtfPt'], label='omtfPt, quality>=12')
ax[0,2].plot(efficiency_qual12['ptCut'], efficiency_qual12['omtfUPt'], label='omtfUPt, quality>=12')
ax[0,2].plot(efficiency_qual12['ptCut'], efficiency_qual12['nnPt0'], label='nnPt0, quality>=12')
ax[0,2].legend()
ax[0,2].set_yscale('log')
ax[0,2].set_xlabel('ptCut [GeV]')
ax[0,2].set_ylabel('efficiency')
ax[0,2].set_title('omtfQuality >= 12')

ax[1,0].plot(efficiency_nnPt1_4['ptCut'], efficiency_nnPt1_4['muonPt'], label='muonPt')
ax[1,0].plot(efficiency_nnPt1_4['ptCut'], efficiency_nnPt1_4['omtfPt'], label='omtfPt, quality>=8')
ax[1,0].plot(efficiency_nnPt1_4['ptCut'], efficiency_nnPt1_4['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,0].plot(efficiency_nnPt1_4['ptCut'], efficiency_nnPt1_4['nnPt0'], label='nnPt0, quality>=8, nnPt1>=4')
ax[1,0].legend()
ax[1,0].set_yscale('log')
ax[1,0].set_xlabel('ptCut [GeV]')
ax[1,0].set_ylabel('efficiency')
ax[1,0].set_title('nnPt1 >= 4')

ax[1,1].plot(efficiency_nnPt1_5['ptCut'], efficiency_nnPt1_5['muonPt'], label='muonPt')
ax[1,1].plot(efficiency_nnPt1_5['ptCut'], efficiency_nnPt1_5['omtfPt'], label='omtfPt, quality>=8')
ax[1,1].plot(efficiency_nnPt1_5['ptCut'], efficiency_nnPt1_5['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,1].plot(efficiency_nnPt1_5['ptCut'], efficiency_nnPt1_5['nnPt0'], label='nnPt0, quality>=8, nnPt1>=5')
ax[1,1].legend()
ax[1,1].set_yscale('log')
ax[1,1].set_xlabel('ptCut [GeV]')
ax[1,1].set_ylabel('efficiency')
ax[1,1].set_title('nnPt1 >= 5')

ax[1,2].plot(efficiency_nnPt1_6['ptCut'], efficiency_nnPt1_6['muonPt'], label='muonPt')
ax[1,2].plot(efficiency_nnPt1_6['ptCut'], efficiency_nnPt1_6['omtfPt'], label='omtfPt, quality>=8')
ax[1,2].plot(efficiency_nnPt1_6['ptCut'], efficiency_nnPt1_6['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,2].plot(efficiency_nnPt1_6['ptCut'], efficiency_nnPt1_6['nnPt0'], label='nnPt0, quality>=8, nnPt1>=6')
ax[1,2].legend()
ax[1,2].set_yscale('log')
ax[1,2].set_xlabel('ptCut [GeV]')
ax[1,2].set_ylabel('efficiency')
ax[1,2].set_title('nnPt1 >= 6')

ax[2,0].plot(efficiency_qual12_nnPt1_4['ptCut'], efficiency_qual12_nnPt1_4['muonPt'], label='muonPt')
ax[2,0].plot(efficiency_qual12_nnPt1_4['ptCut'], efficiency_qual12_nnPt1_4['omtfPt'], label='omtfPt, quality>=12')
ax[2,0].plot(efficiency_qual12_nnPt1_4['ptCut'], efficiency_qual12_nnPt1_4['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,0].plot(efficiency_qual12_nnPt1_4['ptCut'], efficiency_qual12_nnPt1_4['nnPt0'], label='nnPt0, quality>=12, nnPt1>=4')
ax[2,0].legend()
ax[2,0].set_yscale('log')
ax[2,0].set_xlabel('ptCut [GeV]')
ax[2,0].set_ylabel('efficiency')
ax[2,0].set_title('nnPt1 >= 4, quality >= 12')

ax[2,1].plot(efficiency_qual12_nnPt1_5['ptCut'], efficiency_qual12_nnPt1_5['muonPt'], label='muonPt')
ax[2,1].plot(efficiency_qual12_nnPt1_5['ptCut'], efficiency_qual12_nnPt1_5['omtfPt'], label='omtfPt, quality>=12')
ax[2,1].plot(efficiency_qual12_nnPt1_5['ptCut'], efficiency_qual12_nnPt1_5['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,1].plot(efficiency_qual12_nnPt1_5['ptCut'], efficiency_qual12_nnPt1_5['nnPt0'], label='nnPt0, quality>=12, nnPt1>=5')
ax[2,1].legend()
ax[2,1].set_yscale('log')
ax[2,1].set_xlabel('ptCut [GeV]')
ax[2,1].set_ylabel('efficiency')
ax[2,1].set_title('nnPt1 >= 5, quality >= 12')

ax[2,2].plot(efficiency_qual12_nnPt1_6['ptCut'], efficiency_qual12_nnPt1_6['muonPt'], label='muonPt')
ax[2,2].plot(efficiency_qual12_nnPt1_6['ptCut'], efficiency_qual12_nnPt1_6['omtfPt'], label='omtfPt, quality>=12')
ax[2,2].plot(efficiency_qual12_nnPt1_6['ptCut'], efficiency_qual12_nnPt1_6['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,2].plot(efficiency_qual12_nnPt1_6['ptCut'], efficiency_qual12_nnPt1_6['nnPt0'], label='nnPt0, quality>=12, nnPt1>=6')
ax[2,2].legend()
ax[2,2].set_yscale('log')
ax[2,2].set_xlabel('ptCut [GeV]')
ax[2,2].set_ylabel('efficiency')
ax[2,2].set_title('nnPt1 >= 6, quality >= 12')


fig.tight_layout()
fig.savefig('efficiency.png')



# rate vs efficiency
fig, ax = plt.subplots(3, 3, figsize=(30, 30))


ax[0,0].plot(rate['muonPt'], efficiency['muonPt'], label='muonPt')
ax[0,0].plot(rate['omtfPt'], efficiency['omtfPt'], label='omtfPt')
ax[0,0].plot(rate['omtfUPt'], efficiency['omtfUPt'], label='omtfUPt')
ax[0,0].plot(rate['nnPt0'], efficiency['nnPt0'], label='nnPt0')
ax[0,0].set_prop_cycle(None)
ax[0,0].plot(rate.query('ptCut == 20')['muonPt'], efficiency.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[0,0].plot(rate.query('ptCut == 20')['omtfPt'], efficiency.query('ptCut == 20')['omtfPt'], 'o')
ax[0,0].plot(rate.query('ptCut == 20')['omtfUPt'], efficiency.query('ptCut == 20')['omtfUPt'], 'o')
ax[0,0].plot(rate.query('ptCut == 20')['nnPt0'], efficiency.query('ptCut == 20')['nnPt0'], 'o')
ax[0,0].legend()
ax[0,0].set_xlabel('rate')
ax[0,0].set_ylabel('efficiency')
ax[0,0].set_title('no quality cut')


ax[0,1].plot(rate_qual8['muonPt'], efficiency_qual8['muonPt'], label='muonPt')
ax[0,1].plot(rate_qual8['omtfPt'], efficiency_qual8['omtfPt'], label='omtfPt, quality>=8')
ax[0,1].plot(rate_qual8['omtfUPt'], efficiency_qual8['omtfUPt'], label='omtfUPt, quality>=8')
ax[0,1].plot(rate_qual8['nnPt0'], efficiency_qual8['nnPt0'], label='nnPt0, quality>=8')
ax[0,1].set_prop_cycle(None)
ax[0,1].plot(rate_qual8.query('ptCut == 20')['muonPt'], efficiency_qual8.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[0,1].plot(rate_qual8.query('ptCut == 20')['omtfPt'], efficiency_qual8.query('ptCut == 20')['omtfPt'], 'o')
ax[0,1].plot(rate_qual8.query('ptCut == 20')['omtfUPt'], efficiency_qual8.query('ptCut == 20')['omtfUPt'], 'o')
ax[0,1].plot(rate_qual8.query('ptCut == 20')['nnPt0'], efficiency_qual8.query('ptCut == 20')['nnPt0'], 'o')
ax[0,1].legend()
ax[0,1].set_xlabel('rate')
ax[0,1].set_ylabel('efficiency')
ax[0,1].set_title('omtfQuality >= 8')


ax[0,2].plot(rate_qual12['muonPt'], efficiency_qual12['muonPt'], label='muonPt')
ax[0,2].plot(rate_qual12['omtfPt'], efficiency_qual12['omtfPt'], label='omtfPt, quality>=12')
ax[0,2].plot(rate_qual12['omtfUPt'], efficiency_qual12['omtfUPt'], label='omtfUPt, quality>=12')
ax[0,2].plot(rate_qual12['nnPt0'], efficiency_qual12['nnPt0'], label='nnPt0, quality>=12')
ax[0,2].set_prop_cycle(None)
ax[0,2].plot(rate_qual12.query('ptCut == 20')['muonPt'], efficiency_qual12.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[0,2].plot(rate_qual12.query('ptCut == 20')['omtfPt'], efficiency_qual12.query('ptCut == 20')['omtfPt'], 'o')
ax[0,2].plot(rate_qual12.query('ptCut == 20')['omtfUPt'], efficiency_qual12.query('ptCut == 20')['omtfUPt'], 'o')
ax[0,2].plot(rate_qual12.query('ptCut == 20')['nnPt0'], efficiency_qual12.query('ptCut == 20')['nnPt0'], 'o')
ax[0,2].legend()
ax[0,2].set_xlabel('rate')
ax[0,2].set_ylabel('efficiency')
ax[0,2].set_title('omtfQuality >= 12')


ax[1,0].plot(rate_nnPt1_4['muonPt'], efficiency_nnPt1_4['muonPt'], label='muonPt')
ax[1,0].plot(rate_nnPt1_4['omtfPt'], efficiency_nnPt1_4['omtfPt'], label='omtfPt, quality>=8')
ax[1,0].plot(rate_nnPt1_4['omtfUPt'], efficiency_nnPt1_4['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,0].plot(rate_nnPt1_4['nnPt0'], efficiency_nnPt1_4['nnPt0'], label='nnPt0, quality>=8, nnPt1>=4')
ax[1,0].set_prop_cycle(None)
ax[1,0].plot(rate_nnPt1_4.query('ptCut == 20')['muonPt'], efficiency_nnPt1_4.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[1,0].plot(rate_nnPt1_4.query('ptCut == 20')['omtfPt'], efficiency_nnPt1_4.query('ptCut == 20')['omtfPt'], 'o')
ax[1,0].plot(rate_nnPt1_4.query('ptCut == 20')['omtfUPt'], efficiency_nnPt1_4.query('ptCut == 20')['omtfUPt'], 'o')
ax[1,0].plot(rate_nnPt1_4.query('ptCut == 20')['nnPt0'], efficiency_nnPt1_4.query('ptCut == 20')['nnPt0'], 'o')
ax[1,0].legend()
ax[1,0].set_xlabel('rate')
ax[1,0].set_ylabel('efficiency')
ax[1,0].set_title('nnPt1 >= 4')


ax[1,1].plot(rate_nnPt1_5['muonPt'], efficiency_nnPt1_5['muonPt'], label='muonPt')
ax[1,1].plot(rate_nnPt1_5['omtfPt'], efficiency_nnPt1_5['omtfPt'], label='omtfPt, quality>=8')
ax[1,1].plot(rate_nnPt1_5['omtfUPt'], efficiency_nnPt1_5['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,1].plot(rate_nnPt1_5['nnPt0'], efficiency_nnPt1_5['nnPt0'], label='nnPt0, quality>=8, nnPt1>=5')
ax[1,1].set_prop_cycle(None)
ax[1,1].plot(rate_nnPt1_5.query('ptCut == 20')['muonPt'], efficiency_nnPt1_5.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[1,1].plot(rate_nnPt1_5.query('ptCut == 20')['omtfPt'], efficiency_nnPt1_5.query('ptCut == 20')['omtfPt'], 'o')
ax[1,1].plot(rate_nnPt1_5.query('ptCut == 20')['omtfUPt'], efficiency_nnPt1_5.query('ptCut == 20')['omtfUPt'], 'o')
ax[1,1].plot(rate_nnPt1_5.query('ptCut == 20')['nnPt0'], efficiency_nnPt1_5.query('ptCut == 20')['nnPt0'], 'o')
ax[1,1].legend()
ax[1,1].set_xlabel('rate')
ax[1,1].set_ylabel('efficiency')
ax[1,1].set_title('nnPt1 >= 5')


ax[1,2].plot(rate_nnPt1_6['muonPt'], efficiency_nnPt1_6['muonPt'], label='muonPt')
ax[1,2].plot(rate_nnPt1_6['omtfPt'], efficiency_nnPt1_6['omtfPt'], label='omtfPt, quality>=8')
ax[1,2].plot(rate_nnPt1_6['omtfUPt'], efficiency_nnPt1_6['omtfUPt'], label='omtfUPt, quality>=8')
ax[1,2].plot(rate_nnPt1_6['nnPt0'], efficiency_nnPt1_6['nnPt0'], label='nnPt0, quality>=8, nnPt1>=6')
ax[1,2].set_prop_cycle(None)
ax[1,2].plot(rate_nnPt1_6.query('ptCut == 20')['muonPt'], efficiency_nnPt1_6.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[1,2].plot(rate_nnPt1_6.query('ptCut == 20')['omtfPt'], efficiency_nnPt1_6.query('ptCut == 20')['omtfPt'], 'o')
ax[1,2].plot(rate_nnPt1_6.query('ptCut == 20')['omtfUPt'], efficiency_nnPt1_6.query('ptCut == 20')['omtfUPt'], 'o')
ax[1,2].plot(rate_nnPt1_6.query('ptCut == 20')['nnPt0'], efficiency_nnPt1_6.query('ptCut == 20')['nnPt0'], 'o')
ax[1,2].legend()
ax[1,2].set_xlabel('rate')
ax[1,2].set_ylabel('efficiency')
ax[1,2].set_title('nnPt1 >= 6')

ax[2,0].plot(rate_qual12_nnPt1_4['muonPt'], efficiency_qual12_nnPt1_4['muonPt'], label='muonPt')
ax[2,0].plot(rate_qual12_nnPt1_4['omtfPt'], efficiency_qual12_nnPt1_4['omtfPt'], label='omtfPt, quality>=12')
ax[2,0].plot(rate_qual12_nnPt1_4['omtfUPt'], efficiency_qual12_nnPt1_4['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,0].plot(rate_qual12_nnPt1_4['nnPt0'], efficiency_qual12_nnPt1_4['nnPt0'], label='nnPt0, quality>=12, nnPt1>=4')
ax[2,0].set_prop_cycle(None)
ax[2,0].plot(rate_qual12_nnPt1_4.query('ptCut == 20')['muonPt'], efficiency_qual12_nnPt1_4.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[2,0].plot(rate_qual12_nnPt1_4.query('ptCut == 20')['omtfPt'], efficiency_qual12_nnPt1_4.query('ptCut == 20')['omtfPt'], 'o')
ax[2,0].plot(rate_qual12_nnPt1_4.query('ptCut == 20')['omtfUPt'], efficiency_qual12_nnPt1_4.query('ptCut == 20')['omtfUPt'], 'o')
ax[2,0].plot(rate_qual12_nnPt1_4.query('ptCut == 20')['nnPt0'], efficiency_qual12_nnPt1_4.query('ptCut == 20')['nnPt0'], 'o')
ax[2,0].legend()
ax[2,0].set_xlabel('rate')
ax[2,0].set_ylabel('efficiency')
ax[2,0].set_title('nnPt1 >= 4, quality >= 12')

ax[2,1].plot(rate_qual12_nnPt1_5['muonPt'], efficiency_qual12_nnPt1_5['muonPt'], label='muonPt')
ax[2,1].plot(rate_qual12_nnPt1_5['omtfPt'], efficiency_qual12_nnPt1_5['omtfPt'], label='omtfPt, quality>=12')
ax[2,1].plot(rate_qual12_nnPt1_5['omtfUPt'], efficiency_qual12_nnPt1_5['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,1].plot(rate_qual12_nnPt1_5['nnPt0'], efficiency_qual12_nnPt1_5['nnPt0'], label='nnPt0, quality>=12, nnPt1>=5')
ax[2,1].set_prop_cycle(None)
ax[2,1].plot(rate_qual12_nnPt1_5.query('ptCut == 20')['muonPt'], efficiency_qual12_nnPt1_5.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[2,1].plot(rate_qual12_nnPt1_5.query('ptCut == 20')['omtfPt'], efficiency_qual12_nnPt1_5.query('ptCut == 20')['omtfPt'], 'o')
ax[2,1].plot(rate_qual12_nnPt1_5.query('ptCut == 20')['omtfUPt'], efficiency_qual12_nnPt1_5.query('ptCut == 20')['omtfUPt'], 'o')
ax[2,1].plot(rate_qual12_nnPt1_5.query('ptCut == 20')['nnPt0'], efficiency_qual12_nnPt1_5.query('ptCut == 20')['nnPt0'], 'o')
ax[2,1].legend()
ax[2,1].set_xlabel('rate')
ax[2,1].set_ylabel('efficiency')
ax[2,1].set_title('nnPt1 >= 5, quality >= 12')

ax[2,2].plot(rate_qual12_nnPt1_6['muonPt'], efficiency_qual12_nnPt1_6['muonPt'], label='muonPt')
ax[2,2].plot(rate_qual12_nnPt1_6['omtfPt'], efficiency_qual12_nnPt1_6['omtfPt'], label='omtfPt, quality>=12')
ax[2,2].plot(rate_qual12_nnPt1_6['omtfUPt'], efficiency_qual12_nnPt1_6['omtfUPt'], label='omtfUPt, quality>=12')
ax[2,2].plot(rate_qual12_nnPt1_6['nnPt0'], efficiency_qual12_nnPt1_6['nnPt0'], label='nnPt0, quality>=12, nnPt1>=6')
ax[2,2].set_prop_cycle(None)
ax[2,2].plot(rate_qual12_nnPt1_6.query('ptCut == 20')['muonPt'], efficiency_qual12_nnPt1_6.query('ptCut == 20')['muonPt'], 'o', label='ptCut = 20')
ax[2,2].plot(rate_qual12_nnPt1_6.query('ptCut == 20')['omtfPt'], efficiency_qual12_nnPt1_6.query('ptCut == 20')['omtfPt'], 'o')
ax[2,2].plot(rate_qual12_nnPt1_6.query('ptCut == 20')['omtfUPt'], efficiency_qual12_nnPt1_6.query('ptCut == 20')['omtfUPt'], 'o')
ax[2,2].plot(rate_qual12_nnPt1_6.query('ptCut == 20')['nnPt0'], efficiency_qual12_nnPt1_6.query('ptCut == 20')['nnPt0'], 'o')
ax[2,2].legend()
ax[2,2].set_xlabel('rate')
ax[2,2].set_ylabel('efficiency')
ax[2,2].set_title('nnPt1 >= 6, quality >= 12')


fig.tight_layout()
fig.savefig('rate_vs_efficiency.png')

# rate and efficiency for ptCut = 20 and changing cut on nnPt1

fig, ax = plt.subplots(1, 3, figsize=(30, 10))

ax[0].plot(rate_nnPt0_20['nnPt1Cut'], rate_nnPt0_20['nnPt0'], label='rate')
ax[0].legend()
ax[0].set_xlabel('nnPt1Cut')
ax[0].set_ylabel('rate')
ax[0].set_title('rate, nnPt0 >= 20, quality>=8')

ax[1].plot(efficiency_nnPt0_20['nnPt1Cut'], efficiency_nnPt0_20['nnPt0'], label='efficiency')
ax[1].legend()
ax[1].set_xlabel('nnPt1Cut')
ax[1].set_ylabel('efficiency')
ax[1].set_title('efficiency, nnPt0 >= 20, quality>=8')

ax[2].plot(rate_nnPt0_20['nnPt0'], efficiency_nnPt0_20['nnPt0'], label='rate vs efficiency')
ax[2].legend()
ax[2].set_xlabel('rate')
ax[2].set_ylabel('efficiency')
ax[2].set_title('rate vs efficiency, nnPt0 >= 20, quality>=8')

fig.tight_layout()
fig.savefig('rate_vs_efficiency_nnPt0Cut20.png')