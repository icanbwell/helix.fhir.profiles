from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType
from spark_auto_mapper_fhir.value_sets.loinc_codes import LOINCCodesCode


class ProductFeatureCode(LOINCCodesCode):
    """
    bWell codeset representing product feature(s)
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    codeset: FhirUri = "https://www.icanbwell.com/product-feature-code"


class ProductFeatureCodeValues:

    # working values
    ProviderSearch = ProductFeatureCode("provider-search")
    IntegratedScheduling = ProductFeatureCode("integrated-scheduling")
    CareMeasure = ProductFeatureCode("care-measure")
    MedicareAdvantageProviderDirectory = ProductFeatureCode("mapd")
    Employment = ProductFeatureCode("employment")
    Person = ProductFeatureCode("Person")
    Mixpanel = ProductFeatureCode("mixpanel")
