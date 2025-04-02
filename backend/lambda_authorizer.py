import json
import jwt
import os
from typing import Dict, Any

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Should match your backend secret

def generate_policy(principal_id: str, effect: str, resource: str, tenant_id: str) -> Dict[str, Any]:
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        },
        'context': {
            'tenant_id': tenant_id
        }
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Get the Authorization header
        auth_header = event.get('authorizationToken', '')
        if not auth_header.startswith('Bearer '):
            raise Exception('Authorization header must start with Bearer')
        
        # Extract the token
        token = auth_header.split(' ')[1]
        
        # Verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Extract tenant_id from the token
        tenant_id = payload.get('tenant_id')
        if not tenant_id:
            raise Exception('Token must include tenant_id')
        
        # Generate allow policy with tenant context
        return generate_policy(payload['sub'], 'Allow', event['methodArn'], tenant_id)
        
    except Exception as e:
        print(f'Error: {str(e)}')
        # Generate deny policy
        return generate_policy('user', 'Deny', event['methodArn'], '') 