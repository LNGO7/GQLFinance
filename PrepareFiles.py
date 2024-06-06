import json
import pandas as pd
import openpyxl
from openpyxl.chart import PieChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows  
import plotly.express as px

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def parse_json_to_dataframe(data):
    finance_pages = data['data']['financePage']
    parsed_data = {
        'ID': [],
        'Name': [],
        'Amount': [],
        'Finance Type': [],
        'Project Name': [],
        'Start Date': [],
        'End Date': []
    }

    for page in finance_pages:
        parsed_data['ID'].append(page['id'])
        parsed_data['Name'].append(page['name'])
        parsed_data['Amount'].append(page['amount'])
        parsed_data['Finance Type'].append(page['financeType'][0]['name'])
        parsed_data['Project Name'].append(page['project']['name'])
        parsed_data['Start Date'].append(page['project']['startdate'])
        parsed_data['End Date'].append(page['project']['enddate'])

    return pd.DataFrame(parsed_data)

def save_to_excel(dataframe, excel_filename):
    wb = openpyxl.Workbook()
    ws = wb.active

    for row in dataframe_to_rows(dataframe, index=False, header=True):
        ws.append(row)

    # Create Pie Chart
    pie = PieChart()
    labels = Reference(ws, min_col=4, min_row=2, max_row=len(dataframe)+1)
    data = Reference(ws, min_col=3, min_row=2, max_row=len(dataframe)+1)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(labels)
    pie.title = "Finance Analysis - Pie Chart"
    ws.add_chart(pie, "G1")

    # Create Sunburst Chart
    sunburst_fig = px.sunburst(dataframe, path=['Finance Type', 'Project Name'], values='Amount', title='Finance Analysis - Sunburst Chart')
    sunburst_fig.update_traces(textinfo='label+percent entry')
    sunburst_fig.write_image("sunburst_chart.png")
    img = openpyxl.drawing.image.Image("sunburst_chart.png")
    ws.add_image(img, 'G10')

    wb.save(excel_filename)

def main():
    json_file_path = 'finance_analysis.json'
    excel_filename = 'finance_data.xlsx'

    # Load JSON file
    data = load_json_file(json_file_path)

    # Parse JSON data to DataFrame
    df = parse_json_to_dataframe(data)

    # Save DataFrame to Excel file with charts
    save_to_excel(df, excel_filename)

if __name__ == "__main__":
    main()
