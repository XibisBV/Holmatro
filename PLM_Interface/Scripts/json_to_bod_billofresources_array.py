# TODO: remove example and use data flow params to set input_document
input_json = """{
    "Products": [
        {
            "Import": "IL",
            "Product": "450.000.001",
            "Description": "Test 1 for New ERP",
            "Project": "PRE000625",
            "BOM_Quantity": "1",
            "Unit": "pcs",
            "Item_Group": "000001",
            "Item_Type": "Product",
            "Revision": "000",
            "Effective_Date": "020930",
            "Materials": [
                {
                    "Position": 10,
                    "Material": "450.000.002",
                    "Length": "",
                    "Net_Quantity": "1",
                    "Unit": "pcs"
                },
                {
                    "Position": 20,
                    "Material": "450.000.003",
                    "Length": "",
                    "Net_Quantity": "2",
                    "Unit": "pcs"
                },
                {
                    "Position": 30,
                    "Material": "450.000.004",
                    "Length": "",
                    "Net_Quantity": "5",
                    "Unit": "pcs"
                },
                {
                    "Position": 40,
                    "Material": "450.000.005",
                    "Length": "",
                    "Net_Quantity": "10",
                    "Unit": "pcs"
                },
                {
                    "Position": 50,
                    "Material": "632.011.024",
                    "Length": "",
                    "Net_Quantity": "0.9",
                    "Unit": "ltr"
                },
                {
                    "Position": 60,
                    "Material": "632.011.071",
                    "Length": "2930",
                    "Net_Quantity": "1",
                    "Unit": "mm"
                }
            ]
        }
    ]
}"""

company = "4000"
tenant = "L567NQT482F74MTX_TST"
site = "S_STA001"

#declarations
import xml.etree.ElementTree as ET
import json
from datetime import datetime
from datetime import date

#Receive input JSON
input_document = input_json
data = json.loads(input_document)

now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
from datetime import datetime, timezone
# 1. Define the input string
input_date_str = data["Products"][0]["Effective_Date"]  # Example: September 29, 2025

# Define the variable with the fixed date value
first_day_of_2038 = '010138'

# 2. Define the format string for strptime
# %d: Day of the month (01-31)
# %m: Month (01-12)
# %y: Year without century (00-99)
format_string = "%d%m%y"

# 3. Parse the string into a naive datetime object
# A 'naive' datetime object has no timezone information
naive_dt = datetime.strptime(input_date_str, format_string)
naive_dt_38 = datetime.strptime(first_day_of_2038, format_string)

# 4. Make the datetime object timezone-aware and set it to GMT (UTC)
# The datetime.timezone.utc object represents the UTC (or "Zulu") timezone.
gmt_dt = naive_dt.replace(tzinfo=timezone.utc)
gmt_dt_38 = naive_dt_38.replace(tzinfo=timezone.utc)

# You can also format it back into a common string standard like ISO 8601,
# which includes the 'Z' for Zulu time (a common representation for UTC/GMT).
iso_8601_format = gmt_dt.isoformat()
iso_8601_format_38 = gmt_dt_38.isoformat()

root = ET.Element("ProcessBillOfResources", {
    "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
})

#build applicaton area
application_area = ET.SubElement(root, "ApplicationArea")
sender = ET.SubElement(application_area, "Sender")
ET.SubElement(sender, "LogicalID").text = "lid://infor.ln.ln01/" + company
ET.SubElement(sender, "ComponentID").text = "erp"
ET.SubElement(sender, "ConfirmationCode").text = "OnError"
ET.SubElement(application_area, "CreationDateTime").text = now
ET.SubElement(application_area, "BODID").text = "infor-nid:" + tenant + ":" + company + ":" + data["Products"][0]["Product"] + data["Products"][0]["Revision"] + "?BillOfResources&verb=Process"

#build data area
data_area = ET.SubElement(root, "DataArea")
process = ET.SubElement(data_area, "Process")
ET.SubElement(process, "TenantID").text = tenant
ET.SubElement(process, "AccountingEntityID").text = company
ET.SubElement(process, "LocationID")
action_criteria = ET.SubElement(process, "ActionCriteria")
ET.SubElement(action_criteria, "ActionExpression", {"actionCode": "Replace"})

