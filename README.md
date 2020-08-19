# tcrregex

![](15-Table1-1.png){:width="25%"}

## Install 

```
pip install git+https://github.com/kmayerb/tcrregex.git
```
``
## Download Data Files

After install, download key background files. THIS IS NOT OPTIONAL.

```
python -c "import tcrregex as td; td.install_test_files.install_test_files()"
python -c "import tcrregex as td; td.setup_db.install_all_next_gen()"
python -c "import tcrregex as td; td.setup_blast.install_blast_to_externals(download_from = 'dropbox_osx')"
```

## Usage

Suppose you've done some flashywork with [tcrdist3](https://tcrdist3.readthedocs.io/en/latest/#), our research group's open-source Python package that enables a broad array of flexible T cell receptor sequence analyses; however, you are old-school and you want regex motif patterns and the classic motif plots as they were developed in the original [TCRdist 2017 scripts suite](https://github.com/phbradley/tcr-dist) associated with the Dash et al. Nature (2017) [doi:10.1038/nature22383](https://www.semanticscholar.org/paper/Quantifiable-predictive-features-define-T-cell-Dash-Fiore-Gartland/b3e8d6f21fbdcd58888af31e791b5a8d24a1c592/figure/2).


First, with tcrdist3: 

```python
import pandas as pd
from tcrdist.repertoire import TCRrep

df = pd.read_csv("dash.csv")
tr = TCRrep(cell_df = df, 
            organism = 'mouse', 
            chains = ['alpha','beta'], 
            db_file = 'alphabeta_gammadelta_db.tsv')
```

Now,  boot up the tcrregex package


```python
from tcrregex.subset import TCRsubset
from tcrregex.cdr3_motif import TCRMotif
from tcrregex.storage import StoreIOMotif, StoreIOEntropy
from tcrregex import plotting

# define a logical criteria
ind = (tr.clone_df.epitope == "PA")

# subset the TCRrep clone DataFrame to only those sequences meeting that criteria
clone_df_subset = tr.clone_df[ind].reset_index(drop = True).copy()

# subset the alpha chain and beta chain distance matrices using the `clone_df_subset.clone_id` index
dist_a_subset = pd.DataFrame(tr.pw_alpha[ind,:][:,ind])
dist_b_subset = pd.DataFrame(tr.pw_beta[ind,:][:,ind])
assert dist_a_subset.shape[0] == clone_df_subset.shape[0]
assert dist_a_subset.shape[1] == clone_df_subset.shape[0]
assert dist_b_subset.shape[0] == clone_df_subset.shape[0]
assert dist_b_subset.shape[1] == clone_df_subset.shape[0]

from tcrregex.subset import TCRsubset
from tcrregex.mappers import populate_legacy_fields
assert isinstance(dist_a_subset, pd.DataFrame)
assert isinstance(dist_b_subset, pd.DataFrame)
assert isinstance(clone_df_subset, pd.DataFrame)

# use the populate_legacy_fields function to add some columns needed for compatability with tcrdist1
clone_df_subset = populate_legacy_fields(df = clone_df_subset, chains =['alpha', 'beta'])

# FOR DEMO ONLY: Limit the sarch to first 100 seqs
clone_df_subset = clone_df_subset.iloc[0:50, :].copy()
dist_b_subset = dist_b_subset.iloc[0:50, 0:50].copy()
dist_a_subset = dist_a_subset.iloc[0:50, 0:50].copy()

# initialize an instance of the TCRsubset class.
ts = TCRsubset(clone_df_subset,
            organism = "mouse",
            epitopes = ["PA"] ,
            epitope = "PA",
            chains = ["A","B"],
            dist_a = dist_a_subset,
            dist_b = dist_b_subset)

# Chilax this step can take forever! 
ts.find_motif()

# So make sure to save your motifs DataFrame 
ts.motif_df.to_csv("saved_motifs.csv", index = False)

# You can always reload these and skip the wait
ts.motif_df = pd.read_csv("saved_motifs.csv")

# Output alpha-chain motifs
motif_list_a = list()
motif_logos_a = list()
for i,row in ts.motif_df[ts.motif_df.ab == "A"].iterrows():
    StoreIOMotif_instance = ts.eval_motif(row)
    motif_list_a.append(StoreIOMotif_instance)
    motif_logos_a.append(plotting.plot_pwm(StoreIOMotif_instance, create_file = False, my_height = 200, my_width = 600))

with open('alpha_motifs.html' , 'w') as outfile:
  for motif in motif_list_a:
    svg = plotting.plot_pwm(StoreIOMotif_instance, create_file = False, my_height = 200, my_width = 600)
    outfile.write(f"<div>{svg}</div>")

# Output beta-chain motifs
motif_list_b = list()
motif_logos_b = list()
for i,row in ts.motif_df[ts.motif_df.ab == "B"].iterrows():
    StoreIOMotif_instance = ts.eval_motif(row)
    motif_list_b.append(StoreIOMotif_instance)
    motif_logos_b.append(plotting.plot_pwm(StoreIOMotif_instance, create_file = False, my_height = 200, my_width = 600))

with open('beta_motifs.html' , 'w') as outfile:
  for motif in motif_list_b:
    svg = plotting.plot_pwm(StoreIOMotif_instance, create_file = False, my_height = 200, my_width = 600)
    outfile.write(f"<div>{svg}</div>")
```

Open your files:



['beta_motifs.html'](beta_motifs.html)

['alpha_motifs.html'](alpha_motifs.html)

<div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div><div><svg width="600" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1"  >
<text x="0.000000" y="75.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.333333,0.929915)">29*01</text>

<text x="0.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.333333,0.082051)">19*01</text>

<text x="0.000000" y="2850.000000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.333333,0.027350)">14*01</text>

<text x="0.000000" y="2925.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.238095,0.027350)">13-1*01</text>


<rect x="0" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="147.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.929915)">S</text>

<text x="147.000000" y="585.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.136752)">T</text>

<text x="207.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">L</text>

<text x="207.000000" y="159.375000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.218803)">S</text>

<text x="207.000000" y="393.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.109402)">P</text>

<text x="207.000000" y="600.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">I</text>

<text x="207.000000" y="675.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">F</text>

<text x="207.000000" y="1087.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">W</text>

<text x="207.000000" y="1162.500000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="207.000000" y="1237.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>

<text x="207.000000" y="1312.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">H</text>

<text x="207.000000" y="1387.500000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.054701)">G</text>

<text x="207.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">M</text>

<text x="207.000000" y="2925.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.027350)">E</text>

<text x="267.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.765812)">G</text>

<text x="267.000000" y="375.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.191453)">D</text>

<text x="267.000000" y="2700.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">T</text>

<text x="267.000000" y="2775.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">S</text>

<text x="267.000000" y="2850.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">N</text>

<text x="267.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">F</text>

<text x="327.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.246154)">G</text>

<text x="327.000000" y="159.375000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.218803)">R</text>

<text x="327.000000" y="287.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.164103)">Q</text>

<text x="327.000000" y="362.500000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.164103)">E</text>

<text x="327.000000" y="800.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">D</text>

<text x="327.000000" y="1275.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.054701)">T</text>

<text x="327.000000" y="1350.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">N</text>

<text x="327.000000" y="1425.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.054701)">A</text>

<text x="327.000000" y="2925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.027350)">V</text>

<text x="387.000000" y="75.000000" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.273504)">G</text>

