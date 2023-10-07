SUCCESSFUL_RESPONSE = {
    'statusCode': 200,
    'headers': {
        'Content-type': 'application/json'
    },
}

INVALID_DATA = {
    'statusCode': 400,
    'headers': {
        'Content-type': 'application/json'
    },
    'body': {
        'error': 'Invalid data'
    }
}

PERMISSION_DENIED = {
    'statusCode': 403,
    'headers': {
        'Content-type': 'application/json'
    },
    'body': {
        'error': 'Permission denied'
    }
}
