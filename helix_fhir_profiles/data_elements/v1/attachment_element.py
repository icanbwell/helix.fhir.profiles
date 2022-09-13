from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataElementAttachment:
    @staticmethod
    def get_attachment_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "attachment"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".attachment"),
                    label=label,
                    short="An address expressed using postal conventions",
                    definition="A physical or postal address",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Address")]),
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_practitioner_photo(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "practitioner-photo"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat(resource, ".photo"),
                    path=A.concat(resource, ".photo"),
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="practitioner headshot",
                    alias=FhirList(["headshot", "picture"]),
                    min=0,
                    type_=FhirList([ElementDefinitionType(code="Attachment")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".photo.id"),
                    path=A.concat(resource, ".photo.id"),
                    label=label,
                    short="headshot",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".photo.contentType"),
                    path=A.concat(resource, ".photo.contentType"),
                    label=label,
                    short="image/jpg",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".photo.url"),
                    path=A.concat(resource, ".photo.url"),
                    label=label,
                    short="URL to the image",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="url")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".photo.title"),
                    path=A.concat(resource, ".photo.title"),
                    label=label,
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ]
        )
        return elements
