import dgidb
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

    # Gene search types work correctly
    query = 'braf'
    results = dgidb.get_interactions(query,search='genes')
    assert type(results) == type(pd.DataFrame())
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

    # Categories search builds a dataframe
    query = 'braf'
    results = dgidb.get_categories(query)
    assert type(results) == type(pd.DataFrame())

    # Categories does not return drugs data
    query = 'imatinib'
    results = dgidb.get_categories(query)
    assert len(results) == 0

    pass