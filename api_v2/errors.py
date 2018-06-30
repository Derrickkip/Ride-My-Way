"""
API error handlers
"""

errors = {
    'Bad request Error': {
        'message':"Wrong message format retry",
        'status': 400,
    },

    'Unauthorised Error': {
        'message': "You are not authorised to view this page",
        'status': 401,
    },
    'Forbidden Error': {
        'message': "You dont have permission to view this",
        'status': 403,
    }
}