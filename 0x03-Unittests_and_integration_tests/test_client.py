#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload"""

        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org   # memoized property

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns URL from org"""

        fake_org_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        client = GithubOrgClient("google")

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_org_payload

            result = client._public_repos_url
            self.assertEqual(result, fake_org_payload["repos_url"])


    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""

        # Fake repo payload returned by get_json
        fake_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        mock_get_json.return_value = fake_repos

        # Fake URL returned by _public_repos_url property
        fake_url = "https://api.github.com/orgs/google/repos"

        client = GithubOrgClient("google")

        # Patch the _public_repos_url property
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value=fake_url
        ) as mock_repos_url:

            repos = client.public_repos()

            # Check correct repo list
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Ensure _public_repos_url property called once
            mock_repos_url.assert_called_once()

        # Ensure get_json was called once with the fake URL
        mock_get_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    unittest.main()
