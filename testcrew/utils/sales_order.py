#################Current#####


import frappe
from frappe import _
from frappe.utils import get_fullname
from testcrew.utils.jira_integration import JiraApi
from console import console



def create_jira_issue_on_approval(doc, method):
    console("Enter in approval method").log()
    if doc.workflow_state == 'Approved':
        console("Pass workflow state").log()
        owner_email = doc.owner
        jira_api = JiraApi(owner_email)
        jira_api.create_issue_and_subtasks_from_sales_order(doc)

    
    elif doc.workflow_state == 'Cancel':
        console("Pass cancel workflow state").log()
        owner_email = doc.owner
        jira_api = JiraApi(owner_email)
        issue_key = doc.jira_issue_key
        if issue_key:
            jira_api.delete_issue_and_subtasks(issue_key)
        else:
            frappe.msgprint(
                _("No Jira issue key found in the Sales Order."),
                alert=True
            )
