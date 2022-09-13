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
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.claim_information_category_codes import (
    ClaimInformationCategoryCodesCode,
    ClaimInformationCategoryCodesCodeValues,
)
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataBackboneElementSupportingInfo:
    @staticmethod
    def get_supporting_info_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "supporting-info"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    # comment="",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".supportingInfo.id"),
                    label=label,
                    short="set to category code",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.sequence"),
                    label=label,
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Extensible,
                    #     valueSet="https://www.hl7.org/fhir/us/bwell/bwell-vs-claim-information-category",  # todo update
                    # ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".value[x]"),
                    path=A.concat(resource, ".supportingInfo.value[x]"),
                    label=label,
                    min=1,
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_days_supply(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "days-supply"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="quantity of supply",
                    # comment="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    # system=
                                    code=GenericTypeCode("dayssupply")
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".valueQuantity"),
                    path=A.concat(resource, ".supportingInfo.valueQuantity"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="Quantity")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_dispense_as_written(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "daw"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="dispense as written",
                    definition="Dispense as written description",
                    # comment="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    # system=
                                    code=GenericTypeCode("dawcode")
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".valueCodeableConcept"),
                    path=A.concat(resource, ".supportingInfo.valueCodeableConcept"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="https://bluebutton.cms.gov/resources/variables/daw_prod_slctn_cd"
                                )
                            ]
                        )
                    ),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_generic_brand(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "generic-brand"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    # system=
                                    code=GenericTypeCode("brandgeneric")
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".valueString"),
                    path=A.concat(resource, ".supportingInfo.valueString"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_refill_number(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "refill-number"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Refill number",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    # system=
                                    code=GenericTypeCode("refillnum")
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".valueQuantity"),
                    path=A.concat(resource, ".supportingInfo.valueQuantity"),
                    label=label,
                    short="Fill number quantity",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="Quantity")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_prescribed_date(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "prescribed-date"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    # comment="",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    # system=
                                    code=GenericTypeCode("prescribeddate")
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".timing[x]"),
                    path=A.concat(resource, ".supportingInfo.timing[x]"),
                    label=label,
                    short="timing date",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="date")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_type_of_bill(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "type-of-bill"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="claim type",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 1",
                    fixedInteger=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("type-of-bill"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".valueString"),
                    path=A.concat(resource, ".supportingInfo.valueString"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_discharge_status(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "discharge-status"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Discharge status",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 2",
                    fixedInteger=2,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("discharge-status"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Discharge,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="http://www.nubc.org/patient-discharge",  # todo
                    # ),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_admission_source(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "admission-source"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Admission source",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 3",
                    fixedInteger=3,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("admsrc"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="https://www.nubc.org/point-of-origin-for-admission-or-visit",  # todo update?
                    # ),
                ),
            ],
            True,
        )

        return elements

    # admission type
    @staticmethod
    def get_admission_type(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "admission-type"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Admission type",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 4",
                    fixedInteger=4,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("admtype"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="http://www.nubc.org/priority-type-of-admission-or-visit",  # todo update?
                    # ),
                ),
            ],
            True,
        )

        return elements

    # type of facility
    @staticmethod
    def get_type_of_facility(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "type-of-facilty"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Type of facility",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 5",
                    fixedInteger=5,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("tob-typeoffacility"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    short="bill type",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="https://www.cms.gov/Medicare/CMS-Forms/CMS-Forms/CMS-Forms-Items/CMS1196256.html",  # todo update?
                    # ),
                ),
            ],
            True,
        )

        return elements

    # bill classification
    @staticmethod
    def get_bill_classification(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "bill-classification"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Bill classification",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 6",
                    fixedInteger=6,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("tob-billclassification"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="https://www.cms.gov/Medicare/CMS-Forms/CMS-Forms/CMS-Forms-Items/CMS1196256.html",  # todo update?
                    # ),
                ),
            ],
            True,
        )

        return elements

    # frequency
    @staticmethod
    def get_frequency(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "frequency"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Frequency code",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 7",
                    fixedInteger=7,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("tob-frequency"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="https://www.cms.gov/Medicare/CMS-Forms/CMS-Forms/CMS-Forms-Items/CMS1196256.html",  # todo update?
                    # ),
                ),
            ],
            True,
        )

        return elements

    # place-of-service
    @staticmethod
    def get_place_of_service(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "place-of-service"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Place of service",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    short="Fixed: 8",
                    fixedInteger=8,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("placeofservice"),
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".code"),
                    path=A.concat(resource, ".supportingInfo.code"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     valueSet="https://www.cms.gov/Medicare/CMS-Forms/CMS-Forms/CMS-Forms-Items/CMS1196256.html",  # todo update?
                    # ),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_received_date(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "received-date"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".supportingInfo"),
                    sliceName=label,
                    label=label,
                    short="Claim received date",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".supportingInfo.category"),
                    label=label,
                    min=1,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    # system="http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBSupportingInfoType",
                                    code=GenericTypeCode("claimreceiveddate")
                                ),
                                Coding(
                                    system=ClaimInformationCategoryCodesCode.codeset,
                                    code=ClaimInformationCategoryCodesCodeValues.Information,
                                ),
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".timingDate"),
                    path=A.concat(resource, ".supportingInfo.timing[x]"),
                    label=label,
                    short="date value of when the claim was received",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="date")]),
                ),
            ],
            True,
        )

        return elements
