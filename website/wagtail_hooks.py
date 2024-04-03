from wagtail import hooks

from website.graphql.schema import CustomQuery


@hooks.register("register_schema_query")
def register_custom_query(query_mixins):
    query_mixins.append(CustomQuery)
