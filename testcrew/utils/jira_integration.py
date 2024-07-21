#################Current#####

from jira import JIRA
import frappe
from frappe import _
from requests.auth import HTTPBasicAuth
from console import console

class JiraApi:
    __slots__ = ('client','email','token','url','project')

    def __init__(self,owner_email) -> None:
        self.email = None
        self.token = None
        self.url =  None
        self.client = self.get_jira_client(owner_email)
        self.project = None

    
    def get_jira_client(self,owner_email):
        """ https://jira.readthedocs.io/api.html"""
        try:
                console("LLLLL").log()
                #TEEEEEEEEEEEEEEEEEEEEEEEEEEsting set my emaillllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
                owner_email = "mrehan_c@testcrew.com"
                doc_name = frappe.db.get_value('Jira Setting', {'email': owner_email}, 'name')
                if not doc_name:
                    frappe.throw(_("No Jira Setting found for the logged-in user"))

                doc = frappe.get_doc('Jira Setting', doc_name)
                # doc = frappe.get_doc('Jira Setting','Jira Setting')
                console("doc",doc).log()
                self.url ,self.token,self.email = doc.jira_server_url,doc.get_password(fieldname="token", raise_exception=False),doc.email
                return JIRA(
                server=self.url,
                basic_auth=(self.email,self.token),
                options= {'rest_api_version': '3','verify':True,"headers": {"Accept": "application/json","Content-Type": "application/json"}},
                )
        except Exception as e:
                frappe.log_error('jira_cleint_error',e)
                frappe.throw(_("Seems either Email or Token or URL  is wrong !!!"))
    
    
    @staticmethod
    def create_project_in_jira(key:str,name:str):
        """create project in jira once project inserted in frappe"""
        try:
            jApi = JiraApi()
            JiraApi.project = jApi.client.create_project(key=key,name=name,issueSecurityScheme=10002,projectCategory=10000,url=jApi.url)
            return JiraApi.project
        except Exception as e:
            frappe.log_error('project_sync_error',frappe.utils.get_traceback(e))
            return e
    
    @staticmethod
    def create_issue_in_jira(owner_email,data:dict):
        try:
            jApi = JiraApi(owner_email)
            return jApi.client.create_issue(
                dict(project=data.get('project_key'),
                    issuetype=data.get('issue_type'),
                    summary=data.get('summary'),
                    description=dict(type ="doc",version= 1,
                    content = [
                         {
                        "type": "paragraph",
                         "content": [
                        {
                        "type": "text",
                        "text": data.get('description')
                        }
                        ]}])))
        except Exception as e:
            frappe.log_error('issue_error',frappe.utils.get_traceback(e))
            return e
    

    def create_subtask(self, parent_issue_key: str, subtask_data: dict):
        """Create a subtask under a parent issue in Jira"""
        try:
            subtask = self.client.create_issue(
                fields={
                    'project': {'key': subtask_data.get('project_key')},
                    'issuetype': {'name': 'Subtask'},
                    'parent': {'key': parent_issue_key},
                    'summary': subtask_data.get('summary'),
                    'description': {
                        'type': 'doc',
                        'version': 1,
                        'content': [
                            {
                                'type': 'paragraph',
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': subtask_data.get('description')
                                    }
                                ]
                            }
                        ]
                    }
                }
            )
            return subtask
        except Exception as e:
            frappe.log_error(message=frappe.utils.get_traceback(), title='subtask_error')
            return e


    def create_issue_and_subtasks_from_sales_order(self, sales_order):
        """Create a Jira issue and subtasks from Sales Order"""
        try:
            # Create the main issue
            issue_data = {
                'project_key': 'JIT',
                'issue_type': 'Project Card',  # or 'Bug', 'Story', etc.
                'summary': sales_order.customer_name,
                'description': f'Sales Order: {sales_order.name}'
            }
            owner = sales_order.owner
            issue = self.create_issue_in_jira(owner,issue_data)
            console(f"Issue created: {issue.key}").log()
            subtask_keys = []


            # # Update Sales Order with the Jira issue key
            # sales_order.jira_issue_key = issue.key
            # sales_order.save()

            # Update Sales Order with the Jira issue key
            frappe.db.set_value('Sales Order', sales_order.name, 'jira_issue_key', issue.key)


            # Create subtasks for each item in the sales order
            for item in sales_order.items:
                subtask_data = {
                    'project_key': 'JIT',
                    'summary': item.item_code,
                    'description': f'Item: {item.item_code}, Qty: {item.qty}, Rate: {item.rate}'
                }
                subtask = self.create_subtask(issue.key, subtask_data)
                subtask_keys.append(subtask.key)
                console(f"Subtask created: {subtask.key}").log()


            frappe.msgprint(
                _("Jira issue {0} created with subtasks: {1}").format(issue.key, ", ".join(subtask_keys)),
                alert=True
            )
        except Exception as e:
            frappe.log_error(message=frappe.utils.get_traceback(), title='create_issue_subtasks_error')
            frappe.throw(_("Failed to create Jira issue or subtasks: {0}").format(str(e)))


    def delete_issue_and_subtasks(self, issue_key):
        """Delete a Jira issue and its subtasks"""
        try:
            issue = self.client.issue(issue_key)
            subtasks = issue.fields.subtasks
            # Delete subtasks first
            for subtask in subtasks:
                # self.client.delete_issue(subtask.key)
                self.client.issue(subtask.key).delete()
                console(f"Subtask deleted: {subtask.key}").log()
            # Delete the main issue
            #self.client.delete_issue(issue_key)
            issue.delete()
            console(f"Issue deleted: {issue_key}").log()
            frappe.msgprint(
                _("Jira issue {0} and its subtasks have been deleted.").format(issue_key),
                alert=True
            )
        except Exception as e:
            frappe.log_error(message=frappe.utils.get_traceback(), title='delete_issue_subtasks_error')
            frappe.throw(_("Failed to delete Jira issue or subtasks: {0}").format(str(e)))