<text x="387.000000" y="150.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.273504)">E</text>

<text x="387.000000" y="241.666667" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.246154)">A</text>

<text x="387.000000" y="510.000000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.136752)">R</text>

<text x="387.000000" y="925.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.082051)">T</text>

<text x="387.000000" y="2850.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.027350)">Y</text>

<text x="387.000000" y="2925.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.027350)">Q</text>

<text x="447.000000" y="75.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.328205)">Q</text>

<text x="447.000000" y="187.500000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">P</text>

<text x="447.000000" y="325.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.164103)">L</text>

<text x="447.000000" y="465.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.136752)">V</text>

<text x="447.000000" y="850.000000" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082051)">E</text>

<text x="447.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">A</text>

<text x="447.000000" y="1462.500000" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.054701)">R</text>

<text x="507.000000" y="75.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.437607)">L</text>

<text x="507.000000" y="195.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.273504)">Y</text>

<text x="507.000000" y="318.750000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.218803)">F</text>

<text x="507.000000" y="925.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.082051)">V</text>

<text x="507.000000" y="1462.500000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.054701)">Q</text>


<rect x="105" y="0" height="80" width="300" style="fill:none;stroke:black;stroke-width:1" />

<rect x="105.0" y="82" height="36.0" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="105.0" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="119.28571428571429" y="82" height="31.384615384615387" width="14.285714285714292" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="119.28571428571429" y="113.38461538461539" height="4.615384615384613" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:black;stroke:black;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:red;stroke:red;stroke-width:1" />

