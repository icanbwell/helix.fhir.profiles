from typing import Dict, Any, List

from library.fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
)

from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding

from library.fhir_profiles.data_elements.v1.address_element import (
    DataElementAddress,
)
from library.fhir_profiles.backbone_elements.v1.backbone_element_hours_of_operation import (
    DataBackboneElementHoursOfOperation,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.location_mode import LocationModeCodeValues

from library.fhir_profiles.data_elements.v1.contact_point_element import (
    DataElementContactPoint,
)
from library.fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from library.fhir_profiles.data_elements.v1.location_type_element import (
    DataElementLocationType,
)
from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileHealthcareLocation:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-healthcare-location")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileHealthcareLocation.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Location")

    mapper = AutoMapper(
        view=parameters["view_healthcare_location"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileHealthcareLocation.get_profile_id()),
            profile_name="Healthcare Location",
            computer_friendly_profile_name="HealthcareLocation",
            fhir_resource_type=resource,
            description=A.text("Location where healthcare services are rendered"),
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ProviderRoster,
                    )
                ]
            ),
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=resource, path=resource),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"), path=A.concat(resource, ".id")
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource))
            # EXTENSIONS
            .concat(DataElementExtension.get_extension_any(resource=resource))
            .concat(DataElementExtension.get_location_parking(resource=resource))
            .concat(DataElementExtension.get_location_image(resource=resource))
            # IDENTIFIER
            .concat(
                DataElementIdentifier.get_identifier_any(resource=resource),
            )
            .concat(DataElementIdentifier.get_npi(resource=resource))
            .concat(DataElementIdentifier.get_facility_id(resource=resource))
            .concat(
                FhirList(
                    [
                        # STATUS
                        ElementDefinition(
                            id_="Location.status",
                            path="Location.status",
                            # label="",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="active | inactive",
                            definition="Default to active when missing or unknown",
                            min=1,
                            mustSupport=A.boolean(True),
                            # binding=ElementDefinitionBinding(
                            #     strength=BindingStrengthCodeValues.Extensible,
                            #     description="Indicates whether the location is still in use.",
                            #     valueSet=LocationStatusCode.codeset,
                            # ),
                        ),
                        # NAME
                        ElementDefinition(
                            id_="Location.name",
                            path="Location.name",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="name of the facility",
                            definition="Name of the location as used by humans. Does not need to be unique.",
                            comment="typically the same as the organization name",
                            alias=FhirList(["practice name"]),
                            min=1,
                            max="1",
                            mustSupport=A.boolean(True),
                        ),
                        # ALIAS
                        ElementDefinition(
                            id_="Location.alias",
                            path="Location.alias",
                            label="other_name",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="other names for the location",
                            definition="A list of alternate names that the location is known as, or was known as, in the past.",
                            comment="If more than one name is relevant, list the alternatives here",
                            min=0,
                            max="*",
                            mustSupport=A.boolean(True),
                        ),
                        # DESCRIPTION
                        ElementDefinition(
                            id_="Location.description",
                            path="Location.description",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="description of the location",
                            definition="Description of the Location, which helps patients in finding or referencing the place.",
                            # comment="",
                            min=0,
                            max="1",
                            mustSupport=A.boolean(True),
                        ),
                        # MODE
                        ElementDefinition(
                            id_="Location.mode",
                            path="Location.mode",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="Fixed value 'instance'",
                            definition="Indicates the resourcce represents a specific location.",
                            comment="If the record is for a physical location, use instance",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="code")]),
                            fixedCode=LocationModeCodeValues.Instance,
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            )
            .concat(
                # TYPES
                DataElementLocationType.get_location_type_any(resource=resource)
            )
            .concat(DataElementLocationType.get_location_specialty(resource=resource))
            .concat(DataElementLocationType.get_covid_vaccine(resource=resource))
            .concat(DataElementLocationType.get_covid_testing(resource=resource))
            .concat(DataElementLocationType.get_emergency_room(resource=resource))
            # TELECOM
            .concat(DataElementContactPoint.get_contact_point_any(resource=resource))
            .concat(DataElementContactPoint.get_business_phone(resource=resource))
            .concat(
                DataElementContactPoint.get_business_fax(resource=resource),
            )
            # ADDRESS
            .concat(DataElementAddress.get_business_address(resource=resource))
            .concat(
                FhirList(
                    [
                        # PHYSICAL TYPE
                        ElementDefinition(
                            id_="Location.physicalType",
                            path="Location.physicalType",
                            sliceName="physicalType",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="Physical form of the location",
                            definition="Physical form of the location, e.g. building, room, vehicle, road.",
                            min=0,
                            max="1",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            mustSupport=A.boolean(True),
                            # patternCodeableConcept=
                            # binding=ElementDefinitionBinding(
                            #     strength=BindingStrengthCodeValues.Extensible,
                            #     description="Physical form of the location",
                            #     valueSet=LocationTypeCode.codeset,
                            # ),
                        ),
                        # POSITION
                        ElementDefinition(
                            id_="Location.position",
                            path="Location.position",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="The absolute geographic location",
                            definition="Longitude and latitude values of the physical location",
                            # comment="",
                            requirements="Required to calculate distance for Finding Care",
                            min=1,
                            max="1",
                            type_=FhirList(
                                [ElementDefinitionType(code="BackboneElement")]
                            ),
                            # example=,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_="Location.position.longitude",
                            path="Location.position.longitude",
                            short="Longitude with WGS84 datum",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="decimal")]),
                        ),
                        ElementDefinition(
                            id_="Location.position.latitude",
                            path="Location.position.latitude",
                            short="Latitude with WGS84 datum",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="decimal")]),
                        ),
                        # managing organization
                        ElementDefinition(
                            id_="Location.managingOrganization",
                            path="Location.managingOrganization",
                            sliceName="managingOrganization",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="Healthcare Organization that manages the location / facility",
                            definition="The organization responsible for the provisioning and upkeep of the location.",
                            min=0,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfileHealthcareOrganization.get_profile_url()
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            )
            .concat(
                # hours of operation
                DataBackboneElementHoursOfOperation.get_element_definition(
                    resource=resource
                ),
            ),
        )
    )

    return [mapper]
