# To run the tests you must first start the service locally in test mode.
# cargo run -p feature -- --test-mode
# That loads in the test user so the tests can run.

import pytest
from pytest_unordered import unordered  # type: ignore

import requests
from unittest import mock

from typing import List
import sys


sys.path.insert(0, "./src/")

from oso_cloud import Oso
from oso_cloud.oso import Value, Fact


# These are integration tests and they will only work if you have started the
# server with a test user.
# cargo run -- --test-mode
class TestAnything:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.user1: Value = {"type": "User", "id": "1"}
        self.repo2: Value = {"type": "Repo", "id": "2"}
        self.repo3: Value = {"type": "Repo", "id": "3"}
        self.more_facts: List[Fact] = [
            {"name": "has_role", "args": [self.user1, "member", self.repo2]},
            {"name": "has_relation", "args": [self.repo2, "parent", self.repo3]},
        ]

    def teardown(self) -> None:
        self.oso.bulk_delete(self.more_facts)
        self.oso.delete(
            {"name": "has_role", "args": [self.user1, "member", self.repo2]}
        )
        self.oso.delete(
            {"name": "has_relation", "args": [self.repo2, "parent", self.repo3]}
        )

    def test_anything(self) -> None:
        self.oso.policy(
            """
            actor User {
            }

            resource Repo {
                roles = ["member"];
                permissions = ["read"];
                relations = { parent: Repo };
                "read" if "member";
                "read" if "read" on "parent";
            }
        """
        )

        assert not self.oso.authorize(self.user1, "read", self.repo2)

        assert self.oso.list(self.user1, "read", "Repo") == []

        assert self.oso.actions(self.user1, self.repo2) == []

        self.oso.tell(
            {"name": "has_relation", "args": [self.repo2, "parent", self.repo3]}
        )
        self.oso.delete(
            {"name": "has_relation", "args": [self.repo2, "parent", self.repo3]}
        )

        self.oso.tell({"name": "has_role", "args": [self.user1, "member", self.repo2]})
        assert self.oso.get(
            {"name": "has_role", "args": [self.user1, "member", self.repo2]}
        ) == [
            {
                "name": "has_role",
                "args": [
                    {"type": "User", "id": "1"},
                    {"type": "String", "id": "member"},
                    {"type": "Repo", "id": "2"},
                ],
            },
        ]
        assert self.oso.authorize(self.user1, "read", self.repo2)
        assert self.oso.list(self.user1, "read", "Repo") == ["2"]
        assert self.oso.actions(self.user1, self.repo2) == ["read"]
        self.oso.delete(
            {"name": "has_role", "args": [self.user1, "member", self.repo2]}
        )

        self.oso.bulk_tell(self.more_facts)
        assert self.oso.get(
            {"name": "has_role", "args": [self.user1, "member", self.repo2]}
        ) == [
            {
                "name": "has_role",
                "args": [
                    {"type": "User", "id": "1"},
                    {"type": "String", "id": "member"},
                    {"type": "Repo", "id": "2"},
                ],
            },
        ]
        assert self.oso.get(
            {"name": "has_relation", "args": [self.repo2, "parent", self.repo3]}
        ) == [
            {
                "name": "has_relation",
                "args": [
                    {"type": "Repo", "id": "2"},
                    {"type": "String", "id": "parent"},
                    {"type": "Repo", "id": "3"},
                ],
            },
        ]

        self.oso.bulk_delete(self.more_facts)
        assert (
            self.oso.get(
                {"name": "has_role", "args": [self.user1, "member", self.repo2]}
            )
            == []
        )
        assert (
            self.oso.get(
                {"name": "has_relation", "args": [self.repo2, "parent", self.repo3]}
            )
            == []
        )

        self.oso.bulk(tell=self.more_facts)
        assert self.oso.get({"name": "has_role", "args": [None, None, None]}) == [
            {
                "name": "has_role",
                "args": [
                    {"type": "User", "id": "1"},
                    {"type": "String", "id": "member"},
                    {"type": "Repo", "id": "2"},
                ],
            }
        ]
        self.oso.bulk(
            delete=[{"name": "has_role", "args": [self.user1, None, None]}],
            tell=[{"name": "has_role", "args": [self.user1, "member", self.repo3]}],
        )
        assert self.oso.get({"name": "has_role", "args": [None, None, None]}) == [
            {
                "name": "has_role",
                "args": [
                    {"type": "User", "id": "1"},
                    {"type": "String", "id": "member"},
                    {"type": "Repo", "id": "3"},
                ],
            }
        ]
        self.oso.bulk(delete=[{"name": "has_role", "args": [self.user1, None, None]}])
        assert self.oso.get({"name": "has_role", "args": [None, None, None]}) == []


