import requests
import pandas as pd
import json

def get_drug(terms,use_pandas=True):

    base_url  = 'http://localhost:3000/api/graphql'

    if isinstance(terms,list):
        terms = '\",\"'.join(terms)

    query = "{\ndrugs(name: [\"" + terms.upper() + "\"]) {\nname\ndrugAliases {\nalias\n}\ndrugAttributes {\nname\nvalue\n}\nantiNeoplastic\nimmunotherapy\napproved\ndrugApprovalRatings {\nid\n}\ndrugApplications {\nappNo\n}\n}\n}\n"

    r = requests.post(base_url, json={'query': query})

    if use_pandas == True:
        data = __process_drug(r.json())
    elif use_pandas == False:
        data = r.json()

    return(data)

def get_interactions(terms,search='genes',use_pandas=True):

    base_url  = 'http://localhost:3000/api/graphql'

    if isinstance(terms,list):
        terms = '\",\"'.join(terms)

    if search == 'genes':
        query = "{\ngenes(name: [\"" + terms.upper() + "\"]) {\nname\nlongName\ngeneCategories{\nname\n}\ninteractions {\ninteractionAttributes {\nname\nvalue\n}\ndrug {\nname\napproved\n}\ninteractionScore\ninteractionClaims {\npublications {\npmid\ncitation\n}\nsource {\nfullName\nid\n}\n}\n}\n}\n}"
    elif search == 'drugs':
        query = "{\ndrugs(name: [\"" + terms.upper() + "\"]){\nname\napproved\ninteractions {\ngene {\nname\n}\ninteractionAttributes {\nname\nvalue\n}\ninteractionScore\ninteractionClaims {\npublications {\npmid\ncitation\n}\nsource {\nfullName\nid\n}\n}\n}\n}\n}"
    else:
        raise Exception("Search type must be specified using: search='drugs' or search='genes'")

    r = requests.post(base_url, json={'query': query})

    if use_pandas == True:
        if search == 'genes':
            data = __process_gene_search(r.json())
        elif search == 'drugs':
            data = __process_drug_search(r.json())
        else:
            raise Exception("Search type must be specified using: search='drugs', or search='genes'")

    elif use_pandas == False:
        return(r.json())

    return(data)

def get_categories(terms,use_pandas=True):

    base_url  = 'http://localhost:3000/api/graphql'

    if isinstance(terms,list):
        terms = '\",\"'.join(terms)

    query = "{\ngenes(name: [\"" + terms.upper() + "\"]) {\nname\nlongName\ngeneCategoriesWithSources{\nname\nsourceNames\n}\n}\n}"
    r = requests.post(base_url, json={'query': query})

    if use_pandas == True:
        data = __process_gene_categories(r.json())
    elif use_pandas == False:
        data = r.json()

    return(data)

def __process_drug(results):
    drug_list = []
    alias_list = []
    attribute_list = []
    antineoplastic_list = []
    immunotherapy_list = []
    approved_list = []

    for match in results['data']['drugs']:
        drug_list.append(match['name'])
        alias_list.append("|".join([alias['alias'] for alias in match['drugAliases']]))
        current_attributes = [": ".join([attribute['name'],attribute['value']]) for attribute in match['drugAttributes']]
        attribute_list.append(" | ".join(current_attributes))
        antineoplastic_list.append(str(match['antiNeoplastic']))
        immunotherapy_list.append(str(match['immunotherapy']))
        approved_list.append(str(match['approved']))

    data = pd.DataFrame().assign(drug=drug_list,
                                    aliases=alias_list,
                                    attributes=attribute_list,
                                    antineoplastic=antineoplastic_list,
                                    immunotherapy=immunotherapy_list,
                                    approved=approved_list)


    return(data)


def __process_gene_search(results):
    interactionscore_list = []
    drugname_list = []
    approval_list = []
    interactionattributes_list = []
    gene_list = []
    longname_list = []
    sources_list = []
    pmids_list = []
    genecategories_list = []

    for match in results['data']['genes']:
        current_gene = match['name']
        current_longname = match['longName']

        # TO DO: Evaluate if categories should be returned as part of interactions search. Seems useful but also redundant?
        list_string = []
        for category in match['geneCategories']:
            list_string.append(f"{category['name']}")
        current_genecategories = " | ".join(list_string)

        for interaction in match['interactions']:
            gene_list.append(current_gene)
            genecategories_list.append(current_genecategories)
            longname_list.append(current_longname)
            drugname_list.append(interaction['drug']['name'])
            approval_list.append(str(interaction['drug']['approved']))
            interactionscore_list.append(interaction['interactionScore'])

            list_string = []
            for attribute in interaction['interactionAttributes']:
                list_string.append(f"{attribute['name']}: {attribute['value']}")
            interactionattributes_list.append(" | ".join(list_string))

            list_string = []
            for claim in interaction['interactionClaims']:
                list_string.append(f"{claim['source']['fullName']}")
                sub_list_string = []
                for publication in claim['publications']:
                    sub_list_string.append(f"{publication['pmid']}")
            sources_list.append(" | ".join(list_string))
            pmids_list.append(" | ".join(sub_list_string))

    data = pd.DataFrame().assign(gene=gene_list,
                                            longname=longname_list,
                                            categories=genecategories_list,
                                            drug=drugname_list,
                                            approval=approval_list,
                                            score=interactionscore_list,
                                            interaction_attributes=interactionattributes_list,
                                            source=sources_list,
                                            pmid=pmids_list)
    return(data)

def __process_gene_categories(results):
    gene_list = []
    categories_list = []
    sources_list = []
    longname_list = []

    for match in results['data']['genes']:
        current_gene = match['name']
        current_longname = match['longName']

        for category in match['geneCategoriesWithSources']:
            gene_list.append(current_gene)
            longname_list.append(current_longname)
            categories_list.append(category['name'])
            sources_list.append(' | '.join(category['sourceNames']))

        pass

    data = pd.DataFrame().assign(gene=gene_list,
                                longname=longname_list,
                                categories=categories_list,
                                sources=sources_list)


    return(data)

def __process_drug_search(results):
    interactionscore_list = []
    genename_list = []
    approval_list = []
    interactionattributes_list = []
    drug_list = []
    sources_list = []
    pmids_list = []

    for match in results['data']['drugs']:
        current_drug = match['name']
        current_approval = (str(match['approved']))

        for interaction in match['interactions']:
            drug_list.append(current_drug)
            genename_list.append(interaction['gene']['name'])
            interactionscore_list.append(interaction['interactionScore'])
            approval_list.append(current_approval)

            list_string = []
            for attribute in interaction['interactionAttributes']:
                list_string.append(f"{attribute['name']}: {attribute['value']}")

            interactionattributes_list.append("| ".join(list_string))

            list_string = []
            for claim in interaction['interactionClaims']:
                list_string.append(f"{claim['source']['fullName']}")
                sub_list_string = []
                for publication in claim['publications']:
                    sub_list_string.append(f"{publication['pmid']}")

            sources_list.append(" | ".join(list_string))
            pmids_list.append(" | ".join(sub_list_string))

    data = pd.DataFrame().assign(drug=drug_list,
                                gene=genename_list,
                                approval=approval_list,
                                score=interactionscore_list,
                                interaction_attributes=interactionattributes_list,
                                source=sources_list,
                                pmid=pmids_list)
    return(data)
