# Versions

## 0.12.1

* Fixed typos in some example files.

* Added command to plot parallel coordinates for multiple samples.

* Updated interface of plotting commands to take configuration files as arguments instead of traced directory.

## 0.12.0

* Changed input files to work from YAML config instead of command line arguments.

* Added ability to do multiple sample analysis.

* Added robust Beta-Binomial version of PyClone.

* Added genotype naive clustering DP methods with Gaussian, Binomial and Beta-Binomial densities.

* Updated and renamed the `build_inputs` -> `build_mutations_file` function for building YAML inputs from tsv file.

## 0.11.3

* Fixed overflow in mpear clustering.

## 0.11.1

* Small change to clustering to use mutation_id not mutation in output, to make consistent with simple input.

## 0.11

* Reverted to PyDP for implementing DP methods.

* Removed dependency on numpy in analysis code.

## Older

* Unfortunately I did not keep a complete list of changes as the software evolved.