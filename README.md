
# Machine Learning on the ArXiv and non-neutrality of science

This repo contains the tools to reproduce the plots in the paper *''(Non)-neutrality of science and algorithms: Machine Learning between fundamental physics and society''*, published in italian on the journal  [The Lab's Quarterly](http://www.thelabs.sp.unipi.it}{The Lab's Quarterly). The english version can be found on the ArXiv.




## Description

1) Data collection

The script arxiv_scrape.py launches a query using the ArXiv API

* query_type can be either 'ti' (for title) or 'abs' (for abstract)
* query_words is a string to search for
* start is an integer that indicates from which result to start retrieving papers (e.g. --start=1000 means that the results will be collected starting from teh 1000th paper on). This is useful for long queries, since the API may not retrieve all results at once and multiple runs may be needed. To be sure that all results have been retrieved, it is good practise to manually check the number of expected results wiht the arXiv manual advanced search
* max_results indicates the max nulber of results to look for in a sigle query


Usage:
```
arxiv_scrape.py --query_type abs --query_words 'machine+learning' --start=1000 --max_results=2000
```

2) Data analysis

The notebook arxiv_analysis contains tha analysis of the results and allows to reproduce the plots in the paper
