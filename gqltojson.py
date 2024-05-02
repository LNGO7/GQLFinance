import json

# GQL dotaz
gql_query = {
  "data": {
    "financePage": [
      {
        "id": "f911230f-7e1f-4e9b-90a9-b921996ceb87",
        "name": "komplet",
        "amount": 100000,
        "valid": True,
        "lastchange": "2024-04-17T10:41:49.370920",
        "financeType": [
          {
            "id": "9e37059c-de2c-4112-9009-559c8b0396f1",
            "name": "osobní náklady"
          }
        ],
        "project": {
          "id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb",
          "name": "Nukleární reaktor pro budovy",
          "startdate": "2023-01-01T17:27:12",
          "enddate": "2025-12-31T17:27:12",
          "valid": True,
          "team": {
            "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
            "name": "Uni"
          }
        },
        "changedby": None
      }
    ]
  }
}

# Převedení GQL dotazu na JSON formát
json_query = {"query": json.dumps(gql_query)}

# Uložení JSON formátu do souboru
with open("output.json", "w") as json_file:
    json.dump(json_query, json_file, indent=2)