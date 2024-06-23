from schemas.email_structure import EmailScaffold

class EMAIL_AGENT_FUNCTIONS:
    Email_Task = [
        {
            "name": "Email_Creation",
            "description": "Create an Email for the client",
            "parameters": EmailScaffold.schema()
        },
    ]