<rect x="119.28571428571429" y="118.0" height="0.0" width="14.285714285714292" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="133.57142857142858" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="133.57142857142858" y="105.07692307692307" height="12.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.07692307692307" height="0.9230769230769198" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="133.57142857142858" y="117.99999999999999" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="147.85714285714286" y="82" height="23.076923076923066" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="147.85714285714286" y="105.07692307692307" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="115.23076923076923" height="2.7692307692307736" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="147.85714285714286" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="162.14285714285714" y="82" height="15.692307692307693" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="162.14285714285714" y="97.6923076923077" height="11.07692307692308" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="108.76923076923077" height="9.230769230769226" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="162.14285714285714" y="118.0" height="0.0" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="176.42857142857144" y="82" height="7.384615384615387" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="176.42857142857144" y="89.38461538461539" height="10.15384615384616" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="99.53846153846155" height="18.461538461538453" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="176.42857142857144" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="190.71428571428572" y="82" height="2.7692307692307736" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="190.71428571428572" y="84.76923076923077" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="86.61538461538461" height="31.384615384615387" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="190.71428571428572" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="205.0" y="82" height="0.9230769230769198" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="82.92307692307692" height="35.07692307692308" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="205.0" y="118.0" height="0.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="219.28571428571428" y="82" height="0.9230769230769198" width="14.285714285714306" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="0.0" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="82.92307692307692" height="26.769230769230774" width="14.285714285714306" style="fill:black;stroke:black;stroke-width:1" />

<rect x="219.28571428571428" y="109.6923076923077" height="1.8461538461538396" width="14.285714285714306" style="fill:red;stroke:red;stroke-width:1" />

<rect x="219.28571428571428" y="111.53846153846153" height="6.461538461538467" width="14.285714285714306" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="233.57142857142858" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="233.57142857142858" y="82.0" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="82.92307692307692" height="18.461538461538467" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="233.57142857142858" y="101.38461538461539" height="2.7692307692307736" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="233.57142857142858" y="104.15384615384616" height="13.84615384615384" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="247.85714285714286" y="82" height="0.0" width="14.28571428571425" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="0.0" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="82.0" height="15.692307692307693" width="14.28571428571425" style="fill:black;stroke:black;stroke-width:1" />

<rect x="247.85714285714286" y="97.6923076923077" height="2.7692307692307736" width="14.28571428571425" style="fill:red;stroke:red;stroke-width:1" />

<rect x="247.85714285714286" y="100.46153846153847" height="17.538461538461533" width="14.28571428571425" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="262.1428571428571" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="82.0" height="12.92307692307692" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="262.1428571428571" y="94.92307692307692" height="23.07692307692308" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="276.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="82.0" height="9.230769230769226" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="276.42857142857144" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="290.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="82.0" height="8.307692307692307" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="290.7142857142857" y="90.3076923076923" height="0.9230769230769198" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="290.7142857142857" y="91.23076923076923" height="26.769230769230774" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="305.0" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="305.0" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="82.0" height="7.384615384615387" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="305.0" y="89.38461538461539" height="0.9230769230769198" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="305.0" y="90.3076923076923" height="27.692307692307693" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="319.28571428571433" y="82" height="0.0" width="14.28571428571422" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="0.0" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="82.0" height="4.615384615384613" width="14.28571428571422" style="fill:black;stroke:black;stroke-width:1" />

<rect x="319.28571428571433" y="86.61538461538461" height="3.6923076923076934" width="14.28571428571422" style="fill:red;stroke:red;stroke-width:1" />

<rect x="319.28571428571433" y="90.3076923076923" height="27.692307692307693" width="14.28571428571422" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="333.57142857142856" y="82" height="0.0" width="14.285714285714334" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="0.0" width="14.285714285714334" style="fill:black;stroke:black;stroke-width:1" />

<rect x="333.57142857142856" y="82.0" height="4.615384615384613" width="14.285714285714334" style="fill:red;stroke:red;stroke-width:1" />

<rect x="333.57142857142856" y="86.61538461538461" height="31.384615384615387" width="14.285714285714334" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="347.8571428571429" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="347.8571428571429" y="82.0" height="3.6923076923076934" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="347.8571428571429" y="85.6923076923077" height="32.30769230769231" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="362.14285714285717" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="362.14285714285717" y="82.0" height="1.8461538461538396" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="362.14285714285717" y="83.84615384615384" height="34.15384615384616" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="376.42857142857144" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="376.42857142857144" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<rect x="390.7142857142857" y="82" height="0.0" width="14.285714285714278" style="fill:silver;stroke:silver;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:black;stroke:black;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="0.0" width="14.285714285714278" style="fill:red;stroke:red;stroke-width:1" />

