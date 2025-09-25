import xml.etree.ElementTree as ET
import json
from datetime import datetime

#TODO: fill with data flow params
company = "4000"
tenant = "L567NQT482F74MTX_TST"
site = "S_STA001"

# TODO: remove example and use data flow params to set input_document
input_document = """
{
    "Import": "I",
    "Description": "100.000.096",
    "Searchkey1": "CHN_MINIMUM_SET_Neuswiel VDS - Gelagerd kunststof wiel",
    "Searchkey2": "",
    "Project": "1",
    "UOM": "pcs",
    "PartsListQuantity": "000002",
    "ItemGroup": "Product",
    "MI": "B",
    "Date": "150925",
    "ItemNumber": "151.002.109",
    "Length": "15",
    "Quantity": "1"
  }"""

data = json.loads(input_document)

now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

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
ET.SubElement(application_area, "BODID").text = "infor-nid:L567NQT482F74MTX_TST:4000::10000175:?BillOfResources&verb=Process"

data_area = ET.SubElement(root, "DataArea")
process = ET.SubElement(data_area, "Process")
ET.SubElement(process, "TenantID").text = tenant
ET.SubElement(process, "AccountingEntityID").text = company
ET.SubElement(process, "LocationID")
action_criteria = ET.SubElement(process, "ActionCriteria")
ET.SubElement(action_criteria, "ActionExpression", {"actionCode": "Add"})

bor = ET.SubElement(data_area, "BillOfResources")
bor_header = ET.SubElement(bor, "BillOfResourcesHeader")
doc_id = ET.SubElement(bor_header, "DocumentID")
ET.SubElement(doc_id, "ID", {
    "accountingEntity": company,
    "lid": "lid://infor.ln.ln01/" + company,
    "variationID": "1"
}).text = data["Description"]
ET.SubElement(doc_id, "RevisionID").text = "A"
status = ET.SubElement(bor_header, "Status")
ET.SubElement(status, "Code").text = "Open"
ET.SubElement(bor_header, "EffectiveDateTime").text = now
ET.SubElement(bor_header, "RunSizeBaseUOMQuantity").text = "1"

user_area = ET.SubElement(bor_header, "UserArea")
prop1 = ET.SubElement(user_area, "Property")
ET.SubElement(prop1, "NameValue", {
    "name": "ln.BODName",
    "type": "StringType"
}).text = "BillOfResourcesReceivedPBOMBOD"
prop2 = ET.SubElement(user_area, "Property")
ET.SubElement(prop2, "NameValue", {
    "name": "ln.Site",
    "type": "MasterDataReferenceType",
    "nounName": "Location",
    "accountingEntity": company
}).text = site

operations = ET.SubElement(bor, "Operations")
ET.SubElement(operations, "ID").text = "10"
status_op = ET.SubElement(operations, "Status")
ET.SubElement(status_op, "Code").text = "Open"

consumed_item = ET.SubElement(operations, "ConsumedItem")
item_id = ET.SubElement(consumed_item, "ItemID")
ET.SubElement(item_id, "ID").text = data["ItemNumber"]
ET.SubElement(consumed_item, "BaseUOMQuantity", {"unitCode": data["UOM"].upper()}).text = data["Quantity"]
#TODO: check if this is correct, I assume it is wrong but I don't know how to interpret length and lines
ET.SubElement(consumed_item, "LineNumber").text = data["Length"]
etp = ET.SubElement(consumed_item, "EffectiveTimePeriod")
ET.SubElement(etp, "StartDateTime").text = now
status_ci = ET.SubElement(consumed_item, "Status")
ET.SubElement(status_ci, "Code").text = "Open"
ET.SubElement(consumed_item, "Note").text = "LINENOTE"

ua_ci = ET.SubElement(consumed_item, "UserArea")
p1 = ET.SubElement(ua_ci, "Property")
ET.SubElement(p1, "NameValue", {"name": "ln.UseUpItem"}).text = data["ItemNumber"]
p2 = ET.SubElement(ua_ci, "Property")
ET.SubElement(p2, "NameValue", {"name": "ln.PhantomIndicator"}).text = "No"

output_document = ET.tostring(root, encoding="utf-8").decode("utf-8")