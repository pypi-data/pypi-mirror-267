from typing import List
from oso_cloud import (
    Oso,
    Value,
    Fact,
    OutputFact,
    VariableFact,
    VariableValue,
    ValueDict,
    OutputVariableFact,
)


def test_oso_types() -> None:
    oso = Oso(
        url="http://localhost:8081", api_key="e_0123456789_12345_osotesttoken01xiIn"
    )

    def is_variable_value(value: VariableValue) -> None:
        pass

    def is_variable_fact(fact: VariableFact) -> None:
        pass

    value_dict: ValueDict = {"type": "User", "id": "1"}
    is_variable_value(value_dict)
    fact: OutputFact = {"name": "foo", "args": [value_dict]}
    is_variable_fact(fact)

    user: Value = {"type": "User", "id": "1"}
    role: Value = "admin"
    org: Value = {"type": "Organization", "id": "2"}

    oso.bulk(delete=[{"name": "has_role", "args": [None, None, None]}])

    user_admin: Fact = {"name": "has_role", "args": [user, role, org]}
    oso.tell(user_admin)

    roles: List[OutputFact] = oso.get({"name": "has_role", "args": [user, None, org]})
    assert roles == [
        {
            "name": "has_role",
            "args": [value_dict, {"type": "String", "id": "admin"}, org],
        }
    ]
    oso.bulk(delete=roles)

    delete_role: VariableFact = {"name": "has_role", "args": [None, None, org]}
    deletions = [r for r in roles] + [delete_role]

    oso.bulk(delete=deletions)

    query_result: List[OutputVariableFact] = oso.query(
        {"name": "has_role", "args": [user, role, org]}
    )
