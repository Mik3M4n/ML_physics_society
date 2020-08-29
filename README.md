
# Machine Learning on the ArXiv and non-neutrality of science

This repo contains the tools to reproduce the plots in the paper *''(Non)-neutrality of science and algorithms: Machine Learning between fundamental physics and society''*, published in Italian on the journal  [The Lab's Quarterly](https://thelabsquarterly.files.wordpress.com/2019/04/2018.4-the-labs-quarterly-5.-aniello-lampo-michele-mancarella-angelo-piga-1.pdf). The english version can be found on the arXiv [2006.10745 [physics.soc-ph]](https://arxiv.org/abs/2006.10745).




## Description

1) Data collection

The script arxiv_scrape.py launches a query using the ArXiv API

* query_type can be either 'ti' (for title) or 'abs' (for abstract)
* query_words is a string to search for
* start is an integer that indicates from which result to start retrieving papers (e.g. --start=1000 means that the results will be collected starting from the 1000th paper on). This is useful for long queries, since the API may not retrieve all results at once and multiple runs may be needed. To be sure that all results have been retrieved, it is good practise to manually check the number of expected results with the arXiv manual advanced search
* max_results indicates the max number of results to look for in a sigle query


Usage:
```
arxiv_scrape.py --query_type abs --query_words 'machine+learning' --start=1000 --max_results=2000
```

2) Data analysis

The notebook arxiv_analysis contains the analysis of the results and allows to reproduce the plots in the paper
