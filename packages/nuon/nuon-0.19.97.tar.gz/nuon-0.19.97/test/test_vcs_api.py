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

from nuon.api.vcs_api import VcsApi


class TestVcsApi(unittest.TestCase):
    """VcsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = VcsApi()

    def tearDown(self) -> None:
        pass

    def test_create_vcs_connection(self) -> None:
        """Test case for create_vcs_connection

        create a vcs connection for Github
        """
        pass

    def test_create_vcs_connection_callback(self) -> None:
        """Test case for create_vcs_connection_callback

        public connection to create a vcs connection via a callback
        """
        pass

    def test_get_all_vcs_connected_repos(self) -> None:
        """Test case for get_all_vcs_connected_repos

        get all vcs connected repos for an org
        """
        pass

    def test_get_org_vcs_connections(self) -> None:
        """Test case for get_org_vcs_connections

        get vcs connection for an org
        """
        pass

    def test_get_vcs_connection(self) -> None:
        """Test case for get_vcs_connection

        returns a vcs connection for an org
        """
        pass


if __name__ == '__main__':
    unittest.main()
