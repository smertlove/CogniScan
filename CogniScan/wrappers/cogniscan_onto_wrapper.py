from rdflib import Graph
from rdflib import RDF, OWL

import re


class CogniScanOntoWrapper:

    def __init__(self, path: str):
        self.g = Graph()
        self.g.parse(path)

        self.has_symptom_uri = self.get_uri_by_name("hasSymptom")
        self.has_description_uri = self.get_uri_by_name("hasDescription")

        self._q_diseases_by_symptom = """
            SELECT DISTINCT ?disease
            WHERE {{{{
                ?disease <{}> <{}> .
            }}}}
            ORDER BY ?disease_name
        """.format(self.has_symptom_uri, "{}")

        self._q_symptoms_by_disease = """
        SELECT DISTINCT ?symptom ?symptom_name
        WHERE {{{{
            <{}> <{}> ?symptom .
        }}}}
        ORDER BY ?symptom_name
        """.format("{}", self.has_symptom_uri)

        self._q_description_of_disease = """
        SELECT DISTINCT ?description
        WHERE {{{{
            <{}> <{}> ?description .
        }}}}
        """.format("{}", self.has_description_uri)


        stats = self.describe()
        max_key_len = max(len(str(k)) for k in stats.keys())
        max_val_len = max(len(str(v)) for v in stats.values())

        line_width = max_key_len + max_val_len + 10

        print("=" * line_width)
        print(f"ONTOLOGY STATISTICS".center(line_width))
        print("=" * line_width)
        
        for key, value in stats.items():
            display_name = key.replace('_', ' ').title()
            print(f"{display_name:<{max_key_len+2}}:{value:>{max_val_len+3}}")
        
        print("=" * line_width)

    def uri2name(self, uri: str):
        uri_str = str(uri)
            
        if '#' in uri_str:
            name = uri_str.split('#')[-1]
        else:
            name = uri_str.split('/')[-1]

        return name

    def get_uri_by_name(self, name: str, normalize=False):

        if normalize:
            name = re.sub("\s+", "_", name.capitalize())

        for uri in self.g.subjects():
            cur_name = self.uri2name(uri)

            if cur_name == name:
                return uri

        return None

    def query_my_onto(self, query):

        result = []
        for row in self.g.query(query):
            result.append(self.uri2name(row[0]))

        return result

    def get_diseases_by_symptom(self, symptom: str):
        symptom_uri = self.get_uri_by_name(symptom, normalize=True)
        query = self._q_diseases_by_symptom.format(symptom_uri)
        return self.query_my_onto(query)

    def get_symptoms_by_disease(self, disease: str):
        disease_uri = self.get_uri_by_name(disease, normalize=True)
        query = self._q_symptoms_by_disease.format(disease_uri)
        return self.query_my_onto(query)

    def get_description_of_disease(self, disease: str):
        disease_uri = self.get_uri_by_name(disease, normalize=True)
        query = self._q_description_of_disease.format(disease_uri)
        return self.query_my_onto(query)

    def describe(self):

        classes = list(self.g.subjects(RDF.type, OWL.Class))
        object_properties = list(self.g.subjects(RDF.type, OWL.ObjectProperty))
        datatype_properties = list(self.g.subjects(RDF.type, OWL.DatatypeProperty))
        individuals = list(self.g.subjects(RDF.type, OWL.NamedIndividual))

        return {
            "classes"            : len(classes),
            "object_properties"  : len(object_properties),
            "datatype_properties": len(datatype_properties),
            "individuals"        : len(individuals),
            "total_statements"   : len(self.g),
        }