#build header
bor = ET.SubElement(data_area, "BillOfResources")
bor_header = ET.SubElement(bor, "BillOfResourcesHeader")
doc_id = ET.SubElement(bor_header, "DocumentID")
ET.SubElement(doc_id, "ID", {
    "accountingEntity": company,
    "lid": "lid://infor.ln.ln01/" + company,
    "variationID": data["Products"][0]["Revision"]
}).text = data["Products"][0]["Product"] #data["Products"][0]["Project"] + 
ET.SubElement(doc_id, "RevisionID").text = data["Products"][0]["Revision"]
#doc_id = ET.SubElement(bor_header, "ProjectReference")
#ET.SubElement(doc_id, "ID").text = data["Products"][0]["Project"]
#doc_id = ET.SubElement(bor_header, "ProjectReferenceID")
#ET.SubElement(doc_id, "ID").text = data["Products"][0]["Project"]
status = ET.SubElement(bor_header, "Status")
ET.SubElement(status, "Code").text = "Open"
#ET.SubElement(bor_header, "EffectiveDateTime").text = now
ET.SubElement(bor_header, "EffectiveDateTime").text = iso_8601_format
ET.SubElement(bor_header, "InactiveDateTime").text = iso_8601_format_38
ET.SubElement(bor_header, "RunSizeBaseUOMQuantity").text = data["Products"][0]["BOM_Quantity"]

#build header user area
user_area = ET.SubElement(bor_header, "UserArea")
prop1 = ET.SubElement(user_area, "Property")
ET.SubElement(prop1, "NameValue", {
    "name": "ln.BODName",
    "type": "StringType"
}).text = "BillOfResourcesReceivedPBOMBOD"

#build operations/ consumed items
operations = ET.SubElement(bor, "Operations")
ET.SubElement(operations, "ID").text = "10"
status_op = ET.SubElement(operations, "Status")
ET.SubElement(status_op, "Code").text = "Open"

for material in data["Products"][0]["Materials"]:

    consumed_item = ET.SubElement(operations, "ConsumedItem")
    ET.SubElement(consumed_item, "LineNumber").text = str(material["Position"])
    item_id = ET.SubElement(consumed_item, "ItemID")
    ET.SubElement(item_id, "ID").text = material["Material"]
    ET.SubElement(consumed_item, "BaseUOMQuantity", {"unitCode": material["Unit"].upper()}).text = material["Net_Quantity"]
    etp = ET.SubElement(consumed_item, "EffectiveTimePeriod")
    ET.SubElement(etp, "StartDateTime").text = iso_8601_format
    status_ci = ET.SubElement(consumed_item, "Status")
    ET.SubElement(status_ci, "Code").text = "Open"
 #  ET.SubElement(consumed_item, "Note").text = "DUMMYNOTE"

    #build consumed items user area
    ua_ci = ET.SubElement(consumed_item, "UserArea")
#    p1 = ET.SubElement(ua_ci, "Property")
#    ET.SubElement(p1, "NameValue", {"name": "ln.UseUpItem"}).text = material["Material"]
#    p2 = ET.SubElement(ua_ci, "Property")
#    ET.SubElement(p2, "NameValue", {"name": "ln.PhantomIndicator"}).text = "No"
    p2 = ET.SubElement(ua_ci, "Property")
    # Access the 'Length' attribute
    length_value = material.get("Length")
    # Test if the value is an empty string ("")
    if length_value == "":
       ET.SubElement(p2, "NameValue", {"name": "ln.Length", "unitCode": ""}).text = "0"
    elif length_value is None:
       ET.SubElement(p2, "NameValue", {"name": "ln.Length", "unitCode": ""}).text = "0"
    else:
        ET.SubElement(p2, "NameValue", {"name": "ln.Length", "unitCode": material["Unit"].upper()}).text = material["Length"]

output_bod = ET.tostring(root, encoding="utf-8").decode("utf-8")

#Only for TERMINAL in VSC
print(output_bod)