# pySEACR
Python3 implementation of [SEACR](https://github.com/FredHutch/SEACR).

## SEACR: *S*parse *E*nrichment *A*nalysis for *C*UT&*R*UN

SEACR is intended to call peaks and enriched regions from sparse CUT&RUN or chromatin profiling data in which background is dominated by "zeroes" (i.e. regions with no read coverage). It requires bedgraphs from paired-end sequencing as input, which can be generated from *read pair* BED files (i.e. BED coordinates reflecting the 5' and 3' termini of each read pair) using bedtools genomecov with the "-bg" flag, or alternatively from name-sorted paired-end BAM files as described in "Preparing input bedgraph files" below.

A description of the method can be found in the following manuscript, which we respectfully request that you cite if you find SEACR useful in your research:

Meers MP, Tenenbaum D, Henikoff S. (2019). Peak calling by Sparse Enrichment Analysis for CUT&RUN chromatin profiling. *Epigenetics and Chromatin* 12(1):42.

Direct link: https://doi.org/10.1186/s13072-019-0287-4

## Usage:

	python3 -m pySEACR treatment bedgraph [ control bedgraph | numeric threshold ] [ -n ] [ -s ]

## Description of input fields:

treatment bedgraph: Target data bedgraph file in UCSC bedgraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html).

control bedgraph: Control (IgG) data bedgraph file to generate an empirical threshold for peak calling.

numeric threshold: Alternatively, a numeric threshold *n* between 0 and 1 returns the top *n* fraction of peaks based on total signal within peaks.

--norm -n: Normalize control to target data. This option is recommended unless experimental and control data are already rigorously normalized to each other (e.g. via spike-in).

--stringent -s: by default, pySEACR uses a total signal threshold between the knee and peak of the total signal curve, and corresponds to the “relaxed” mode described in the text. The “stringent” options uses the peak of the curve, and corresponds to “stringent” mode.

## Preparing input bedgraph files

Bedgraph files should reflect density across *read pairs* rather than individual reads. If starting from BAM files, we recommend converting to paired end BED files using bedtools bamtobed with the -bedpe flag, then selecting the 5' and 3' coordinates of the read pair to generate a new BED3 file, and finally converting that file to a bedgraph using bedtools genomecov.

Here is some example code for converting from a paired-end BAM to a fragment bedgraph file as described above:

	bedtools bamtobed -bedpe -i $sample.bam > $sample.bed
	awk '$1==$4 && $6-$2 < 1000 {print $0}' $sample.bed > $sample.clean.bed
	cut -f 1,2,6 $sample.clean.bed | sort -k1,1 -k2,2n -k3,3n > $sample.fragments.bed
	bedtools genomecov -bg -i $sample.fragments.bed -g my.genome > $sample.fragments.bedgraph

## Output:
Unlike the original SEACR, pySEACR prints results to stdout.

## Output data structure:

	<chr>	<start>	<end>	<total signal>	<max signal>	<max signal region>

## Description of output fields:

Field 1: Chromosome

Field 2: Start coordinate

Field 3: End coordinate

Field 4: Total signal contained within denoted coordinates

Field 5: Maximum bedgraph signal attained at any base pair within denoted coordinates

Field 6: Region representing the farthest upstream and farthest downstream bases within the denoted coordinates that are represented by the maximum bedgraph signal

## Examples:

	python3 -m pySEACR target.bedgraph IgG.bedgraph -n -s > output
Calls enriched regions in target data using normalized IgG control track with stringent threshold

	python3 -m pySEACR target.bedgraph IgG.bedgraph > output
Calls enriched regions in target data using non-normalized IgG control track with relaxed threshold

	python3 -m pySEACR target.bedgraph 0.01 -s > output
Calls enriched regions in target data by selecting the top 1% of regions by AUC

## Differences between SEACR and pySEACR
* pySEACR uses different commandline options.
    * Normalization is a flag option now (-n).
    * pySEACR uses the relaxed threshold by default and will use the stringent with the -s flag.
* pySEACR writes results to stdout instead of a named file.
* pySEACR uses scikit-learn's kernel density estimator for normalization while SEACR uses R's implementation. The two methods rarely produce the same results.
