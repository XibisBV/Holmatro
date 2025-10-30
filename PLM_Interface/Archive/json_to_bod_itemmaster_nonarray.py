# TODO: remove example and use data flow params to set input_document
input_json = """
[
    {
        "Import": "IH",
        "Product": "450.000.002",
        "Description": "Test 1 for New ERP",
        "Project": "PRE000625",
        "BOM_Quantity": "1",
        "Unit": "mm",
        "Item_Group": "000006",
        "Item_Type": "Product",
        "Revision": "000",
        "Effective_Date": "020930",
        "Materials": [
            {
                "Position": 10,
                "Material": "",
                "Length": "",
                "Net_Quantity": ""
            }
        ]
    },
    {
        "Import": "IH",
        "Product": "450.000.003",
        "Description": "Test 1 for New ERP",
        "Project": "PRE000625",
        "BOM_Quantity": "1",
        "Unit": "mm",
        "Item_Group": "000006",
        "Item_Type": "Product",
        "Revision": "000",
        "Effective_Date": "020930",
        "Materials": [
            {
                "Position": 10,
                "Material": "",
                "Length": "",
                "Net_Quantity": ""
            }
        ]
    },
    {
        "Import": "IH",
        "Product": "450.000.004",
        "Description": "Test 1 for New ERP",
        "Project": "PRE000625",
        "BOM_Quantity": "1",
        "Unit": "mm",
        "Item_Group": "000006",
        "Item_Type": "Product",
        "Revision": "000",
        "Effective_Date": "020930",
        "Materials": [
            {
                "Position": 10,
                "Material": "",
                "Length": "",
                "Net_Quantity": ""
            }
        ]
    },
    {
        "Import": "IH",
        "Product": "450.000.005",
        "Description": "Test 1 for New ERP",
        "Project": "PRE000625",
        "BOM_Quantity": "1",
        "Unit": "mm",
        "Item_Group": "000006",
        "Item_Type": "Product",
        "Revision": "000",
        "Effective_Date": "020930",
        "Materials": [
            {
                "Position": 10,
                "Material": "",
                "Length": "",
                "Net_Quantity": ""
            }
        ]
    },
    {
        "Import": "IL",
        "Product": "450.000.001",
        "Description": "Test 1 for New ERP",
        "Project": "PRE000625",
        "BOM_Quantity": "1",
        "Unit": "mm",
        "Item_Group": "000006",
        "Item_Type": "Product",
        "Revision": "000",
        "Effective_Date": "020930",
        "Materials": [
            {
                "Position": 10,
                "Material": "",
                "Length": "",
                "Net_Quantity": ""
            },
            {
                "Position": 20,
                "Material": "450.000.002",
                "Length": "",
                "Net_Quantity": "1"
            },
            {
                "Position": 30,
                "Material": "450.000.003",
                "Length": "",
                "Net_Quantity": "2"
            },
            {
                "Position": 40,
                "Material": "450.000.004",
                "Length": "",
                "Net_Quantity": "5"
            },
            {
                "Position": 50,
                "Material": "450.000.005",
                "Length": "",
                "Net_Quantity": "10"
            },
            {
                "Position": 60,
                "Material": "632.011.024",
                "Length": "",
                "Net_Quantity": "0.9"
            },
            {
                "Position": 70,
                "Material": "632.011.071",
                "Length": "2930",
                "Net_Quantity": "1"
            }
        ]
    }
]"""

input_json = """
{
    "Import": "IH",
    "Product": "151.004.757",
    "Description": "STRAP CARRYING PENTHEON",
    "Project": "BPE000003",
    "BOM_Quantity": "1",
    "Unit": "pcs",
    "Item_Group": "000003",
    "Item_Type": "Product",
    "Revision": "009",
    "Effective_Date": "120527",
    "Material": "151.002.109",
    "Length": "15",
    "Net_Quantity": "1"
}"""

company = "4000"
tenant = "L567NQT482F74MTX_TST"
site = "S_STA001"

