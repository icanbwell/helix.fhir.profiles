from typing import Dict, Any, List

# from library.fhir_profile_definitions.v1.data_element_definitions.extension_element import DataElementExtension
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding

from helix_fhir_profiles.data_elements.v1.address_element import (
    DataElementAddress,
)
from helix_fhir_profiles.data_elements.v1.contact_point_element import (
    DataElementContactPoint,
)
from helix_fhir_profiles.data_elements.v1.human_name_element import (
    DataElementHumanName,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.structure_definition_mappings.extensions.v1.extension_contact_related_patient_mapping import (
    ExtensionContactRelatedPatient,
)
from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfilePatient:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-patient")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfilePatient.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Patient")

    mapper = AutoMapper(
        view=parameters["view_patient"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfilePatient.get_profile_id()),
            profile_name=A.text("Patient"),
            computer_friendly_profile_name=A.text("Patient"),
            fhir_resource_type=resource,
            description=A.text(
                "Includes but is not limited to: \n \n * Receiver of healthcare services \n \n * Beneficiary of an insurance plan \n \n * bWell app user \n \n * Employee"
            ),
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ElibilityFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.EmployeeFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.RxClaimsFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.MedicalClaimsFile,
                    ),
                ]
            ),
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=resource, path=resource),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"),
                        path=A.concat(resource, ".id"),
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource))
            # EXTENSIONS
            # .concat(DataElementExtension.get_extension_any(resource=resource)).concat(
            #     DataElementExtension.get_contact_related_patient(resource=resource)
            # )
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_member_number(resource=resource))
            .concat(DataElementIdentifier.get_employee_id(resource=resource))
            .concat(DataElementIdentifier.get_ssn(resource=resource))
            .concat(
                FhirList(
                    [
                        # ACTIVE
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            short="resource active flag",
                            definition="indication of whether the resource is still in use",
                            comment="default to true",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            )
            .concat(
                # NAME
                DataElementHumanName.get_human_name_any(resource=resource)
            )
            # TELECOMs
            .concat(
                DataElementContactPoint.get_contact_point_any(resource=resource),
            )
            .concat(DataElementContactPoint.get_personal_phone(resource=resource))
            .concat(DataElementContactPoint.get_personal_email(resource=resource))
            .concat(DataElementContactPoint.get_business_phone(resource=resource))
            .concat(DataElementContactPoint.get_business_email(resource=resource))
            .concat(
                FhirList(
                    [
                        # GENDER
                        ElementDefinition(
                            id_=A.concat(resource, ".gender"),
                            path=A.concat(resource, ".gender"),
                            short="male | female | unknown",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.Person,
                                    ),
                                ]
                            ),
                            alias=FhirList(["sex"]),
                            mustSupport=A.boolean(False),
                        ),
                        # BIRTHDATE
                        ElementDefinition(
                            id_=A.concat(resource, ".birthDate"),
                            path=A.concat(resource, ".birthDate"),
                            short="the individual's date of birth",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.Person,
                                    ),
                                ]
                            ),
                            type_=FhirList([ElementDefinitionType(code="date")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            )
            .concat(
                # ADDRESS
                DataElementAddress.get_address_any(resource=resource),
            )
            .concat(
                FhirList(
                    [
                        # CONTACT
                        # todo make element definition
                        ElementDefinition(
                            id_="de-related-contact",
                            path=A.concat(resource, ".contact"),
                            short="family contact(s)",
                            definition="Other individuals related to this patient",
                            comment="insurance plan subscribers with dependents should have dependents listed, and vice versa",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        # code=ProductFeatureCodeValues.,
                                    )
                                ]
                            ),
                            alias=FhirList(
                                ["health-circle", "dependent", "subscriber"]
                            ),
                            min=0,
                            max="*",
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".contact.id"),
                            path=A.concat(resource, ".contact.id"),
                            short="referenced id",
                            min=1,
                            max="1",
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".contact.extension"),
                            path=A.concat(resource, ".contact.extension"),
                            sliceName="related-contact",
                            label="related-contact",
                            short="Extension to reference another Patient resource",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Extension",
                                        profile=FhirList(
                                            [
                                                ExtensionContactRelatedPatient.get_profile_url()
                                            ]
                                        ),
                                    )
                                ]
                            ),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".contact.relationship"),
                            path=A.concat(resource, ".contact.relationship"),
                            short="relationship code",
                            definition="Dependent Code (SUB,SPS,CHD,UNK)",
                        ),
                        # COMMUNICATION
                        # todo make element definition
                        ElementDefinition(
                            id_=A.concat(resource, ".communication"),
                            path=A.concat(resource, ".communication"),
                            min=0,
                            max="*",
                            type_=FhirList(
                                [ElementDefinitionType(code="BackboneElement")]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".communication.id"),
                            path=A.concat(resource, ".communication.id"),
                            short="language code",
                            min=1,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".communication.language"),
                            path=A.concat(resource, ".communication.language"),
                            min=1,
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                        ),
                    ]
                )
            ),
        ),
    )

    return [mapper]
