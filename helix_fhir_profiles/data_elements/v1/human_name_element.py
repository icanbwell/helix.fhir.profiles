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


class DataElementHumanName:
    @staticmethod
    def get_human_name_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "person-name"
        element_list = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".name"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.Person,
                            ),
                        ]
                    ),
                    short="An individual's name",
                    # definition="",
                    # comment="",
                    # requirements=
                    type_=FhirList([ElementDefinitionType(code="HumanName")]),
                    # example=FhirList([]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".name.id"),
                    label=A.text(label),
                    short="source prefix - name",
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".use"),
                    path=A.concat(resource, ".name.use"),
                    label=A.text(label),
                    short="usual | official | temp | nickname | anonymous | old | maiden",
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".text"),
                    path=A.concat(resource, ".name.text"),
                    label=A.text(label),
                    short="Full text representation of the full name",
                    alias=FhirList(["full name"]),
                    min=1,
                    max="1",
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".family"),
                    path=A.concat(resource, ".name.family"),
                    label=A.text(label),
                    short="Last name",
                    alias=FhirList(["last name", "surname"]),
                    min=1,
                    max="1",
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".given"),
                    path=A.concat(resource, ".name.given"),
                    label=A.text(label),
                    short="First and middle names",
                    min=1,
                    max="*",
                    alias=FhirList(["first name", "middle name", "middle initial"]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".prefix"),
                    path=A.concat(resource, ".name.prefix"),
                    label=A.text(label),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".suffix"),
                    path=A.concat(resource, ".name.suffix"),
                    label=A.text(label),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".period"),
                    path=A.concat(resource, ".name.period"),
                    label=A.text(label),
                ),
            ],
            True,
        )

        return element_list
