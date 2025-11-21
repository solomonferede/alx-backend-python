#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch
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
        # Setup the mock to return a fake payload
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Instantiate the client
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org()

        # Check that the returned value is the mocked payload
        self.assertEqual(result, expected_payload)

        # Ensure get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
