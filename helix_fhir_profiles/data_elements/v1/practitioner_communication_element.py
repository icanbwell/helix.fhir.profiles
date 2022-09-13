from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.list import FhirList


class DataElementCommunication:
    @staticmethod
    def get_language(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "language"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".communication"),
                    label=label,
                    short="A language the practitioner can use in patient communication",
                    # definition="",
                    # comment="",
                    # requirements="",
                    alias=FhirList(["spoken language", "communication"]),
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".communication.id"),
                    label=label,
                    short="set to code",
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding"),
                    path=A.concat(resource, ".communication.coding"),
                    label=label,
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding.id"),
                    path=A.concat(resource, ".communication.coding.id"),
                    label=label,
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding.system"),
                    path=A.concat(resource, ".communication.coding.system"),
                    label=label,
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding.code"),
                    path=A.concat(resource, ".communication.coding.code"),
                    label=label,
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding.display"),
                    path=A.concat(resource, ".communication.coding.display"),
                    label=label,
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ],
            True,
        )

        return elements