class TestAuthorizeResources:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User {
            }

            resource Repo {
                roles = ["member"];
                permissions = ["read"];
                relations = { parent: Repo };
                "read" if "member";
            }
        """
        )
        self.bob: Value = {"type": "User", "id": "bob"}
        self.acme: Value = {"type": "Repo", "id": "acme"}
        self.anvil: Value = {"type": "Repo", "id": "anvil"}
        self.coyote: Value = {"type": "Repo", "id": "coyote"}
        self.oso.tell({"name": "has_role", "args": [self.bob, "member", self.acme]})
        self.oso.tell({"name": "has_role", "args": [self.bob, "member", self.coyote]})

    def teardown(self) -> None:
        self.oso.delete({"name": "has_role", "args": [self.bob, "member", self.acme]})
        self.oso.delete({"name": "has_role", "args": [self.bob, "member", self.coyote]})

    def test_authorize_resouces_empty(self) -> None:
        assert self.oso.authorize_resources(self.bob, "read", []) == []
        assert self.oso.authorize_resources(self.bob, "read", None) == []

    def test_authorize_resouces_match_all(self) -> None:
        assert self.oso.authorize_resources(
            self.bob, "read", [self.acme, self.coyote]
        ) == unordered([self.acme, self.coyote])

    def test_authorize_resources_match_some(self) -> None:
        assert self.oso.authorize_resources(
            self.bob, "read", [self.acme, self.anvil]
        ) == unordered([self.acme])

    def test_authorize_resources_match_none(self) -> None:
        assert self.oso.authorize_resources(self.bob, "read", [self.anvil]) == []


class TestContextFacts:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User {
            }

            resource Repo {
                roles = ["member"];
                permissions = ["read"];
                "read" if "member";
            }
        """
        )
        self.alice: Value = {"type": "User", "id": "alice"}
        self.bob: Value = {"type": "User", "id": "bob"}
        self.acme: Value = {"type": "Repo", "id": "acme"}
        self.anvil: Value = {"type": "Repo", "id": "anvil"}

    def test_context_facts(self) -> None:
        # authorize
        assert not self.oso.authorize(self.alice, "read", self.acme)
        assert self.oso.authorize(
            self.alice,
            "read",
            self.acme,
            [{"name": "has_role", "args": [self.alice, "member", self.acme]}],
        )
        # authorize_resources
        assert self.oso.authorize_resources(
            self.alice,
            "read",
            [self.acme, self.anvil],
            [{"name": "has_role", "args": [self.alice, "member", self.acme]}],
        ) == unordered([self.acme])
        assert self.oso.authorize_resources(
            self.alice,
            "read",
            [self.acme, self.anvil],
            [{"name": "has_role", "args": [self.alice, "member", self.anvil]}],
        ) == unordered([self.anvil])

        # list
        assert self.oso.list(
            self.alice,
            "read",
            "Repo",
            [{"name": "has_role", "args": [self.alice, "member", self.acme]}],
        ) == unordered(["acme"])
        assert self.oso.list(
            self.alice,
            "read",
            "Repo",
            [{"name": "has_role", "args": [self.alice, "member", self.anvil]}],
        ) == unordered(["anvil"])

        # actions
        assert self.oso.actions(
            self.alice,
            self.acme,
        ) == unordered([])
        assert self.oso.actions(
            self.alice,
            self.acme,
            [{"name": "has_role", "args": [self.alice, "member", self.anvil]}],
        ) == unordered([])
        assert self.oso.actions(
            self.alice,
            self.acme,
            [{"name": "has_role", "args": [self.alice, "member", self.acme]}],
        ) == unordered(["read"])


