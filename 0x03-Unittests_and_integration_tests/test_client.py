#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and configure payload returns."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Mocked response objects for .json()
        mock_org_resp = MagicMock()
        mock_org_resp.json.return_value = cls.org_payload

        mock_repos_resp = MagicMock()
        mock_repos_resp.json.return_value = cls.repos_payload

        # side_effect to return fixture payload based on URL
        def get_side_effect(url):
            if url.endswith("/orgs/google"):
                return mock_org_resp
            if url.endswith("/orgs/google/repos"):
                return mock_repos_resp
            return MagicMock(json=lambda: {})

        mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license using integration fixtures."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )


if __name__ == "__main__":
    unittest.main()
