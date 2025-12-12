from rdflib import Graph
import re


class CogniScanOntoWrapper:

    def __init__(self, path: str):
        self.g = Graph()
        self.g.parse(path)

        self.has_symptom_uri = self.get_uri_by_name("hasSymptom")
        self.has_description_uri = self.get_uri_by_name("hasDescription")

        self._q_diseases_by_symptom = """
            SELECT DISTINCT ?disease
            WHERE {{
                ?disease <{0}> <{1}> .
            }}
            ORDER BY ?disease_name
        """.format(self.has_symptom_uri, "{1}")

        self._q_symptoms_by_disease = """
        SELECT DISTINCT ?symptom ?symptom_name
        WHERE {{
            <{0}> <{1}> ?symptom .
        }}
        ORDER BY ?symptom_name
        """.format("{0}", self.has_symptom_uri)

        self._q_description_of_disease = """
        SELECT DISTINCT ?description
        WHERE {{
            <{0}> <{1}> ?symptom .
        }}
        """.format("{0}", self.has_description_uri)

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
        return self.g.query(query)

    def get_diseases_by_symptom(self, symptom: str):
        query = self._q_diseases_by_symptom.format(symptom)
        return self.query_my_onto(query)

    def get_symptoms_by_disease(self, disease: str):
        query = self._q_symptoms_by_disease.format(disease)
        return self.query_my_onto(query)

    def get_description_of_disease(self, disease: str):
        print(self._q_description_of_disease)
        query = self._q_description_of_disease.format(disease)
        return self.query_my_onto(query)



