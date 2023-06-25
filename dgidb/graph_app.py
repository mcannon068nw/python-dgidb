import dgidb
import network_graph as ng

import tkinter as tk

def create_interactions_network():
    genes = ['BRAF','ABL1','BCR','PDGFRA']
    drugs = ['IMATINIB','OLARATUMAB','DASATINIB','NELOTINIB']
    
    gene_interactions = dgidb.get_interactions(genes)
    drug_interactions = dgidb.get_interactions(drugs,search='drugs')

    ng.create_network(gene_interactions)

def save_graph():
    ng.save_graph()

def generate_UI():
    window = tk.Tk()
    window.title("NetworkX Graph")

    window.mainloop()