#TODO: fill with data flow params
company = "4000"
tenant = "L567NQT482F74MTX_TST"
site = "S_STA001"

# TODO: remove example and use data flow params to set input_document
input_document = """
{
    "Import": "IH",
    "Product": "151.004.757",
    "Description": "STRAP CARRYING PENTHEON",
    "Project": "PRJ00123",
    "BOM_Quantity": "1",
    "Unit": "pcs",
    "Item_Group": "000004",
    "Item_Type": "M",
    "Revision": "001",
    "Effective_Date": "020925",
    "Material": "151.002.109",
    "Length": "15",
    "Net_Quantity": "1"
}"""

import xml.etree.ElementTree as ET
import json
from datetime import datetime

data = json.loads(input_document)

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
root = ET.Element("ProcessBillOfResources", {
    "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
})

application_area = ET.SubElement(root, "ApplicationArea")
sender = ET.SubElement(application_area, "Sender")
ET.SubElement(sender, "LogicalID").text = "lid://infor.ln.ln01/" + company
ET.SubElement(sender, "ComponentID").text = "erp"
ET.SubElement(sender, "ConfirmationCode").text = "OnError"
ET.SubElement(application_area, "CreationDateTime").text = now
#TODO: fill BODID with values based on best practices
ET.SubElement(application_area, "BODID").text = "infor-nid:" + tenant + ":" + company + ":" + data["Product"] + "?BillOfResources&verb=Process"

data_area = ET.SubElement(root, "DataArea")
process = ET.SubElement(data_area, "Process")
ET.SubElement(process, "TenantID").text = tenant
ET.SubElement(process, "AccountingEntityID").text = company
ET.SubElement(process, "LocationID")
action_criteria = ET.SubElement(process, "ActionCriteria")
ET.SubElement(action_criteria, "ActionExpression", {"actionCode": "Replace"})

bor = ET.SubElement(data_area, "BillOfResources")
bor_header = ET.SubElement(bor, "BillOfResourcesHeader")
doc_id = ET.SubElement(bor_header, "DocumentID")
ET.SubElement(doc_id, "ID", {
    "accountingEntity": company,
    "lid": "lid://infor.ln.ln01/" + company,
    "variationID": data["Revision"]
}).text = data["Project"] + data["Product"] 
ET.SubElement(doc_id, "RevisionID").text = data["Revision"]
doc_id = ET.SubElement(bor_header, "ProjectReference")
ET.SubElement(doc_id, "ID").text = data["Project"]
doc_id = ET.SubElement(bor_header, "ProjectReferenceID")
ET.SubElement(doc_id, "ID").text = data["Project"]
status = ET.SubElement(bor_header, "Status")
ET.SubElement(status, "Code").text = "Open"
#ET.SubElement(bor_header, "EffectiveDateTime").text = now
ET.SubElement(bor_header, "EffectiveDateTime").text = iso_8601_format
ET.SubElement(bor_header, "RunSizeBaseUOMQuantity").text = data["BOM_Quantity"]

user_area = ET.SubElement(bor_header, "UserArea")
prop1 = ET.SubElement(user_area, "Property")
ET.SubElement(prop1, "NameValue", {
    "name": "ln.BODName",
    "type": "StringType"
}).text = "BillOfResourcesReceivedPBOMBOD"

operations = ET.SubElement(bor, "Operations")
ET.SubElement(operations, "ID").text = "10"
status_op = ET.SubElement(operations, "Status")
ET.SubElement(status_op, "Code").text = "Open"

consumed_item = ET.SubElement(operations, "ConsumedItem")
item_id = ET.SubElement(consumed_item, "ItemID")
ET.SubElement(item_id, "ID").text = data["Material"]
ET.SubElement(consumed_item, "BaseUOMQuantity", {"unitCode": data["Unit"].upper()}).text = data["Net_Quantity"]
ET.SubElement(consumed_item, "LineNumber").text = "10"
etp = ET.SubElement(consumed_item, "EffectiveTimePeriod")
ET.SubElement(etp, "StartDateTime").text = iso_8601_format
status_ci = ET.SubElement(consumed_item, "Status")
ET.SubElement(status_ci, "Code").text = "Open"
ET.SubElement(consumed_item, "Note").text = "DUMMYNOTE"

ua_ci = ET.SubElement(consumed_item, "UserArea")
p1 = ET.SubElement(ua_ci, "Property")
ET.SubElement(p1, "NameValue", {"name": "ln.UseUpItem"}).text = data["Material"]
p2 = ET.SubElement(ua_ci, "Property")
ET.SubElement(p2, "NameValue", {"name": "ln.PhantomIndicator"}).text = "No"
ET.SubElement(p2, "NameValue", {"name": "ln.Lenght"}).text = data["Length"]

output_bod = ET.tostring(root, encoding="utf-8").decode("utf-8")

print(output_bod)