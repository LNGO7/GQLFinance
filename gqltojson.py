import json

def transform_gql_to_json(gql_query):
    # Převod vstupního GQL do požadovaného formátu
    sourceTable = []

    for finance_item in gql_query["data"]["financePage"]:
        row = {}
        row["id"] = finance_item["id"]
        row["name"] = finance_item["name"]
        row["amount"] = finance_item["amount"]
        row["valid"] = finance_item["valid"]
        row["lastchange"] = finance_item["lastchange"]
        row["financeTypeName"] = finance_item["financeType"][0]["name"]
        row["projectID"] = finance_item["project"]["id"]
        row["projectName"] = finance_item["project"]["name"]
        row["projectStartDate"] = finance_item["project"]["startdate"]
        row["projectEndDate"] = finance_item["project"]["enddate"]
        row["projectValid"] = finance_item["project"]["valid"]
        row["teamID"] = finance_item["project"]["team"]["id"]
        row["teamName"] = finance_item["project"]["team"]["name"]
        row["changedby"] = finance_item["changedby"]
        
        sourceTable.append(row)

    return sourceTable

# Vstupní GQL dotaz
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

# Převod GQL dotazu pomocí funkce
sourceTable = transform_gql_to_json(gql_query)

# Uložení výsledného formátu do JSON souboru
with open('result.json', "w", encoding='utf-8') as outputFile:
    json.dump(sourceTable, outputFile)
