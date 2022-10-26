from dgidb import dgidb
import requests
import pandas as pd
import pytest


def test_get_interactions():
    """Test that interactions works correctly"""

    # Search types work correctly
    query = 'braf'
    with pytest.raises(Exception) as excinfo:
        results = dgidb.get_interactions(query,search='fake')
    assert "Search type must be specified" in str(excinfo.value)

    # Default search type functions correct as 'gene' and not 'drug'
    query = 'imatinib'
    results = dgidb.get_interactions(query)
    assert len(results) == 0

    # Use pandas default is correctly set to 'true'
    query = 'braf'
    results = dgidb.get_interactions(query)
    assert type(results) == type(pd.DataFrame())

    # Use pandas can be toggled to 'false' and returns a dictionary response object
    query = 'braf'
    results = dgidb.get_interactions(query,use_pandas=False)
    assert type(results) != type(pd.DataFrame())
    assert type(results) == type(dict())

    # Gene search types work correctly
    query = 'braf'
    results = dgidb.get_interactions(query,search='genes')
    assert results.columns[0] == 'gene'

    # Gene search is not grabbing drugs
    query = 'imatinib'
    results = dgidb.get_interactions(query,search='genes')
    assert len(results) == 0

    # Drug search types work correctly
    query = 'imatinib'
    results = dgidb.get_interactions(query,search='drugs')
    assert type(results) == type(pd.DataFrame())
    assert results.columns[0] == 'drug'

    # Drug search is not grabbing genes
    query = 'braf'
    results = dgidb.get_interactions(query,search='drugs')
    assert len(results) == 0

    pass

def test_get_categories():
    """Test that categories works correctly"""

    # Categories search builds a dataframe (with use_pandas default set to 'true')
    query = 'braf'
    results = dgidb.get_categories(query)
    assert type(results) == type(pd.DataFrame())

    # Categories does not return drugs data
    query = 'imatinib'
    results = dgidb.get_categories(query)
    assert len(results) == 0

    # Use pandas can be toggled to 'false' and returns a dictionary response object
    query = 'imatinib'
    results = dgidb.get_categories(query,use_pandas=False)
    assert type(results) != type(pd.DataFrame())
    assert type(results) == type(dict())

    pass

def test_get_drugs():
    """Test that drug profile works correctly"""

    # Drug search builds a dataframe (with use_pandas default set to 'true')
    query = 'imatinib'
    results = dgidb.get_drug(query)
    assert type(results) == type(pd.DataFrame())

    # Drug search does not return gene data
    query = 'braf'
    results = dgidb.get_drug(query)
    assert(len(results)) == 0

    # Use pandas can be toggled to 'false' and returns dictionary response object
    query = 'imatinib'
    results = dgidb.get_drug(query,use_pandas=False)
    assert type(results) != type(pd.DataFrame())
    assert type(results) == type(dict())


