import asyncio
import aiohttp
from itertools import product
from functools import reduce
import pandas as pd

async def getToken(username, password):
    keyurl = "http://localhost:33001/oauth/login3"
    async with aiohttp.ClientSession() as session:
        async with session.get(keyurl) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to get key: {resp.status}")
            keyJson = await resp.json()

        payload = {"key": keyJson["key"], "username": username, "password": password}
        async with session.post(keyurl, json=payload) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to get token: {resp.status}")
            tokenJson = await resp.json()

    return tokenJson.get("token", None)

def query(q, token):
    async def post(variables):
        gqlurl = "http://localhost:33001/api/gql"
        payload = {"query": q, "variables": variables}
        cookies = {'authorization': token}

        async with aiohttp.ClientSession() as session:
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"Query failed: {resp.status} - {text}")
                return await resp.json()
    return post

def enumerateAttrs(attrs):
    for key, value in attrs.items():
        names = value.split(".")
        name = names[0]
        yield key, name

def flattenList(inList, outItem, attrs):
    for item in inList:
        assert isinstance(item, dict), "Expected dict in list"
        for row in flatten(item, outItem, attrs):
            yield row

def flattenDict(inDict, outItem, attrs):
    result = {**outItem}
    complexAttrs = []
    for key, value in enumerateAttrs(attrs):
        attributeValue = inDict.get(value, None)
        if isinstance(attributeValue, (list, dict)):
            complexAttrs.append((key, value))
        else:
            result[key] = attributeValue

    lists = []
    for key, value in complexAttrs:
        attributeValue = inDict.get(value, None)
        prefix = f"{value}."
        prefixlen = len(prefix)
        subAttrs = {key: value[prefixlen:] for key, value in attrs.items() if value.startswith(prefix)}
        items = list(flatten(attributeValue, result, subAttrs))
        lists.append(items)

    if not lists:
        yield result
    else:
        for element in product(*lists):
            reduced = reduce(lambda a, b: {**a, **b}, element, {})
            yield reduced

def flatten(inData, outItem, attrs):
    if isinstance(inData, dict):
        yield from flattenDict(inData, outItem, attrs)
    elif isinstance(inData, list):
        yield from flattenList(inData, outItem, attrs)
    else:
        raise ValueError(f"Unexpected type: {type(inData)}")

def toTable(flatData):
    return pd.DataFrame(flatData)

username = "john.newbie@world.com"
password = "john.newbie@world.com"
queryStr = """
{
  result: userPage(
    where: {memberships: {group: {name: {_ilike: "%uni%"}}}}
  ) {
    id
    email
    name
    surname
    presences {
      event {
        id
        name
        startdate
        enddate
        eventType {
          id
          name
        }
      }
      presenceType {
        id
        name
      }
    }
  }
}
"""

mappers = {
    "id": "id",
    "name": "name",
    "surname": "surname",
    "email": "email",
    "eventid": "presences.event.id",
    "eventname": "presences.event.name",
    "startdate": "presences.event.startdate",
    "enddate": "presences.event.enddate",
    "eventTypeid": "presences.event.eventType.id",
    "eventTypename": "presences.event.eventType.name",
    "presenceTypeid": "presences.presenceType.id",
    "presenceTypename": "presences.presenceType.name"
}

async def fullPipe():
    token = await getToken(username, password)
    qfunc = query(queryStr, token)
    response = await qfunc({})
    data = response.get("data", None)
    result = data.get("result", None)
    flatData = list(flatten(result, {}, mappers))
    pandasData = toTable(flatData)
    return pandasData

# Run the full pipeline asynchronously
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    pandasData = loop.run_until_complete(fullPipe())
    print(pandasData)
