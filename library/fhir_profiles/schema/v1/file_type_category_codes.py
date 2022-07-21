from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType
from spark_auto_mapper_fhir.value_sets.definition_use_codes import (
    DefinitionUseCodesCode,
)


class FileTypeCategoryCode(DefinitionUseCodesCode):
    """
    bWell codeset representing legacy flat file type categories
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    codeset: FhirUri = "https://www.icanbwell.com/file-category-code"


class FileTypeCategoryCodeValues:
    ElibilityFile = FileTypeCategoryCode("eligibility")
    EmployeeFile = FileTypeCategoryCode("employee")
    MedicalClaimsFile = FileTypeCategoryCode("med-claims")
    RxClaimsFile = FileTypeCategoryCode("rx-claims")
    ProviderRoster = FileTypeCategoryCode("provider-roster")
