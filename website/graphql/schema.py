import asyncio

import graphene
import requests
from aiodataloader import DataLoader


class CharacterLoader(DataLoader):
    async def batch_load_fn(self, keys):
        print(keys)
        return keys


char_loader = CharacterLoader()


async def get_usr(id):
    usr = await char_loader.load(id)
    return usr


class Character(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()


class CustomQuery(graphene.ObjectType):
    name = graphene.String()
    charachters = graphene.List(Character)
    character = graphene.Field(Character, id=graphene.Int(required=True))

    def resolve_name(root, info):
        return "Eric"

    def resolve_charachters(root, info, id=None):
        if id is None:
            response = requests.get("https://rickandmortyapi.com/api/character")
            data = response.json()
            for char in data["results"]:
                char_loader.prime(char["id"], char)

            return data["results"]

    def resolve_character(root, info, id):
        response = requests.get("https://rickandmortyapi.com/api/character/" + str(id))
        return response.json()
