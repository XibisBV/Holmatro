# TODO: remove example and use data flow params to set input_document
input_document = 'IL;151.004.757;STRAP CARRYING PENTHEON;PRJ00123;1;pcs;000004;Product;001;020925;151.002.108;15;3' + '\n' + 'IH;151.004.757;STRAP CARRYING PENTHEON;PRJ00123;1;pcs;000004;Product;001;020925;151.002.109;15;1'
input_document = 'IH;450.000.002;Test 2 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.003;Test 3 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.004;Test 4 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.005;Test 5 for New ERP;PRE000625;1;pcs;000004;Product;000;020930;;;;' + '\n' + 'IH;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;;;;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.002;;1;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.003;;2;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.004;;5;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;pcs;000001;Product;000;020930;450.000.005;;10;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;ltr;000006;Product;000;020930;632.011.024;;0.9;' + '\n' + 'IL;450.000.001;Test 1 for New ERP;PRE000625;1;mm;000006;Product;000;020930;632.011.071;2930;1;'
    
import csv 
import json
from collections import defaultdict 
pos_line = 0
next_product_name = ''
prev_product_name = 'A'

product_data = defaultdict(list)

input_document_with_headers = 'Import;Product;Description;Project;BOM_Quantity;Unit;Item_Group;Item_Type;Revision;Effective_Date;Material;Length;Net_Quantity' + '\n' + input_document 

values = input_document_with_headers.splitlines()

inputReader = csv.DictReader(values,delimiter=';')
for row in inputReader:
#    next_product_name = row['Product']
#    if prev_product_name != next_product_name:
#        pos_line = 10
#    else:
    pos_line =+ 10

    import_name = row['Import']
    product_name = row['Product']
 #  prev_product_name = row['Product']
    description_name = row['Description']
    project_name = row['Project']
    BOM_Quantity = row['BOM_Quantity']
    Unit = row['Unit']
    Item_Group = row['Item_Group']
    Item_Type = row['Item_Type']
    Revision = row['Revision']
    Effective_Date = row['Effective_Date']

    material_line = {
                    "Position": pos_line,
                    "Material": row['Material'],
                    "Length": row['Length'],
                    "Net_Quantity": row['Net_Quantity']
    }
    
    product_data[import_name, product_name, description_name, project_name, BOM_Quantity, Unit,Item_Group,Item_Type,Revision,Effective_Date].append(material_line)

json_output_list = []
for product_name, materials_list in product_data.items():
    # ⭐ KEY CHANGE: Create an object for each product with explicit labels
    product_object = {
        "Import": import_name,
        "Product": product_name,
        "Description": description_name,
        "Project": project_name,
        "BOM_Quantity": BOM_Quantity,
        "Unit": Unit,
        "Item_Group": Item_Group,
        "Item_Type": Item_Type,
        "Revision": Revision,
        "Effective_Date": Effective_Date,
        "Materials": materials_list # The sub-array is explicitly labeled "Materials"
    }
    json_output_list.append(product_object)

output_json = json.dumps(json_output_list, indent=4)

print(json_output_list)
print(output_json)
