import asyncio
import aiohttp
import pandas as pd
from gqltojson import transform_gql_to_json  # Import the transformer function
import getmegraph as graph

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

username = "john.newbie@world.com"
password = "john.newbie@world.com"
queryStr = """
query FinanceAnalysis {
  financePage {
    id
    name
    amount
    valid
    lastchange
    financeType {
      id
      name
    }
    project {
      id
      name
      startdate
      enddate
      valid
      team {
        id
        name
      }
    }
    changedby {
      id
      name
    }
  }
}
"""

async def fullPipe():
    token = await getToken(username, password)
    qfunc = query(queryStr, token)
    response = await qfunc({})
    data = response.get("data", None)
    
    # Use the transform_gql_to_json function to transform the data
    transformed_data = transform_gql_to_json(data)
    
    # Convert to pandas DataFrame
    pandasData = pd.DataFrame(transformed_data)
    return pandasData

# Run the full pipeline asynchronously
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    pandasData = loop.run_until_complete(fullPipe())
    print(pandasData)
    pandasData.to_json('result.json', orient='records', lines=True)
    graph.main()
