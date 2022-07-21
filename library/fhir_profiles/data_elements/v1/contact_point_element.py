from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.complex_types.contact_point import ContactPoint
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.contact_point_system import (
    ContactPointSystemCodeValues,
)
from spark_auto_mapper_fhir.value_sets.contact_point_use import (
    ContactPointUseCodeValues,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataElementContactPoint:
    @staticmethod
    def get_contact_point_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "contact-point"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".telecom"),
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            ),
                        ]
                    ),
                    slicing=ElementDefinitionSlicing(
                        description="slice by types", rules=SlicingRulesCodeValues.Open
                    ),
                    short="Details of a technology-based contact point",
                    definition="phone, fax, etc",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="ContactPoint")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".id"),
                    path=A.concat(resource, ".telecom.id"),
                    label=label,
                    short="set to use and type code(s)",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".system"),
                    path=A.concat(resource, ".telecom.system"),
                    label=label,
                    short="phone | fax | email | pager | url | sms | other",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".value"),
                    path=A.concat(resource, ".telecom.value"),
                    label=label,
                    short="The value of the contact point",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".use"),
                    path=A.concat(resource, ".telecom.use"),
                    label=label,
                    short="home | work | temp | old | mobile - purpose of this contact point",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_business_phone(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "business-phone"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".telecom"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Contact phone number for the business",
                    type_=FhirList([ElementDefinitionType(code="ContactPoint")]),
                    patternContactPoint=ContactPoint(
                        id_="business-phone",
                        system=ContactPointSystemCodeValues.Phone,
                        use=ContactPointUseCodeValues.Work,
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_business_fax(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "business-fax"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".telecom"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Contact fax number for the business",
                    type_=FhirList([ElementDefinitionType(code="ContactPoint")]),
                    patternContactPoint=ContactPoint(
                        id_="business-fax",
                        system=ContactPointSystemCodeValues.Fax,
                        use=ContactPointUseCodeValues.Work,
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_business_email(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "business-email"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".telecom"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Contact email address for the individual",
                    type_=FhirList([ElementDefinitionType(code="ContactPoint")]),
                    patternContactPoint=ContactPoint(
                        id_="business-email",
                        system=ContactPointSystemCodeValues.Email,
                        use=ContactPointUseCodeValues.Work,
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_personal_phone(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "personal-phone"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".telecom"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Contact phone number for the individiaul",
                    type_=FhirList([ElementDefinitionType(code="ContactPoint")]),
                    patternContactPoint=ContactPoint(
                        id_="personal-phone",
                        system=ContactPointSystemCodeValues.Phone,
                        use=ContactPointUseCodeValues.Work,
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_personal_email(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "personal-email"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".telecom"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Contact email address for the individual",
                    type_=FhirList([ElementDefinitionType(code="ContactPoint")]),
                    patternContactPoint=ContactPoint(
                        id_="personal-email",
                        system=ContactPointSystemCodeValues.Email,
                        use=ContactPointUseCodeValues.Work,
                    ),
                )
            ]
        )

        return elements
