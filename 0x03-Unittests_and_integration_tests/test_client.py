#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct JSON
        payload and calls get_json once."""

        # Set a fake return value for get_json
        fake_payload = {"login": org_name, "repos_url":
                        f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = fake_payload

        # Create client instance
        client = GithubOrgClient(org_name)

        # Call .org (memoized method)
        result = client.org

        # Check return value
        self.assertEqual(result, fake_payload)

        # Check get_json was called once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
