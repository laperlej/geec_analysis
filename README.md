# epiGeEC Analysis #
- - - -
The **epiGenomic Efficient Correlator Analysis** tools are a suite to analyse correlation matrix from **epiGenomic Efficient Correlator**.

### Installation
- - - -
Linux/x64 is the only OS currently supported

**Install epiGeEC Analysis**

    git clone git@bitbucket.org:labjacquespe/geec_analysis.git

**Dependencies**

You will need pip to install the python package, use the following command if not already installed

	sudo apt-get install python-pip  
	
Pip will attempt to install all dependencies but most likely will fail

See documentation on how to install [pandas](https://github.com/svaksha/PyData-Workshop-Sprint/wiki/linux-install-pandas).

In _geec_analysis_ path:

	sudo pip install -r requirements.txt

You might have more success with

	sudo apt-get install python-pandas

### How To Use
- - - -

For more info on each parameter use the help flag

	python toolname.py --help

Annotate a matrix

    python geec_annotate.py --pdf output.pdf --tsv output.tsv epiGeEC_Correlate.mat epiGeEC_Datasets.json assay cell_type timepoint

Evaluate clusters

    python geec_ari.py epiGeEC_Correlate.mat epiGeEC_Datasets.json -b assay cell_type timepoint -r assay cell_type timepoint > output.ari

### License
- - - -
[GNU General Public License v3](LICENSE)