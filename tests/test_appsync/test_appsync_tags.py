import boto3

from moto import mock_aws


@mock_aws
def test_create_graphql_api_with_tags():
    client = boto3.client("appsync", region_name="ap-southeast-1")
    api = client.create_graphql_api(
        name="api1", authenticationType="API_KEY", tags={"key": "val", "key2": "val2"}
    )["graphqlApi"]

    assert api["tags"] == {"key": "val", "key2": "val2"}

    api = client.get_graphql_api(apiId=api["apiId"])["graphqlApi"]

    assert api["tags"] == {"key": "val", "key2": "val2"}


@mock_aws
def test_tag_resource():
    client = boto3.client("appsync", region_name="us-east-2")
    api = client.create_graphql_api(name="api1", authenticationType="API_KEY")[
        "graphqlApi"
    ]

    client.tag_resource(resourceArn=(api["arn"]), tags={"key1": "val1"})

    api = client.get_graphql_api(apiId=api["apiId"])["graphqlApi"]
    assert api["tags"] == {"key1": "val1"}


@mock_aws
def test_tag_resource_with_existing_tags():
    client = boto3.client("appsync", region_name="us-east-2")
    api = client.create_graphql_api(
        name="api1", authenticationType="API_KEY", tags={"key": "val", "key2": "val2"}
    )["graphqlApi"]

    client.untag_resource(resourceArn=api["arn"], tagKeys=["key"])

    client.tag_resource(
        resourceArn=(api["arn"]), tags={"key2": "new value", "key3": "val3"}
    )

    api = client.get_graphql_api(apiId=api["apiId"])["graphqlApi"]
    assert api["tags"] == {"key2": "new value", "key3": "val3"}


@mock_aws
def test_untag_resource():
    client = boto3.client("appsync", region_name="eu-west-1")
    api = client.create_graphql_api(
        name="api1", authenticationType="API_KEY", tags={"key": "val", "key2": "val2"}
    )["graphqlApi"]

    client.untag_resource(resourceArn=api["arn"], tagKeys=["key"])

    api = client.get_graphql_api(apiId=api["apiId"])["graphqlApi"]
    assert api["tags"] == {"key2": "val2"}


@mock_aws
def test_untag_resource_all():
    client = boto3.client("appsync", region_name="eu-west-1")
    api = client.create_graphql_api(
        name="api1", authenticationType="API_KEY", tags={"key": "val", "key2": "val2"}
    )["graphqlApi"]

    client.untag_resource(resourceArn=api["arn"], tagKeys=["key", "key2"])

    api = client.get_graphql_api(apiId=api["apiId"])["graphqlApi"]
    assert api["tags"] == {}


@mock_aws
def test_list_tags_for_resource():
    client = boto3.client("appsync", region_name="ap-southeast-1")
    api = client.create_graphql_api(
        name="api1", authenticationType="API_KEY", tags={"key": "val", "key2": "val2"}
    )["graphqlApi"]

    resp = client.list_tags_for_resource(resourceArn=api["arn"])

    assert resp["tags"] == {"key": "val", "key2": "val2"}


@mock_aws
def test_resource_groups_tagging_api():
    region = "us-west-2"
    client = boto3.client("appsync", region_name=region)
    rtapi_client = boto3.client("resourcegroupstaggingapi", region_name=region)

    api = client.create_graphql_api(
        name="api-with-tags",
        authenticationType="API_KEY",
        tags={"key": "val", "key2": "val2"},
    )["graphqlApi"]
    client.create_graphql_api(name="api-no-tags", authenticationType="API_KEY")[
        "graphqlApi"
    ]

    resp = rtapi_client.get_resources(ResourceTypeFilters=["appsync"])
    assert len(resp["ResourceTagMappingList"]) == 1
    assert resp["ResourceTagMappingList"][0]["ResourceARN"] == api["arn"]
    assert resp["ResourceTagMappingList"][0]["Tags"] == [
        {"Key": "key", "Value": "val"},
        {"Key": "key2", "Value": "val2"},
    ]
