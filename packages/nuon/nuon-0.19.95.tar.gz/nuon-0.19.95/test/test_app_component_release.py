# coding: utf-8

"""
    Nuon

    API for managing nuon apps, components, and installs.

    The version of the OpenAPI document: 0.19.15
    Contact: support@nuon.co
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from nuon.models.app_component_release import AppComponentRelease

class TestAppComponentRelease(unittest.TestCase):
    """AppComponentRelease unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AppComponentRelease:
        """Test AppComponentRelease
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AppComponentRelease`
        """
        model = AppComponentRelease()
        if include_optional:
            return AppComponentRelease(
                build_id = '',
                created_at = '',
                created_by_id = '',
                id = '',
                release_steps = [
                    nuon.models.app/component_release_step.app.ComponentReleaseStep(
                        component_release_id = '', 
                        created_at = '', 
                        created_by_id = '', 
                        delay = '', 
                        id = '', 
                        install_deploys = [
                            nuon.models.app/install_deploy.app.InstallDeploy(
                                build_id = '', 
                                component_id = '', 
                                component_name = '', 
                                created_at = '', 
                                created_by_id = '', 
                                id = '', 
                                install_component_id = '', 
                                install_deploy_type = 'release', 
                                install_id = '', 
                                release_id = '', 
                                status = '', 
                                status_description = '', 
                                updated_at = '', )
                            ], 
                        requested_install_ids = [
                            ''
                            ], 
                        status = '', 
                        status_description = '', 
                        updated_at = '', )
                    ],
                status = '',
                status_description = '',
                total_release_steps = 56,
                updated_at = ''
            )
        else:
            return AppComponentRelease(
        )
        """

    def testAppComponentRelease(self):
        """Test AppComponentRelease"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
