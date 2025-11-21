#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the static method has_license with
        different repo and license_key inputs."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get before any tests run."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Function to return the correct fixture based on URL
        def get_side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url.endswith("/orgs/test_org"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/repos"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get after all tests run."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos using fixture data."""
        client = GithubOrgClient("test_org")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with a license filter."""
        client = GithubOrgClient("test_org")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
