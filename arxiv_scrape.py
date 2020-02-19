

"""
Usage:

arxiv_scrape.py --query_type abs --query_words 'machine+learning' --start=1000 --max_results=2000

"""



import urllib
import feedparser
import urllib.request
import pandas as pd
import time
import os
import re
import argparse


def read_parse_url(url):
    with urllib.request.urlopen(url) as url:
        try:
            data = url.read()
        except urllib.HTTPError as e:
            if e.code == 503:
                to = int(e.hdrs.get("retry-after", 30))
                print
                "Got 503. Retrying after {0:d} seconds.".format(to)

                time.sleep(to)
            else:
                raise
    feed = feedparser.parse(data)
    return feed



def process_feed(feed):
    
    my_dict = {'ID':[], 'date':[], 'title':[], 'author':[],
               'link':[], 'journal':[], 'comments':[], 
               'primary_cat':[], 'all_cat':[], 'abstract':[]}
    
    
    for entry in feed.entries:
        my_dict['ID'].append(entry.id.split('/abs/')[-1])
        my_dict['date'].append(entry.published)
        my_dict['title'].append(entry.title)
        my_dict['author'].append(','.join(author.name for author in entry.authors))
    
        for link in entry.links:
            if link.rel == 'alternate':
                my_link =  link.href
        my_dict['link'].append(my_link)
    
        try:
            journal_ref = entry.arxiv_journal_ref
        except AttributeError:
            journal_ref = 'None'
        my_dict['journal'].append(journal_ref)

        try:
            comment = entry.arxiv_comment
        except AttributeError:
            comment = 'None'
        my_dict['comments'].append(comment)

        my_dict['primary_cat'].append(entry.tags[0]['term'])
    
        all_categories = [t['term'] for t in entry.tags]
        my_dict['all_cat'].append(all_categories)
        
        my_dict['abstract'].append(entry.summary)

    
    query_df = pd.DataFrame(my_dict)
    
    return query_df





if __name__== '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--query_type", default=None, type=str, required=False)
    parser.add_argument("--query_words", default=None, type=str, required=False)
    parser.add_argument("--max_results", default=2000, type=int, required=False)
    parser.add_argument("--start", default=0, type=int, required=False)

    args = parser.parse_args()


    init_time = time.time()    
    data_available = True

    search_query=args.query_type+':%22'+args.query_words+'%22'

    base_url = 'http://export.arxiv.org/api/query?'
#   search_query = 'ti:%22neural+networks%22'
#    search_query = 'abs:%22string+theory%22'
    max_results = args.max_results
    my_sorting = 'sortBy=submittedDate&sortOrder=descending'
    start = args.start

    print('Starting query for the string: %s' %search_query)


    while data_available:

        my_query = 'search_query=%s&start=%i&max_results=%i&%s' % (search_query,
                                                     start,
                                                     max_results,
                                                      my_sorting )
    
        my_url = base_url+my_query
        
        my_feed = read_parse_url(my_url)
        
        if len(my_feed.entries)==0:
            data_available = False
            print('No more data found.')
    
    
        query_df_slice = process_feed(my_feed)

        try:
           query_df = pd.concat([query_df,query_df_slice])
        except NameError:
            query_df = query_df_slice
        
        if query_df.shape[0]%1000 == 0:
            print('Fetched %s data (last slice from %s to %s)' %(query_df.shape[0],start, start+max_results ))
    
        start += max_results
        
    
    
    query_time = time.time()-init_time
    print('Query completed in %s sec.' %query_time)
    
    ctime = time.strftime('%Y-%m-%d_%H:%M')
    fname = os.getcwd() + '/data/query_at_'+ctime+'_' +re.sub('%22', '', search_query)+'.csv'

    print('Saving dataframe to: '+ fname)
    
    query_df.to_csv(fname, header=True, index=False)
    
    print('Summary: \n %s articles found \n first paper: %s  ' %(query_df.shape[0], query_df.iloc[query_df.shape[0]-1,1]))
    
    
    
