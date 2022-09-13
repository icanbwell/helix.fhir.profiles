from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding

from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.list import FhirList


class DataBackboneElementPractitionerQualification:
    @staticmethod
    def get_practitioner_qualification(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "qualification"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat(resource, ".qualification"),
                    path=A.concat(resource, ".qualification"),
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    alias=FhirList(["provider title", "credential", "suffix"]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".qualification.id"),
                    path=A.concat(resource, ".qualification.id"),
                    short="set to qualification code",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".qualification.code"),
                    path=A.concat(resource, ".qualification.code"),
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".qualification.period"),
                    path=A.concat(resource, ".qualification.period"),
                    short="Period during which the qualification is valid",
                    comment="period.start set to provier's medical school graduation date",
                    alias=FhirList(
                        ["provider effective date", "provider termination date"]
                    ),
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Period")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".qualification.period.start"),
                    path=A.concat(resource, ".qualification.period.start"),
                    label=label,
                    short="Credential start date",
                    alias=FhirList(["medical school graduation date"]),
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="dateTime")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".qualification.period.end"),
                    path=A.concat(resource, ".qualification.period.end"),
                    label=label,
                    short="Termination date of the credential",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="dateTime")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".qualification.issuer"),
                    path=A.concat(resource, ".qualification.issuer"),
                    label=label,
                    alias=FhirList(["medical school"]),
                    min=0,
                    max="1",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                # targetProfile=FhirList()
                            )
                        ]
                    ),
                ),
            ],
            True,
        )

        return elements