class TestQuery:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User {}
            resource Computer {}

            hello(friend) if
                is_friendly(friend);

            something_else(friend, other_friend, _anybody) if
                is_friendly(friend) and is_friendly(other_friend);

        """
        )
        self.sam: Value = {"type": "User", "id": "sam"}
        self.gabe: Value = {"type": "User", "id": "gabe"}
        self.steve: Value = {"type": "Computer", "id": "steve"}
        self.oso.tell({"name": "is_friendly", "args": [self.sam]})
        self.oso.tell({"name": "is_friendly", "args": [self.gabe]})
        self.oso.tell({"name": "is_friendly", "args": [self.steve]})

    def teardown(self) -> None:
        self.oso.delete({"name": "is_friendly", "args": [self.sam]})
        self.oso.delete({"name": "is_friendly", "args": [self.gabe]})
        self.oso.delete({"name": "is_friendly", "args": [self.steve]})

    def test_query(self) -> None:
        assert self.oso.query({"name": "hello", "args": [None]}) == unordered(
            [
                {"name": "hello", "args": [self.sam]},
                {"name": "hello", "args": [self.gabe]},
                {"name": "hello", "args": [self.steve]},
            ]
        )

        assert self.oso.query(
            {"name": "hello", "args": [{"type": "User"}]}
        ) == unordered(
            [
                {"name": "hello", "args": [self.sam]},
                {"name": "hello", "args": [self.gabe]},
            ]
        )

        assert self.oso.query(
            {
                "name": "something_else",
                "args": [
                    {"type": "User"},
                    {"type": "Computer"},
                    None,
                ],
            }
        ) == unordered(
            [
                {"name": "something_else", "args": [self.sam, self.steve, None]},
                {"name": "something_else", "args": [self.gabe, self.steve, None]},
            ]
        )


class TestPolicyMetadata:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User { }

            resource Organization {
                roles = ["admin", "member"];
                permissions = [
                    "read", "add_member", "repository.create",
                ];

                # role hierarchy:
                # admins inherit all member permissions
                "member" if "admin";

                # org-level permissions
                "read" if "member";
                "add_member" if "admin";
                # permission to create a repository
                # in the organization
                "repository.create" if "admin";
            }

            resource Repository {
                permissions = ["read", "delete"];
                roles = ["member", "admin"];
                relations = {
                    organization: Organization,
                };

                # inherit all roles from the organization
                role if role on "organization";

                # admins inherit all member permissions
                "member" if "admin";

                "read" if "member";
                "delete" if "admin";
            }
        """
        )

    def test_metadata(self) -> None:
        metadata = self.oso.get_policy_metadata()
        resources = metadata.resources
        assert list(resources.keys()) == [
            "Organization",
            "Repository",
            "User",
            "global",
        ]
        assert resources["Organization"].roles == ["admin", "member"]
        assert resources["Organization"].permissions == [
            "add_member",
            "read",
            "repository.create",
        ]
        assert resources["Organization"].relations == {}
        assert resources["Repository"].roles == ["admin", "member"]
        assert resources["Repository"].permissions == ["delete", "read"]
        assert resources["Repository"].relations == {"organization": "Organization"}
        assert resources["User"].roles == []
        assert resources["User"].permissions == []
        assert resources["User"].relations == {}
        assert resources["global"].roles == []
        assert resources["global"].permissions == []
        assert resources["global"].relations == {}


