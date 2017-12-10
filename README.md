# Outlier Detection

## Running the Code

* Simply clone the repository using ``git clone`` and run the Jupyter Notebooks locally

* The functions and method have been documented but you can refer to my talk to understand more about the work : https://indico.cern.ch/event/635481/contributions/2685048/

* The data slices have been provided (critical details obscured/modified) for this purpose, however the author and CERN Openlab retain the rights to all intellectual property resulting directly or indirectly from the use of this data


## Structure

* The Jupyter Notebooks stored in the ``src`` directory are named according to the models each one utilises to analyse the data
* There are some pre-determined anomalies observed when using OCSVM as well as IsolationForests stored in the txt file inside the ``anomalies`` directory; these can be used as reference when attempting to replicate the results
* The folders ``old`` and ``v1`` have been kept in the repository for purposes of historical reference and do not impact the working of the notebooks in any manner
* Python scripts (``knn.py`` and others) within the ``src`` directory have also been stored for purpose of historical reference

The most recent version of the code will be released following completion of final formalities for publication (Jan-Feb 2018). If you should require it for reference purposes, please contact me by email at swapneel.mehta@djsce.edu.in

### Notes

* This repository provides some proof-of-concept work released as a precursor to the final models developed as part of the Openlab Summer Student Program at CERN
* We use scikit-learn to efficiently analyse slices of the data pulled from the "data lake" stored both on HDFS as well as Elastcsearch