#Declarations
import xml.etree.ElementTree as ET
import json
from datetime import datetime

#Receive input from input-variable:
input_document = input_json
data = json.loads(input_document)

#Set current date and time:
now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
from datetime import datetime, timezone

# 1. Define the input string
input_date_str = data["Effective_Date"]  # Example: September 29, 2025

# 2. Define the format string for strptime
# %d: Day of the month (01-31)
# %m: Month (01-12)
# %y: Year without century (00-99)
format_string = "%d%m%y"

# 3. Parse the string into a naive datetime object
# A 'naive' datetime object has no timezone information
naive_dt = datetime.strptime(input_date_str, format_string)

# 4. Make the datetime object timezone-aware and set it to GMT (UTC)
# The datetime.timezone.utc object represents the UTC (or "Zulu") timezone.
gmt_dt = naive_dt.replace(tzinfo=timezone.utc)

# You can also format it back into a common string standard like ISO 8601,
# which includes the 'Z' for Zulu time (a common representation for UTC/GMT).
iso_8601_format = gmt_dt.isoformat()

#Start building XML Structure:
root = ET.Element("ProcessItemMaster", {
    "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
})

#ApplicationArea
application_area = ET.SubElement(root, "ApplicationArea")
sender = ET.SubElement(application_area, "Sender")
ET.SubElement(sender, "LogicalID").text = "lid://infor.ln.ln01/" + company
ET.SubElement(sender, "ComponentID").text = "erp"
ET.SubElement(sender, "ConfirmationCode").text = "OnError"
ET.SubElement(application_area, "CreationDateTime").text = now
ET.SubElement(application_area, "BODID").text = "infor-nid:" + tenant + ":" + company + ":" + data["Product"] + "?ItemMaster&verb=Process"

#DataArea
data_area = ET.SubElement(root, "DataArea")
process = ET.SubElement(data_area, "Process")
ET.SubElement(process, "TenantID").text = tenant
ET.SubElement(process, "AccountingEntityID").text = company
ET.SubElement(process, "LocationID")
action_criteria = ET.SubElement(process, "ActionCriteria")
ET.SubElement(action_criteria, "ActionExpression", {"actionCode": "Replace"})

bor = ET.SubElement(data_area, "ItemMaster")
bor_header = ET.SubElement(bor, "ItemMasterHeader")
doc_id = ET.SubElement(bor_header, "ItemID")
ET.SubElement(doc_id, "ID", {
    "accountingEntity": company,
    "lid": "lid://infor.ln.ln01/" + company,
    "variationID": data["Revision"]
}).text = data["Product"]
ET.SubElement(doc_id, "RevisionID").text = data["Revision"]
doc_id = ET.SubElement(bor_header, "ProjectReference")
ET.SubElement(doc_id, "ID").text = data["Project"]
ET.SubElement(bor_header, "Description", {"type": "Item"}).text = data["Description"]
classification = ET.SubElement(bor_header, "Classification")
codes = ET.SubElement(classification, "Codes")
ET.SubElement(codes, "Code", {
    "listID": "Item Types",
    "sequence": "1"}).text = data["Item_Type"]
ET.SubElement(codes, "Code", {
    "listID": "Item Groups",
    "sequence": "2", "accountingEntity": company}).text = data["Item_Group"]
status = ET.SubElement(bor_header, "ItemStatus")
timeperiod = ET.SubElement(status, "TimePeriod")
#ET.SubElement(timeperiod, "StartDateTime").text = now
ET.SubElement(timeperiod, "StartDateTime").text = iso_8601_format
ET.SubElement(status, "Code", {
    "listID": "Item Status",
    "sequence": "0"} ).text = "Open"
ET.SubElement(status, "ArchiveIndicator").text ="false"
ET.SubElement(bor_header, "BaseUOMCode").text = data["Unit"].upper()

#User Area
user_area = ET.SubElement(bor_header, "UserArea")

#Set output-variable
output_bod = ET.tostring(root, encoding="utf-8").decode("utf-8")

print(output_bod)