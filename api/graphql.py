import requests
import pandas as pd
import json

class graphql_parser():
    def __init__(self):
        self.base_url  = 'http://localhost:3000/api/graphql'
        pass

    def post_query(self,gene):

        if isinstance(gene,list):
            gene = '\",\"'.join(gene)

        query = "{\ngenes(name: [\"" + gene + "\"]) {\nname\nlongName\ninteractions {\ninteractionAttributes {\nname\nvalue\n}\ndrug {\nname\napproved\n}\ninteractionScore\ninteractionClaims {\npublications {\npmid\ncitation\n}\nsource {\nfullName\nid\n}\n}\n}\n}\n}"
        r = requests.post(self.base_url, json={'query': query})
        self.results = r.json()
        pass

    def process_results(self):
        interactionscore_list = []
        drugname_list = []
        approval_list = []
        interactionattributes_list = []
        gene_list = []
        longname_list = []
        sources_list = []
        pmids_list = []

        for match in self.results['data']['genes']:
            current_gene = match['name']
            current_longname = match['longName']

            for interaction in match['interactions']:
                gene_list.append(current_gene)
                longname_list.append(current_longname)
                drugname_list.append(interaction['drug']['name'])
                approval_list.append(str(interaction['drug']['approved']))

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

        self.data = pd.DataFrame().assign(gene=gene_list,
                                                longname=longname_list,
                                                drug=drugname_list,
                                                approval=approval_list,
                                                interaction_attributes=interactionattributes_list,
                                                source=sources_list,
                                                pmid=pmids_list)
        pass

    pass # end class

