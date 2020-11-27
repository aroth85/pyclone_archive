# Installation

To install PyClone make sure you have the necessary libraries (listed below) installed. After that PyClone installs like
any other Python package with `python setup.py install`.

If the installation worked correctly the `PyClone` command should now be available.

## Dependencies

### Required

The following packages are required to perform a basic analysis with PyClone.

* [PyDP >= 0.2.0](https://bitbucket.org/aroth85/pydp)

* [PyYAML >= 3.10](http://pyyaml.org)

### Optional

The following libraries are required to use the clustering and plotting capabilities of PyClone.

* [brewer2mpl >= 1.0] (https://github.com/jiffyclub/brewer2mpl) - Required for plotting.

* [eppl >= 0.1.0] (https://bitbucket.org/aroth85/eppl)

* [maplotlib >= 1.2.0](http://matplotlib.org) - Required for plotting.

* [numpy >= 1.6.2](http://www.numpy.org) - Required for plotting and clustering.

* [pandas >= 0.11] (http://pandas.pydata.org) - Required for multi sample plotting.

* [rpy2 >= 2.3.3](http://rpy.sourceforge.net/rpy2.html) - Only necessary to use the dynamic_tree_cut clustering method. The dynamicTreeCut tree cut package should also be installed in R.

* [scikits-learn >= 0.13](http://scikit-learn.org) - Only necessary to use affinity_propogation, dbscan, spectral_clustering clustering methods. 

* [scipy >= 0.11](http://www.scipy.org) - Required for plotting and clustering.