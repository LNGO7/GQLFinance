import json
import pandas as pd
import openpyxl
from openpyxl.chart import LineChart, PieChart, Reference, Series
from openpyxl.utils.dataframe import dataframe_to_rows

# Load the JSON data
file_path = 'output.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert the query to standard JSON
query_str = data['query']
query_json = json.loads(query_str)

# Extracting the relevant data
finance_data = query_json['data']['financePage']

# Prepare data for pie chart including nested financeType data
pie_data = [(item['financeType'][0]['name'], item['amount']) for item in finance_data]

# Prepare data for line chart including nested project data
line_data = [(item['name'], item['project']['name'], item['project']['startdate'], item['project']['enddate']) 
             for item in finance_data if 'project' in item and 'startdate' in item['project'] and 'enddate' in item['project']]

# Creating the pie chart DataFrame
pie_df = pd.DataFrame(pie_data, columns=['Name', 'Amount'])

# Creating the line chart DataFrame
line_df = pd.DataFrame(line_data, columns=['FinanceName', 'ProjectName', 'Startdate', 'Enddate'])
line_df['Startdate'] = pd.to_datetime(line_df['Startdate'])
line_df['Enddate'] = pd.to_datetime(line_df['Enddate'])

# Create a new Excel workbook
wb = openpyxl.Workbook()

# Write pie chart data to Excel
ws = wb.active
ws.title = "Pie Chart Data"

for r_idx, row in enumerate(dataframe_to_rows(pie_df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        ws.cell(row=r_idx, column=c_idx, value=value)

# Create the pie chart in Excel
pie = PieChart()
labels = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
data = Reference(ws, min_col=2, min_row=1, max_row=ws.max_row)
pie.add_data(data, titles_from_data=True)
pie.set_categories(labels)
pie.title = "Distribution by Amount"
ws.add_chart(pie, "E2")

# Write line chart data to Excel
line_ws = wb.create_sheet(title="Line Chart Data")

for r_idx, row in enumerate(dataframe_to_rows(line_df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        line_ws.cell(row=r_idx, column=c_idx, value=value)

# Create the line chart in Excel
line_chart = LineChart()
line_chart.title = "Project Timeline"
line_chart.y_axis.title = "Project Name"
line_chart.x_axis.title = "Date"

for index, row in line_df.iterrows():
    series = Series(values=Reference(line_ws, min_col=3, min_row=index+2, max_col=4, max_row=index+2),
                    title=row['ProjectName'])
    line_chart.series.append(series)

line_ws.add_chart(line_chart, "E2")

# Save the workbook
excel_file_path_corrected = 'finance_charts.xlsx'
wb.save(excel_file_path_corrected)

print(f"Excel file saved to {excel_file_path_corrected}")
