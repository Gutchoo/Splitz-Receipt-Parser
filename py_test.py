import json
import requests

url = 'https://app.nanonets.com/api/v2/OCR/Model/08fe2528-e1e6-49c9-aff1-7aae3d13cba5/LabelFile/?async=false'

data = {'file': open('file path', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('API KEY', ''), files=data)

# print(response.text)

# Assuming response.text contains the JSON string from the OCR model
json_data = json.loads(response.text)

# Extract predictions
predictions = json_data.get("result", [])[0].get("prediction", [])

# Variables to store extracted data
merchant_name = ""
total_amount = 0.0  
tax_amount = 0.0    
date = ""
items = []

# Helper dictionary to organize items
item_details = {}

# Iterate through each prediction
for prediction in predictions:
    if prediction['label'] == 'Merchant_Name':
        merchant_name = prediction['ocr_text']
    elif prediction['label'] == 'Total_Amount':
        # Clean total
        clean_total_amount = prediction['ocr_text'].replace('$', '').replace(',', '') if prediction['ocr_text'] else '0.0'
        try:
            # print(clean_total_amount, type(clean_total_amount))  # comment out
            total_amount = float(clean_total_amount)  # truthy value else 0.0
            # print(total_amount, type(total_amount))  # comment out
        except ValueError:
            total_amount = 0.0  # float conversion error
    elif prediction['label'] == 'Tax_Amount':
        # Clean tax
        clean_tax_amount = prediction['ocr_text'].replace('$', '').replace(',', '') if prediction['ocr_text'] else '0.0'
        try:
            # print(clean_tax_amount, type(clean_tax_amount))  # comment out
            tax_amount = float(clean_tax_amount)  # truthy value else 0.0
            # print(tax_amount, type(tax_amount))  # comment out
        except ValueError: 
            tax_amount = 0.0  # float conversion error
    elif prediction['label'] == 'Date':
        date = prediction['ocr_text']
    elif prediction['label'] == 'table':
        for cell in prediction['cells']:
            row = cell['row']
            label = cell['label']
            text = cell['text']
            if row not in item_details:
                item_details[row] = {'Quantity': '1', 'Description': '', 'Line_Amount': ''}  # Default quantity to '1'
            if label in ['Quantity', 'Description', 'Line_Amount']:
                item_details[row][label] = text

# Convert item details to a list of structured dictionaries
item_list = []
for item in item_details.values():
    # Cleaning line amount
    clean_line_amount = item['Line_Amount'].replace('$', '').replace(',', '') if item['Line_Amount'] else '0.0'
    try:
        price = float(clean_line_amount)
    except ValueError:
        price = 0.0

    # Converting quantity to an integer
    try:
        quantity = int(item['Quantity']) if item['Quantity'] else 1
    except ValueError:
        quantity = 1  # Default to 1 if conversion fails

    item_list.append({
        'Name': item['Description'], 
        'Price': price,
        'Quantity': quantity
    })

# Final Output Dictionary
final_output = {
    'Merchant Name': merchant_name,
    'Total Amount': total_amount,
    'Tax Amount': tax_amount,
    'Date': date,
    'Items': item_list
}

print(final_output) # comment out