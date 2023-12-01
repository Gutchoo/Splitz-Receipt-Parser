import json
import requests

url = 'https://app.nanonets.com/api/v2/OCR/Model/08fe2528-e1e6-49c9-aff1-7aae3d13cba5/LabelFile/?async=false'

data = {'file': open('file_path', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('API KEY', ''), files=data)

# print(response.text)

# Assuming response.text contains the JSON string from the OCR model
json_data = json.loads(response.text)

# Extract predictions
predictions = json_data.get("result", [])[0].get("prediction", [])

# Variables to store extracted data
merchant_name = ""
total_amount = ""
tax_amount = ""
date = ""
items = []

# Helper dictionary to organize items
item_details = {}

# Iterate through each prediction
for prediction in predictions:
    if prediction['label'] == 'Merchant_Name':
        merchant_name = prediction['ocr_text']
    elif prediction['label'] == 'Total_Amount':
        total_amount = prediction['ocr_text']
    elif prediction['label'] == 'Tax_Amount':
        tax_amount = prediction['ocr_text']
    elif prediction['label'] == 'Date':
        date = prediction['ocr_text']
    elif prediction['label'] == 'table':
        for cell in prediction['cells']:
            row = cell['row']
            label = cell['label']
            text = cell['text']
            if row not in item_details:
                item_details[row] = {'Quantity': '', 'Description': '', 'Line_Amount': ''}
            if label in ['Quantity', 'Description', 'Line_Amount']:
                item_details[row][label] = text

# Convert item details to a list of structured dictionaries
item_list = []
for item in item_details.values():
    item_list.append({
        'Name': item['Description'], 
        'Price': item['Line_Amount'],
        'Quantity': item['Quantity']
    })

# Final Output Dictionary
final_output = {
    'Merchant Name': merchant_name,
    'Total Amount': total_amount,
    'Tax Amount': tax_amount,
    'Date': date,
    'Items': item_list
}


# print(final_output)