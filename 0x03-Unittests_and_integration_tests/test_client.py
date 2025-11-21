#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value.

        get_json is patched and not executed.
        """
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org()

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url return
        the correct URL based on org payload."""
        org_payload = {"repos_url":
                       "https://api.github.com/orgs/test_org/repos"}
        client = GithubOrgClient("test_org")

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = org_payload

            result = client._public_repos_url
            self.assertEqual(result, org_payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repo names.

        get_json is patched and returns a fake payload.
        _public_repos_url property is patched as a context manager.
        """
        # Mocked repos payload returned by get_json
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload

        client = GithubOrgClient("test_org")

        # Patch _public_repos_url property to return any URL
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://fakeurl.com/repos"

            result = client.public_repos()
            expected = ["repo1", "repo2"]

            self.assertEqual(result, expected)

            # Ensure both mocks were called once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://fakeurl.com/repos")


if __name__ == "__main__":
    unittest.main()
