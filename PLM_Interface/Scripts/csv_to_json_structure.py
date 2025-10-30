input_document = 'IL;151.004.757;STRAP CARRYING PENTHEON;PRJ00123;1;pcs;000004;Product;001;020925;151.002.108;15;3' + '\n' + 'IH;151.004.757;STRAP CARRYING PENTHEON;PRJ00123;1;pcs;000004;Product;001;020925;151.002.109;15;1'
input_document = 'IH;450.000.002;Test 2 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.003;Test 3 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.004;Test 4 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.005;Test 5 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;;;;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.002;;1;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.003;;2;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.004;;5;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.005;;10;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;ltr;000006;Product;000;020930;632.011.024;;0.9;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;mm;000006;Product;000;020930;632.011.071;2930;1;'

#declarations:    
import csv 
import json

input_document_with_headers = 'Import;Product;Description;Project;BOM_Quantity;Unit;Item_Group;Item_Type;Revision;Effective_Date;Material;Length;Net_Quantity' + '\n' + input_document 

values = input_document_with_headers.splitlines()
products = {}
position = 0

#add labels
inputReader = csv.DictReader(values,delimiter=';')
for row in inputReader:
    
    importValue = row['Import']
    product = row['Product']

    
    key = f"{importValue}_{product}"
    
    if key not in products:
        position = 0
        products[key] = {
            "Import": row['Import'],
            "Product": row['Product'],
            "Description": row['Description'],
            "Project": row['Project'],
            "BOM_Quantity": row['BOM_Quantity'],
            "Unit": row['Unit'],
            "Item_Group": row['Item_Group'],
            "Item_Type": row['Item_Type'],
            "Revision": row['Revision'],
            "Effective_Date": row['Effective_Date'],
            "Materials": []
        }
        
    position += 10
    if importValue == 'IL':
        material_entry = {
            "Position": position,
            "Material": row['Material'],
            "Length": row['Length'],
            "Net_Quantity": row['Net_Quantity'],
            "Unit": row['Unit']
        }
    
        products[key]["Materials"].append(material_entry)
  

output_json_object = {"Products": list(products.values())}

output_json = json.dumps(output_json_object, indent=4)

print(output_json)
