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

from nuon.models.service_cli_config import ServiceCLIConfig

class TestServiceCLIConfig(unittest.TestCase):
    """ServiceCLIConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ServiceCLIConfig:
        """Test ServiceCLIConfig
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ServiceCLIConfig`
        """
        model = ServiceCLIConfig()
        if include_optional:
            return ServiceCLIConfig(
                auth_audience = '',
                auth_client_id = '',
                auth_domain = ''
            )
        else:
            return ServiceCLIConfig(
        )
        """

    def testServiceCLIConfig(self):
        """Test ServiceCLIConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
