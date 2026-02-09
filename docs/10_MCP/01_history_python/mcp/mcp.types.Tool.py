infos

 [Tool(name='read_wiki_structure', title=None, description='Get a list of documentation topics for a GitHub repository.\n\nArgs:\n    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")', inputSchema={'properties': {'repoName': {'type': 'string'}}, 'required': ['repoName'], 'type': 'object'}, outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}, icons=None, annotations=None, meta={'_fastmcp': {'tags': []}}, execution=None), Tool(name='read_wiki_contents', title=None, description='View documentation about a GitHub repository.\n\nArgs:\n    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")', inputSchema={'properties': {'repoName': {'type': 'string'}}, 'required': ['repoName'], 'type': 'object'}, outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}, icons=None, annotations=None, meta={'_fastmcp': {'tags': []}}, execution=None), Tool(name='ask_question', title=None, description='Ask any question about a GitHub repository and get an AI-powered, context-grounded response.\n\nArgs:\n    repoName: GitHub repository or list of repositories (max 10) in owner/repo format\n    question: The question to ask about the repository', inputSchema={'properties': {'repoName': {'anyOf': [{'type': 'string'}, {'items': {'type': 'string'}, 'type': 'array'}]}, 'question': {'type': 'string'}}, 'required': ['repoName', 'question'], 'type': 'object'}, outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}, icons=None, annotations=None, meta={'_fastmcp': {'tags': []}}, execution=None), Tool(name='list_available_repos', title=None, description='List all repositories available to query with your Devin account.\nOnly available in private mode (via devin.ai endpoints).', inputSchema={'properties': {}, 'type': 'object'}, outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}, icons=None, annotations=None, meta={'_fastmcp': {'tags': []}}, execution=None)]  

info

 name='read_wiki_structure' title=None description='Get a list of documentation topics for a GitHub repository.\n\nArgs:\n    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")' inputSchema={'properties': {'repoName': {'type': 'string'}}, 'required': ['repoName'], 'type': 'object'} outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True} icons=None annotations=None meta={'_fastmcp': {'tags': []}} execution=None

info.description

 Get a list of documentation topics for a GitHub repository.

Args:
    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")

info.inputSchema

 {'properties': {'repoName': {'type': 'string'}}, 'required': ['repoName'], 'type': 'object'}

info.outputSchema

 {'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}   

info.icons

 None

info.annotations

 None

info.meta

 {'_fastmcp': {'tags': []}}

info.execution

 None

info

 name='read_wiki_contents' title=None description='View documentation about a GitHub repository.\n\nArgs:\n    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")' inputSchema={'properties': {'repoName': {'type': 'string'}}, 'required': ['repoName'], 'type': 'object'} outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True} icons=None annotations=None meta={'_fastmcp': {'tags': []}} execution=None

info.description

 View documentation about a GitHub repository.

Args:
    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")

info.inputSchema

 {'properties': {'repoName': {'type': 'string'}}, 'required': ['repoName'], 'type': 'object'}

info.outputSchema

 {'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}   

info.icons

 None

info.annotations

 None

info.meta

 {'_fastmcp': {'tags': []}}

info.execution

 None

info

 name='ask_question' title=None description='Ask any question about a GitHub repository and get an AI-powered, context-grounded response.\n\nArgs:\n    repoName: GitHub repository or list of repositories (max 10) in owner/repo format\n    question: The question to ask about the repository' inputSchema={'properties': {'repoName': {'anyOf': [{'type': 'string'}, {'items': {'type': 'string'}, 'type': 'array'}]}, 'question': {'type': 'string'}}, 'required': ['repoName', 'question'], 'type': 'object'} outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True} icons=None annotations=None meta={'_fastmcp': {'tags': []}} execution=None

info.description

 Ask any question about a GitHub repository and get an AI-powered, context-grounded response.

Args:
    repoName: GitHub repository or list of repositories (max 10) in owner/repo format
    question: The question to ask about the repository

info.inputSchema

 {'properties': {'repoName': {'anyOf': [{'type': 'string'}, {'items': {'type': 'string'}, 'type': 'array'}]}, 'question': {'type': 'string'}}, 'required': ['repoName', 'question'], 'type': 'object'}

info.outputSchema

 {'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}   

info.icons

 None

info.annotations

 None

info.meta

 {'_fastmcp': {'tags': []}}

info.execution

 None

info

 name='list_available_repos' title=None description='List all repositories available to query with your Devin account.\nOnly available in private mode (via devin.ai endpoints).' inputSchema={'properties': {}, 'type': 'object'} outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True} icons=None annotations=None meta={'_fastmcp': {'tags': []}} execution=None

info.description

 List all repositories available to query with your Devin account.
Only available in private mode (via devin.ai endpoints).

info.inputSchema

 {'properties': {}, 'type': 'object'}

info.outputSchema

 {'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}   

info.icons

 None

info.annotations

 None

info.meta

 {'_fastmcp': {'tags': []}}

info.execution

 None
