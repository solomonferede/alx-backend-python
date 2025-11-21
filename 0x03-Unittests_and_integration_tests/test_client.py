#!/usr/bin/env python3
"""Unit tests for client module."""
from unittest.mock import patch, PropertyMock
import unittest
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL from org payload."""

        fake_org_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        client = GithubOrgClient("google")

        # Patch org property using PropertyMock
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_org_payload

            # Access property
            result = client._public_repos_url

            # Assert correct repos_url returned
            self.assertEqual(result, fake_org_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