class TestExceptionRetry:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User {}
            resource Foo {}
        """
        )

    @mock.patch("requests.sessions.Session.post")
    def test_retry_server_exception(self, post_mock):
        # provide side effects for both sequential calls to requests.post
        # first raises an exception and is successfully retried
        post_mock.side_effect = [
            requests.exceptions.ConnectionError("foo"),
            mock.DEFAULT,
        ]
        assert self.oso.query({"name": "foo", "args": [None]}) == []

    @mock.patch("requests.sessions.Session.post")
    def test_no_retry_client_exception(self, post_mock):
        # side-effect for a client exception which should not be retried
        response = mock.Mock(status_code=401)
        post_mock.side_effect = [
            requests.exceptions.HTTPError("foo", response=response)
        ]

        with pytest.raises(requests.exceptions.HTTPError):
            self.oso.query({"name": "foo", "args": [None]})


class TestFallback:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:6000",
            api_key="e_0123456789_12345_osotesttoken01xiIn",
            fallback_url="http://localhost:8081",
        )

        self.actor: Value = {"type": "User", "id": "bob"}
        self.resource: Value = {"type": "Repo", "id": "acme"}

    def test_tell(self) -> None:
        with pytest.raises(requests.exceptions.ConnectionError):
            self.oso.tell(
                {
                    "name": "has_permission",
                    "args": [
                        self.actor,
                        "read",
                        self.resource,
                    ],
                }
            )

    def test_authorize(self) -> None:
        assert self.oso.authorize(
            self.actor,
            "read",
            self.resource,
            [{"name": "has_permission", "args": [self.actor, "read", self.resource]}],
        )


import enum


class OrgRole(str, enum.Enum):
    admin = "admin"
    member = "member"


class TestInputs:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User { }

            resource Organization {
                roles = ["admin", "member"];
                permissions = [
                    "read", "add_member", "repository.create",
                ];

                # role hierarchy:
                # admins inherit all member permissions
                "member" if "admin";

                # org-level permissions
                "read" if "member";
                "add_member" if "admin";
                # permission to create a repository
                # in the organization
                "repository.create" if "admin";
            }

            resource Repository {
                permissions = ["read", "delete"];
                roles = ["member", "admin"];
                relations = {
                    organization: Organization,
                };

                # inherit all roles from the organization
                role if role on "organization";

                # admins inherit all member permissions
                "member" if "admin";

                "read" if "member";
                "delete" if "admin";
            }
        """
        )

    def test_enum(self) -> None:
        self.oso.tell(
            {
                "name": "has_role",
                "args": [
                    {"type": "User", "id": "bob"},
                    OrgRole.admin,
                    {"type": "Organization", "id": "acme"},
                ],
            }
        )
        assert self.oso.get({"name": "has_role", "args": [None, None, None]})[0][
            "args"
        ][1] == {
            "type": "String",
            "id": "admin",
        }

    def teardown(self) -> None:
        self.oso.bulk(delete=[{"name": "has_role", "args": [None, None, None]}])


class TestBulkActions:
    def setup(self) -> None:
        self.oso = Oso(
            url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
        )
        self.oso.policy(
            """
            actor User {}

            resource Repo {
                roles = ["member", "admin"];
                permissions = ["read", "delete"];
                "read" if "member";
                "member" if "admin";
                "delete" if "admin";
            }
        """
        )
        self.user: Value = {"type": "User", "id": "1"}
        self.repos: List[Value] = [{"type": "Repo", "id": str(id)} for id in range(3)]
        self.facts: List[Fact] = [
            {"name": "has_role", "args": [self.user, "member", self.repos[0]]},
            {"name": "has_role", "args": [self.user, "admin", self.repos[1]]},
        ]
        self.oso.bulk(tell=self.facts)

    def teardown(self) -> None:
        self.oso.bulk(delete=self.facts)

    def test_bulk_actions(self) -> None:
        assert self.oso.bulk_actions(self.user, []) == []

        assert self.oso.bulk_actions(self.user, self.repos) == unordered(
            [
                unordered(l)
                for l in [
                    ["read", "delete"],
                    ["read"],
                    [],
                ]
            ]
        )

        context: Fact = {
            "name": "has_role",
            "args": [self.user, "member", self.repos[2]],
        }

        assert self.oso.bulk_actions(
            self.user, self.repos, context_facts=[context]
        ) == unordered(
            [
                unordered(l)
                for l in [
                    ["read", "delete"],
                    ["read"],
                    ["read"],
                ]
            ]
        )
