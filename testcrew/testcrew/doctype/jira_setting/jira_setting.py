# Copyright (c) 2024, rehan and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class JiraSetting(Document):
# 	pass




import frappe
from frappe import _
from frappe.model.document import Document
from testcrew.utils.jira_integration import JiraApi
from console import console

class JiraSetting(Document):
    def validate(self):
        console("eeeeeeee").log()
        # jira_api = JiraApi()
        # jira_client = jira_api.get_jira_client()

        # issue_data = {
        #     'project_key': 'JIT',
        #     'issue_type': 'Project Card',  # or 'Bug', 'Story', etc.
        #     'summary': 'Example issue summary',
        #     'description': 'Example issue description'
        # }
        
        # try:
        #     issue = jira_api.create_issue_in_jira(issue_data)
        #     console(f"Issue created: {issue}").log()

        #      # Example data for child issues
        #     subtasks_data = [
        #         {
        #             'project_key': 'JIT',
        #             'summary': 'Subtask 1 summary',
        #             'description': 'Subtask 1 description'
        #         },
        #         {
        #             'project_key': 'JIT',
        #             'summary': 'Subtask 2 summary',
        #             'description': 'Subtask 2 description'
        #         }
        #     ]

        #     for subtask_data in subtasks_data:
        #         subtask = jira_api.create_subtask(issue.key, subtask_data)
        #         console(f"Subtask created: {subtask}").log()

        # except Exception as e:
        #     frappe.log_error(message=str(e), title='create_issue_error')
        #     frappe.throw(_("Failed to create Jira issue: {0}").format(str(e)))

        











# import frappe
# from frappe import _
# from frappe.model.document import Document
# from testcrew.utils.jira_integration import JiraApi
# from console import console

# class JiraSetting(Document):
#     def after_save(self):
#         console("After save: eeeeeeee").log()
#         jira_api = JiraApi()
#         jira_client = jira_api.get_jira_client()

#         # Example data to create an issue in Jira
#         issue_data = {
#             'project_key': 'YOUR_PROJECT_KEY',
#             'issue_type': 'Task',  # or 'Bug', 'Story', etc.
#             'summary': 'Example issue summary',
#             'description': 'Example issue description'
#         }

#         try:
#             issue = jira_api.create_issue_in_jira(issue_data)
#             console(f"Issue created: {issue}").log()

#             # Example data for child issues
#             subtasks_data = [
#                 {
#                     'project_key': 'YOUR_PROJECT_KEY',
#                     'summary': 'Subtask 1 summary',
#                     'description': 'Subtask 1 description'
#                 },
#                 {
#                     'project_key': 'YOUR_PROJECT_KEY',
#                     'summary': 'Subtask 2 summary',
#                     'description': 'Subtask 2 description'
#                 }
#             ]

#             for subtask_data in subtasks_data:
#                 subtask = jira_api.create_subtask(issue.key, subtask_data)
#                 console(f"Subtask created: {subtask}").log()

#         except Exception as e:
#             frappe.log_error(message=str(e), title='create_issue_error')
#             frappe.throw(_("Failed to create Jira issue or subtask: {0}").format(str(e)))
