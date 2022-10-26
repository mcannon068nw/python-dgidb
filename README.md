# python-dgidb
Python API for accessing DGIdb database. Currently supported searches will return individual interaction data for drugs or genes, category annotations for genes, or information for drugs.

## Using python-dgidb:
python-dgidb must be imported first:

    from dgidb import dgidb

python-dgidb sends a pre-defined graphql query with user determined parameters to dgidb v5. Response objects are built into a dataframe using Pandas and returned to the user for readability, ease of use. Users can skip dataframe generation and instead receive the response object by setting use_pandas=False for most search functions.

Currently supported searches:

    dgidb.get_drug(terms, use_pandas=True)

    dgidb.get_categories(terms, use_pandas=True)

    dgidb.get_interactions(terms, search='genes', use_pandas=True)
    dgidb.get_interactions(terms, search='drugs', use_pandas=True)

Search terms support list or string format inputs (e.g. terms=['BRAF','ABL1'] or terms='BRAF'). Interaction searches default to genes but can also accept drugs if search='drugs'.

## TO DO:
- [ ] More parameter options for searches (i.e. approved, immunotherapy, antineoplastic)
- [ ] Implement search for just gene information (similar to get_drug)
- [ ] Make drugApplications and appNo fields accessible for drug information
- [ ] Implement metadata support (i.e. get_source)
