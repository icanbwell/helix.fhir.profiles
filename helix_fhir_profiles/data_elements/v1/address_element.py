from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.address import Address
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.address_type import AddressTypeCodeValues
from spark_auto_mapper_fhir.value_sets.address_use import AddressUseCodeValues
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
)


class DataElementAddress:
    @staticmethod
    def get_address_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "address"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".address"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by types", rules=SlicingRulesCodeValues.Open
                    ),
                    short="An address expressed using postal conventions",
                    definition="A physical or postal address",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Address")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-id"),
                    path=A.concat(resource, ".address.id"),
                    label=label,
                    short="pattern: use - type - 'current'/period-end in MMDDYYYY format",
                    definition="A unique identifier for the element within a given resource",
                    comment="incoming addresses are presumed current unless otherwise specified",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="id example of a current address",
                                valueString="home-both-current",
                            ),
                            ElementDefinitionExample(
                                label="id example of a previous address",
                                valueString="home-old-2022",
                            ),
                        ]
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-use"),
                    path=A.concat(resource, ".address.use"),
                    label=label,
                    short="home | work | temp | billing",
                    definition="The purpose of the address",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-type"),
                    path=A.concat(resource, ".address.type"),
                    label=label,
                    short="postal | physical | both (presumed both if absent)",
                    definition="The type of an address (physical/postal)",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-text"),
                    path=A.concat(resource, ".address.text"),
                    label=label,
                    short="Text representation of the address",
                    definition="Specifies the entire address as it should be displayed e.g. on a postal label",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-line"),
                    path=A.concat(resource, ".address.line"),
                    label=label,
                    short="Street name, number, direction & P.O. Box etc",
                    # definition="",
                    comment="addresses are subjected to a standardization process that may alter these values",
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-city"),
                    path=A.concat(resource, ".address.city"),
                    label=label,
                    short="City name",
                    # definition="",
                    comment="addresses are subjected to a standardization process that may alter these values",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-district"),
                    path=A.concat(resource, ".address.district"),
                    label=label,
                    short="District name (aka county)",
                    # definition="",
                    comment="addresses are subjected to a standardization process that may alter these values",
                    alias=FhirList(["county"]),
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-state"),
                    path=A.concat(resource, ".address.state"),
                    label=label,
                    short="two-digit state code preferred",
                    # definition="",
                    comment="addresses are subjected to a standardization process that may alter these values",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-postalCode"),
                    path=A.concat(resource, ".address.postalCode"),
                    label=label,
                    short="zip code",
                    # definition="",
                    comment="addresses are subjected to a standardization process that may alter these values",
                    requirements="no current structure preference",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-country"),
                    path=A.concat(resource, ".address.country"),
                    label=label,
                    comment="addresses are subjected to a standardization process that may alter these values",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-period"),
                    path=A.concat(resource, ".address.period"),
                    label=label,
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Period")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_personal_address(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "personal-address"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-address-", label),
                    path=A.concat(resource, ".address"),
                    sliceName=label,
                    label=label,
                    short="An area where services are rendered",
                    definition="Represents a state or zip code where services are provided",
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                # code=ProductFeatureCodeValues.,
                            ),
                        ]
                    ),
                    # comment="",
                    requirements="two-digit state value and/or a 5-digit zip code",
                    type_=FhirList([ElementDefinitionType(code="Address")]),
                    patternAddress=Address(id_="coverage-area"),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="a Texas zip code",
                                valueAddress=Address(
                                    id_="coverage-area", state="TX", postalCode="78704"
                                ),
                            ),
                            ElementDefinitionExample(
                                label="the state of Maryland",
                                valueAddress=Address(id_="coverage-area", state="MD"),
                            ),
                        ]
                    ),
                )
            ]
        )
        return elements

    @staticmethod
    def get_coverage_area(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "coverage-area"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-address-", label),
                    path=A.concat(resource, ".address"),
                    sliceName=label,
                    label=label,
                    short="An area where services are rendered",
                    definition="Represents a state or zip code where services are provided",
                    # comment="",
                    requirements="two-digit state value and/or a 5-digit zip code",
                    type_=FhirList([ElementDefinitionType(code="Address")]),
                    patternAddress=Address(
                        id_="coverage-area", type_=AddressTypeCodeValues.Physical
                    ),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="a Texas zip code",
                                valueAddress=Address(
                                    id_="tx-coverage-area",
                                    type_=AddressTypeCodeValues.Physical,
                                    state="TX",
                                    postalCode="78704",
                                ),
                            ),
                            ElementDefinitionExample(
                                label="the state of Maryland",
                                valueAddress=Address(
                                    id_="md-coverage-area",
                                    type_=AddressTypeCodeValues.Physical,
                                    state="MD",
                                ),
                            ),
                        ]
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_business_address(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "business-address"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-address-", label),
                    path=A.concat(resource, ".address"),
                    sliceName=label,
                    label=label,
                    short="Physical location",
                    definition="Physical address of the location",
                    comment="Helix pipelines uses a service to standardize these fields",
                    type_=FhirList([ElementDefinitionType(code="Address")]),
                    min=0,
                    max="1",
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="work address",
                                valueAddress=Address(
                                    id_="work-both-current",
                                    use=AddressUseCodeValues.Work,
                                    type_=AddressTypeCodeValues.Postal_Physical,
                                    line=FhirList(["123 Main St", "STE 5"]),
                                    city="Austin",
                                    state="TX",
                                    postalCode="78701",
                                ),
                            )
                        ]
                    ),
                )
            ]
        )

        return elements
