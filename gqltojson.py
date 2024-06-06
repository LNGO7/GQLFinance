import json

def transform_gql_to_json(gql_query):
    # Převod vstupního GQL do požadovaného formátu
    sourceTable = []
    
    for finance_item in gql_query["financePage"]:
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