#######################################Second Original##################

# from jira import JIRA
# import frappe
# from frappe import _
# from requests.auth import HTTPBasicAuth
# from console import console

# class JiraApi:
#     __slots__ = ('client','email','token','url','project')

#     def __init__(self) -> None:
#         self.email = None
#         self.token = None
#         self.url =  None
#         self.client = self.get_jira_client()
#         self.project = None

    
#     def get_jira_client(self):
#         """ https://jira.readthedocs.io/api.html"""
#         try:
#                 console("LLLLL").log()
#                 user_email = "mrehan_c@testcrew.com"
#                 doc_name = frappe.db.get_value('Jira Setting', {'email': user_email}, 'name')
#                 if not doc_name:
#                     frappe.throw(_("No Jira Setting found for the logged-in user"))

#                 doc = frappe.get_doc('Jira Setting', doc_name)
#                 # doc = frappe.get_doc('Jira Setting','Jira Setting')
#                 console("doc",doc).log()
#                 self.url ,self.token,self.email = doc.jira_server_url,doc.get_password(fieldname="token", raise_exception=False),doc.email
#                 return JIRA(
#                 server=self.url,
#                 basic_auth=(self.email,self.token),
#                 options= {'rest_api_version': '3','verify':True,"headers": {"Accept": "application/json","Content-Type": "application/json"}},
#                 )
#         except Exception as e:
#                 frappe.log_error('jira_cleint_error',e)
#                 frappe.throw(_("Seems either Email or Token or URL  is wrong !!!"))
    
    
#     @staticmethod
#     def create_project_in_jira(key:str,name:str):
#         """create project in jira once project inserted in frappe"""
#         try:
#             jApi = JiraApi()
#             JiraApi.project = jApi.client.create_project(key=key,name=name,issueSecurityScheme=10002,projectCategory=10000,url=jApi.url)
#             return JiraApi.project
#         except Exception as e:
#             frappe.log_error('project_sync_error',frappe.utils.get_traceback(e))
#             return e
    
#     @staticmethod
#     def create_issue_in_jira(data:dict):
#         try:
#             jApi = JiraApi()
#             return jApi.client.create_issue(
#                 dict(project=data.get('project_key'),
#                     issuetype=data.get('issue_type'),
#                     summary=data.get('summary'),
#                     description=dict(type ="doc",version= 1,
#                     content = [
#                          {
#                         "type": "paragraph",
#                          "content": [
#                         {
#                         "type": "text",
#                         "text": data.get('description')
#                         }
#                         ]}])))
#         except Exception as e:
#             frappe.log_error('issue_error',frappe.utils.get_traceback(e))
#             return e
    
















###################Origincal#####################

# from jira import JIRA
# import frappe
# from frappe import _
# from requests.auth import HTTPBasicAuth

# class JiraApi:
#     __slots__ = ('client','email','token','url','project')

#     def __init__(self) -> None:
#         self.email = None
#         self.token = None
#         self.url =  None
#         self.client = self.get_jira_client
#         self.project = None

#     @property
#     def get_jira_client(self):
#         """ https://jira.readthedocs.io/api.html"""
#         try:
#                 doc = frappe.get_doc('Jira Setting','Jira Setting')
#                 self.url ,self.token,self.email = doc.jira_server_url,doc.get_password(fieldname="token", raise_exception=False),doc.email
#                 return JIRA(
#                 server=self.url,
#                 basic_auth=(self.email,self.token),
#                 options= {'rest_api_version': '3','verify':True,"headers": {"Accept": "application/json","Content-Type": "application/json"}},
#                 )
#         except Exception as e:
#                 frappe.log_error('jira_cleint_error',e)
#                 frappe.throw(_("Seems either Email or Token or URL  is wrong !!!"))
    
    
#     @staticmethod
#     def create_project_in_jira(key:str,name:str):
#         """create project in jira once project inserted in frappe"""
#         try:
#             jApi = JiraApi()
#             JiraApi.project = jApi.client.create_project(key=key,name=name,issueSecurityScheme=10002,projectCategory=10000,url=jApi.url)
#             return JiraApi.project
#         except Exception as e:
#             frappe.log_error('project_sync_error',frappe.utils.get_traceback(e))
#             return e
    
#     @staticmethod
#     def create_issue_in_jira(data:dict):
#         try:
#             jApi = JiraApi()
#             return jApi.client.create_issue(
#                 dict(project=data.get('project_key'),
#                     issuetype=data.get('issue_type'),
#                     summary=data.get('summary'),
#                     description=dict(type ="doc",version= 1,
#                     content = [
#                          {
#                         "type": "paragraph",
#                          "content": [
#                         {
#                         "type": "text",
#                         "text": data.get('description')
#                         }
#                         ]}])))
#         except Exception as e:
#             frappe.log_error('issue_error',frappe.utils.get_traceback(e))
#             return e
    
