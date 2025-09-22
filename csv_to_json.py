import csv 
import json 

input_document = 'I;100.000.096;CHN_MINIMUM_SET_Neuswiel VDS - Gelagerd kunststof wiel;;1;pcs;000002;Product;B;150925;151.002.109;15;1'

jsonArray = []
      
input_document_with_headers = 'Import;Description;Searchkey1;Searchkey2;Project;UOM;PartsListQuantity;ItemGroup;MI;Date;ItemNumber;Row;Quantity' + '\n' + input_document 

values = input_document_with_headers.splitlines()

inputReader = csv.DictReader(values, delimiter=';')
for input in inputReader:
    jsonArray.append(input)

jsonString = json.dumps(jsonArray, indent=4)

output_document = jsonString