<rect x="390.7142857142857" y="82.0" height="36.0" width="14.285714285714278" style="fill:dimgray;stroke:dimgray;stroke-width:1" />

<text x="147.000000" y="1535.444992" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.129326)">S</text>

<text x="147.000000" y="10516.025947" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.019019)">T</text>

<text x="207.000000" y="4481.215972" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.042272)">L</text>

<text x="207.000000" y="5116.367969" font-size="100" font-family="monospace" fill="green" transform="scale(0.714286,0.037575)">S</text>

<text x="207.000000" y="10307.735938" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018788)">P</text>

<text x="207.000000" y="13818.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">I</text>

<text x="207.000000" y="13893.647917" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.014091)">F</text>

<text x="267.000000" y="575.260460" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.330729)">G</text>

<text x="267.000000" y="2376.041839" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.082682)">D</text>

<text x="327.000000" y="4008.354448" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.046966)">G</text>

<text x="327.000000" y="4584.398754" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.041748)">R</text>

<text x="327.000000" y="6187.531671" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.031311)">Q</text>

<text x="327.000000" y="6262.531671" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031311)">E</text>

<text x="327.000000" y="12600.063343" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.015655)">D</text>

<text x="387.000000" y="6138.073108" font-size="100" font-family="monospace" fill="orange" transform="scale(0.714286,0.031468)">G</text>

<text x="387.000000" y="6213.073108" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.031468)">E</text>

<text x="387.000000" y="6978.414565" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.028322)">A</text>

<text x="387.000000" y="12636.146216" font-size="100" font-family="monospace" fill="blue" transform="scale(0.714286,0.015734)">R</text>

<text x="447.000000" y="2554.853078" font-size="100" font-family="monospace" fill="purple" transform="scale(0.714286,0.073432)">Q</text>

<text x="447.000000" y="3907.279617" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.048955)">P</text>

<text x="447.000000" y="5284.706155" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.036716)">L</text>

<text x="447.000000" y="6416.647386" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.030597)">V</text>

<text x="447.000000" y="10769.412311" font-size="100" font-family="monospace" fill="red" transform="scale(0.714286,0.018358)">E</text>

<text x="447.000000" y="10844.412311" font-size="100" font-family="monospace" fill="black" transform="scale(0.714286,0.018358)">A</text>


<rect x="105" y="0" height="200.0" width="300" style="fill:none;stroke:black;stroke-width:1" />

<text x="1476.000000" y="75.000000" font-size="100" font-family="monospace" fill="green" transform="scale(0.277778,0.218803)">1-5*01</text>

<text x="1476.000000" y="160.714286" font-size="100" font-family="monospace" fill="red" transform="scale(0.277778,0.191453)">2-7*01</text>

<text x="1476.000000" y="235.714286" font-size="100" font-family="monospace" fill="blue" transform="scale(0.277778,0.191453)">1-1*01</text>

<text x="1476.000000" y="487.500000" font-size="100" font-family="monospace" fill="cyan" transform="scale(0.277778,0.109402)">2-2*01</text>

<text x="1476.000000" y="562.500000" font-size="100" font-family="monospace" fill="magenta" transform="scale(0.277778,0.109402)">1-4*01</text>

<text x="1476.000000" y="825.000000" font-size="100" font-family="monospace" fill="lime" transform="scale(0.277778,0.082051)">2-4*01</text>

<text x="1476.000000" y="900.000000" font-size="100" font-family="monospace" fill="black" transform="scale(0.277778,0.082051)">2-1*01</text>

<text x="1476.000000" y="1425.000000" font-size="100" font-family="monospace" fill="purple" transform="scale(0.277778,0.054701)">2-3*01</text>

<text x="1476.000000" y="2925.000000" font-size="100" font-family="monospace" fill="olive" transform="scale(0.277778,0.027350)">2-5*01</text>


<rect x="410" y="0" height="80" width="100" style="fill:none;stroke:black;stroke-width:1" />

<text x="410.000" y="128.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">PA B #clones=50</text>

<text x="410.000" y="136.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">chi-sq: 53.0</text>

<text x="410.000" y="144.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">motif: S.....L</text>

<text x="410.000" y="152.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match-: 20 40.0%</text>

<text x="410.000" y="160.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">match+: 39 78.0%</text>

<text x="410.000" y="168.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">expect: 4.520</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

<text x="410.000" y="176.000" font-size="8.0" font-weight="normal" font-family="Droid Sans Mono" fill="black" xml:space="preserve">enrich: 4.4</text>

</svg>
</div>