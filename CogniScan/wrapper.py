from owlready2 import *
from collections import defaultdict


def _normalize(symptom: str):

    normalized_symptom = [symptom[0].lower()]
    
    for char in symptom[1:]:
        if char.isupper():
            normalized_symptom.append(" ")
        normalized_symptom.append(char.lower())

    return "".join(normalized_symptom)


class DRPSNPTO_Wrapper:
    def __init__(self, p: str):
        self.onto = get_ontology(p).load()
        print("Ontology loaded successfully!")
        print(f"Ontology name: {self.onto.name}")
        print(f"Ontology base IRI: {self.onto.base_iri}")

        print(f"Number of classes: {len(list(self.onto.classes()))}")
        print(
            f"Number of object properties: {len(list(self.onto.object_properties()))}"
        )
        print(f"Number of data properties: {len(list(self.onto.data_properties()))}")
        print(f"Number of individuals: {len(list(self.onto.individuals()))}")

        symptoms = [
            "AuditoryHallucination",
            "AvoidArguingWithPatientAboutValidityOfHallucination",
            "BizarreDelusion",
            "Delusion",
            "DelusionOfBeingControlled",
            "DelusionOfGuilt",
            "DelusionOfImpoverishment",
            "DelusionOfReference",
            "ErotomanicDelusion",
            "GrandioseDelusion",
            "GustatoryHallucination",
            "Hallucination",
            "HypnagogicHallucination",
            "HypnopompicHallucination",
            "JealousDelusion",
            "MisidentificationDelusion",
            "NihilisticDelusion",
            "OlfactoryHallucination",
            "PersecutoryDelusion",
            "PsychoticSymptomCompletelyStop",
            "PsychoticSymptomInDementia",
            "PsychoticSymptomStabilize",
            "ReligiousDelusion",
            "SomaticDelusion",
            "SomaticHallucination",
            "TactileHallucination",
            "VisualHallucination",
        ]

        self.symptoms = dict()

        for symptom in symptoms:
            self.symptoms[symptom.lower()] = symptom
            self.symptoms[_normalize(symptom).lower()] = symptom

    def find_classes_by_keyword(self, keyword):
        """Find classes containing a specific keyword"""
        matching_classes = []
        for cls in self.onto.classes():
            if hasattr(cls, 'name') and keyword.lower() in cls.name.lower():
                matching_classes.append(cls)
        return matching_classes

    ## NOTE: Это можно и НУЖНО переписать нормально.
    def get_diseases_for_symptom(self, symptom: str):

        symptom_name = self.symptoms[symptom.lower()]
        print(symptom_name)
        if symptom_name is None:
            return []

        diseases_list = []

        symptom_class = self.onto.search_one(iri=f"*{symptom_name}")

        causes_property = self.onto.search_one(iri="*causes")
        if causes_property:
            for cls in self.onto.classes():
                if hasattr(cls, 'name') and hasattr(cls, causes_property.name):
                    prop_value = getattr(cls, causes_property.name)
                    if symptom_class in prop_value:
                        description = f"Causes {symptom_class.name} as a psychotic symptom"
                        diseases_list.append({
                            "disease": cls.name,
                            "disease_description": str((cls.definition or [""])[0]),
                            "description": description
                        })

        if hasattr(symptom_class, 'is_a'):
            for parent in symptom_class.is_a:
                if (hasattr(parent, 'name') and 
                    parent.name != 'Thing' and 
                    parent.name not in ['ObjectProperty', 'hasPsychoticSymptom']):
                    
                    description = f"Parent class of {symptom_class.name}"
                    diseases_list.append({
                        "disease": parent.name,
                        "disease_description": str((parent.definition or [""])[0]),
                        "description": description
                    })

        is_caused_by_property = self.onto.search_one(iri="*isCausedBy")
        if is_caused_by_property and hasattr(symptom_class, is_caused_by_property.name):
            prop_value = getattr(symptom_class, is_caused_by_property.name)
            for item in prop_value:
                if hasattr(item, 'name'):
                    description = f"Identified as a causative factor for {symptom_class.name}"
                    diseases_list.append({
                        "disease": item.name,
                        "disease_description": str((item.definition or [""])[0]),
                        "description": description
                    })

        unique_diseases = []
        seen_diseases = set()
        for disease in diseases_list:
            if disease["disease"] not in seen_diseases:
                unique_diseases.append(disease)
                seen_diseases.add(disease["disease"])

        unique_diseases.sort(key=lambda x: x["disease"])

        return unique_diseases
