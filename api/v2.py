import requests
import pandas as pd

class api_parser():
    def __init__(self):
        self.base_url = 'https://dgidb.org/api/v2/'
        self.base_local = 'https://127.0.0.1:8000/api/v2'
        pass

    def _additional_parameters(self):
        self.fda_approved = True


    def get_drug_interactions(self,gene):
        if isinstance(gene,str):
            r = requests.get(f"{self.base_url}interactions.json?genes={gene}")
        elif isinstance(gene,list):
            r = requests.get(f"{self.base_url}interactions.json?genes={','.join(gene)}")
        else:
            print('Bad request')

        self.results = r.json()
        pass

    def get_gene_interactions(self,drug):
        r = requests.get(f'{self.base_url}interactions.json?drugs={drug}')
        self.results = r.json()
        pass



    def _build_drug_interaction_results(self):
        searchTerm_list = []
        geneName_list = []
        entrezId_list = []
        drugName_list = []
        drugConceptId_list = []
        interactionTypes_list = []
        sources_list = []
        pmids_list = []
        score_list = []

        for match in self.results['matchedTerms']:
            current_searchTerm = match['searchTerm']
            current_geneName = match['geneName']
            current_entrezId = match['entrezId']

            for interaction in match['interactions']:
                searchTerm_list.append(current_searchTerm)
                geneName_list.append(current_geneName)
                entrezId_list.append(current_entrezId)

                drugName_list.append(interaction['drugName'])
                drugConceptId_list.append(interaction['drugConceptId'])
                interactionTypes_list.append(', '.join(interaction['interactionTypes']))
                sources_list.append(', '.join(interaction['sources']))
                pmids_list.append(', '.join(str(pmid) for pmid in interaction['pmids']))
                score_list.append(interaction['score'])
                pass

            self.search_results = pd.DataFrame(columns=['searchTerm','geneName','entrezId','drugName','drugConceptId','interactionTypes','sources','pmids','score'])
            self.search_results = self.search_results.assign(searchTerm=searchTerm_list,
                                                    geneName=geneName_list,
                                                    entrezId=entrezId_list,
                                                    drugName=drugName_list,
                                                    drugConceptId=drugConceptId_list,
                                                    interactionTypes=interactionTypes_list,
                                                    sources=sources_list,
                                                    pmids=pmids_list,
                                                    score=score_list)

        pass


    pass