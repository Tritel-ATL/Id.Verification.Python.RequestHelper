# ID Verification Python Request Helper
This module contains fuctions to access the ID Verification Request APIs

## Libraries
**RequestHelper** - This library accesses the Request API

### Request Helper
This library accesses the Request API
#### Properties
- userHelper (UserHelper) - UserHelper to authentication the API requests
- environment (str) -  Environment to run the API Requests
#### Methods
##### getBulkRequest
Get Bulk Request details by the Bulk Request ID

###### Parameters: 
- bulkRequestId (str): Bulk Request Id

###### Returns:
- Bulk Request

or

- None (if not found)
##### createBulkRequest
Create a new Bulk Request

###### Parameters:
- customerId (str): Customer Id
- workflowId (str): Workflow Id

###### Returns:
- Bulk Request

##### getBulkRequestDataElementsByBulkRequestId
Get Bulk Request Data Elements by Bulk Request Id
###### Parameters: 
- bulkRequestId (str): Bulk Request Id

###### Returns:
- List of Bulk Request Data Element

or

- None (if not found)

##### createBulkRequestDataElement
Create Bulk Request Data Element

###### Parameters:
- bulkRequestId (str): Bulk Request Id
- dataField (str): Data Field
- dataValue (str): Data Value

###### Returns:
- Bulk Request Data Element


## Setup PIP to install libraries
### Powershell Windows

#### Setup the authentication
Replace the profile if needed
```powershell
$env:CODEARTIFACT_AUTH_TOKEN = aws codeartifact get-authorization-token --profile tritel --domain tritelcares --domain-owner 633259327350 --query authorizationToken --output text
```

#### Add the pip library index
```powershell
pip config set site.extra-index-url https://aws:$env:CODEARTIFACT_AUTH_TOKEN@tritelcares-633259327350.d.codeartifact.ap-southeast-1.amazonaws.com/pypi/id-verification-python-repos/simple/
```

### Linux

#### Setup the authentication
Replace the profile if needed
```bash
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --profile tritel --domain tritelcares --domain-owner 633259327350 --region ap-southeast-1 --query authorizationToken --output text`
```

#### Add the pip library index
```bash
pip config set site.extra-index-url https://aws:$env:CODEARTIFACT_AUTH_TOKEN@tritelcares-633259327350.d.codeartifact.ap-southeast-1.amazonaws.com/pypi/id-verification-python-repos/simple/
```