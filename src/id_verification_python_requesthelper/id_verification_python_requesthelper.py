import boto3
from datetime import datetime
from enum import Enum
from id_verification_python_userhelper import UserHelper
import json
import logging
from multipledispatch import dispatch
import requests


log = logging.getLogger(__name__)

class RequestHelper:
    """RequestHelper class to handle Request related operations for the Id Verification APIs
    
    Args:
        userHelper: UserHelper
        
    Properties:
        userHelper: UserHelper object
        environment: Environment to run the API Requests
        
    Returns:
        RequestHelper object  
    """
    # Constructor
    @dispatch(UserHelper)
    def __init__(self, userHelper: UserHelper) -> None:
        """Initialize the RequestHelper
        
        Parameters:
            userHelper: UserHelper
            
        Returns:
            RequestHelper object
        """
        log.debug("RequestHelper.__init__")
        self.userHelper = userHelper
        self.__apiUrl = self.__getApiUrl()
        
    @dispatch(UserHelper, str)
    def __init__(self, userHelper: UserHelper, environment: str) -> None:
        """Initialize the RequestHelper
        
        Parameters:
            userHelper: UserHelper
            
        Returns:
            RequestHelper object
        """
        self.userHelper = userHelper
        self.environment = environment
        self.__apiUrl = self.__getApiUrl()
        
    @dispatch(str, str)
    def __init__(self, username: str, password: str) -> None:
        """Initialize the RequestHelper
        
        Parameters:
            username (str): Username to authenticate the API Requests
            password (str): Password to authenticate the API Requests
            
        Returns:
            RequestHelper object
        """
        self.userHelper = UserHelper(username, password)
        self.__apiUrl = self.__getApiUrl()
    
    @dispatch(str, str, str)
    def __init__(self, username: str, password: str, environment: str) -> None:
        """Initialize the RequestHelper
        
        Parameters:
            username (str): Username to authenticate the API Requests
            password (str): Password to authenticate the API Requests
            environment (str): Environment to run the API Requests
            
        Returns:
            RequestHelper object
        """
        self.userHelper = UserHelper(username, password)
        self.environment = environment
        self.__apiUrl = self.__getApiUrl()
        
    
    # Properties
    userHelper: UserHelper
    """userHelper: UserHelper object"""
    environment:str = "Development"
    """environment: Environment to run the API Requests"""
    __apiUrl = None
    """__getApiUrl: Request API URL"""
    
    
    def __getApiUrl(self) -> str:
        """
        Get the API URL
        
        Returns:
            str: API URL
        """
        
        # Setup AWS Client
        ssmSession = None
        try:
            ssmSession = boto3.Session(profile_name='tritel')
        except Exception as ex:
            log.warning(f"Error trying to use the Tritel Profile (using Default instead): {ex}")
            ssmSession = boto3.Session()
        
        ssmClient = ssmSession.client('ssm')
        
        # Get the API URL
        apiUrl = ssmClient.get_parameter(Name=F'/id-verification/{self.environment}/request-api-url')['Parameter']['Value']
        
        return apiUrl
    
    def getBulkRequest(self, bulkRequestId: str):
        """
        Get Bulk Request
        
        Parameters:
            bulkRequestId (str): Bulk Request Id
        
        Returns:
            Bulk Request
            or 
            None if not found
        """
        headers = {'Authorization': f'Bearer {self.userHelper.getToken()}', 'accept': 'application/json', 'Content-Type': 'application/json'}
        data = f'{{"bulkRequestId": "{bulkRequestId}"}}'
        log.debug(f"RequestHelper URL: http://{self.__apiUrl}/BulkRequest/GetBulkRequestByBulkRequestId?api-version=0.1")
        log.debug(f"RequestHelper.getBulkRequest: {data}")
        response = requests.put(f'http://{self.__apiUrl}/BulkRequest/GetBulkRequestByBulkRequestId?api-version=0.1', headers=headers, data=data)
        if response.status_code == 200:
            bulkRequest: BulkRequest = BulkRequest()
            jsonResponse = response.json()
            bulkRequest.bulkRequestId = jsonResponse['bulkRequest']['bulkRequestId']
            bulkRequest.customerId = jsonResponse['bulkRequest']['customerId']
            bulkRequest.workflowId = jsonResponse['bulkRequest']['workflowId']
            bulkRequest.status = jsonResponse['bulkRequest']['status']
            bulkRequest.createdOn = jsonResponse['bulkRequest']['createdOn']
            bulkRequest.updatedOn = jsonResponse['bulkRequest']['updatedOn']
            bulkRequest.completedOn = jsonResponse['bulkRequest']['completedOn']
            bulkRequest.deletedOn = jsonResponse['bulkRequest']['deletedOn']
            return bulkRequest
        if response.status_code == 404:
            return None
        else:
            return Exception(f"Error: {response.status_code} - {response._content}")

    def createBulkRequest(self, customerId: str, workflowId: str):
        """
        Create a new Bulk Request
        
        Parameters:
            customerId (str): Customer Id
            workflowId (str): Workflow Id
        
        Returns:
            Bulk Request
            or 
            None if not found
        """
        headers = {'Authorization': f'Bearer {self.userHelper.getToken()}', 'accept': 'application/json', 'Content-Type': 'application/json'}
        data = f'{{"customerId": "{customerId}", "workflowId": "{workflowId}","status": 1}}'
        log.debug(f"RequestHelper URL: http://{self.__apiUrl}/BulkRequest/CreateBulkRequest?api-version=0.1")
        log.debug(f"RequestHelper.createBulkRequestCommand: {data}")
        response = requests.post(f'http://{self.__apiUrl}/BulkRequest/CreateBulkRequest?api-version=0.1', headers=headers, data=data)
        if response.status_code == 201:
            bulkRequest: BulkRequest = BulkRequest()
            jsonResponse = response.json()
            bulkRequest.bulkRequestId = jsonResponse['bulkRequest']['bulkRequestId']
            bulkRequest.customerId = jsonResponse['bulkRequest']['customerId']
            bulkRequest.workflowId = jsonResponse['bulkRequest']['workflowId']
            bulkRequest.status = jsonResponse['bulkRequest']['status']
            bulkRequest.createdOn = jsonResponse['bulkRequest']['createdOn']
            bulkRequest.updatedOn = jsonResponse['bulkRequest']['updatedOn']
            bulkRequest.completedOn = jsonResponse['bulkRequest']['completedOn']
            bulkRequest.deletedOn = jsonResponse['bulkRequest']['deletedOn']
            return json.dumps(bulkRequest)
        else:
            return Exception(f"Error: {response.status_code} - {response._content}")

    def getBulkRequestDataElementsByBulkRequestId(self, bulkRequestId: str):
        """
        Get Bulk Request Data Elements by Bulk Request Id
        
        Parameters:
            bulkRequestId (str): Bulk Request Id
        
        Returns:
            List of Bulk Request Data Element
            or 
            None if not found
        """
        headers = {'Authorization': f'Bearer {self.userHelper.getToken()}', 'accept': 'application/json', 'Content-Type': 'application/json'}
        data = f'{{"bulkRequestId": "{bulkRequestId}"}}'
        log.debug(f"RequestHelper URL: http://{self.__apiUrl}/BulkRequestDataElement/GetBulkRequestDataElementsByBulkRequestId?api-version=0.1")
        log.debug(f"RequestHelper.getBulkRequestDataElementsByBulkRequestId: {data}")
        response = requests.put(f'http://{self.__apiUrl}/BulkRequestDataElement/GetBulkRequestDataElementsByBulkRequestId?api-version=0.1', headers=headers, data=data)
        bulkRequestDataElements = []
        if response.status_code == 200:
            for record in response.json()['bulkRequestDataElement']:
                bulkRequestDataElement: BulkRequestDataElement = BulkRequestDataElement()
                bulkRequestDataElement.BulkRequestDataElementId = record['bulkRequestDataElementId']
                bulkRequestDataElement.BulkRequestId = record['bulkRequestId']
                bulkRequestDataElement.DataField = record['dataField']
                bulkRequestDataElement.DataValue = record['dataValue']
                bulkRequestDataElement.CreatedOn = record['createdOn']
                bulkRequestDataElement.UpdatedOn = record['updatedOn']
                bulkRequestDataElement.DeletedOn = record['deletedOn']
                bulkRequestDataElements.append(bulkRequestDataElement)
            return bulkRequestDataElements
        if response.status_code == 404:
            return None
        else:
            return Exception(f"Error: {response.status_code} - {response._content}")   
        
    def createBulkRequestDataElement (self, bulkRequestId: str, dataField: str, dataValue: str):
        """
        Create Bulk Request Data Element
        
        Parameters:
            bulkRequestId (str): Bulk Request Id
            dataField (str): Data Field
            dataValue (str): Data Value
        
        Returns:
            Bulk Request Data Element
        """
        headers = {'Authorization': f'Bearer {self.userHelper.getToken()}', 'accept': 'application/json', 'Content-Type': 'application/json'}
        data = f'{{"bulkRequestId": "{bulkRequestId}", "dataField": "{dataField}", "dataValue": "{dataValue}"}}'
        log.debug(f"RequestHelper URL: http://{self.__apiUrl}/BulkRequestDataElement/CreateBulkRequestDataElement?api-version=0.1")
        log.debug(f"RequestHelper.createBulkRequestDataElement: {data}")
        response = requests.post(f'http://{self.__apiUrl}/BulkRequestDataElement/CreateBulkRequestDataElement?api-version=0.1', headers=headers, data=data)
        if response.status_code == 201:
            bulkRequestDataElement: BulkRequestDataElement = BulkRequestDataElement()
            jsonResponse = response.json()
            bulkRequestDataElement.BulkRequestDataElementId = jsonResponse['bulkRequestDataElement']['bulkRequestDataElementId']
            bulkRequestDataElement.BulkRequestId = jsonResponse['bulkRequestDataElement']['bulkRequestId']
            bulkRequestDataElement.DataField = jsonResponse['bulkRequestDataElement']['dataField']
            bulkRequestDataElement.DataValue = jsonResponse['bulkRequestDataElement']['dataValue']
            bulkRequestDataElement.CreatedOn = jsonResponse['bulkRequestDataElement']['createdOn']
            bulkRequestDataElement.UpdatedOn = jsonResponse['bulkRequestDataElement']['updatedOn']
            bulkRequestDataElement.DeletedOn = jsonResponse['bulkRequestDataElement']['deletedOn']
            return json.dumps(bulkRequestDataElement)
        else:
            return Exception(f"Error: {response.status_code} - {response._content}")
        
    def checkBulkRequestFileExists (self, customerId: str, workflowId: str, filename: str):
        """
        Check if the Filename has already been used to create a Bulk Request for the Customer and Workflow

        Args:
            customerId (str): Customer Id
            workflowId (str): Workflow Id
            filename (str): Filename to be checked


        Returns:
            bool: whether or not the filename exists
        """
        headers = {'Authorization': f'Bearer {self.userHelper.getToken()}', 'accept': 'application/json', 'Content-Type': 'application/json'}
        data = f'{{"customerId": "{customerId}", "workflowId": "{workflowId}", "filename": "{filename}"}}'
        log.debug(f"RequestHelper URL: http://{self.__apiUrl}/BulkRequestDataElement/BulkRequestFileExists?api-version=0.2")
        log.debug(f"RequestHelper.BulkRequestFileExists: {data}")
        response = requests.put(f'http://{self.__apiUrl}/BulkRequestDataElement/BulkRequestFileExists?api-version=0.2', headers=headers, data=data)
        if response.status_code == 200:
            jsonResponse = response.json()
            reply: bool = response.json()['exists']
            return reply
        else:
            return Exception(f"Error: {response.status_code} - {response._content}")
        
        
class BulkRequestStatus(Enum):
    # <summary>The bulk request is newly created.  And has no processing started or completed on it.</summary>
    New = 1
    # <summary>The bulk request is pending.</summary>
    Pending = 2
    # <summary>The bulk request is in progress.</summary>
    InProgress = 3
    # <summary>The bulk request is completed.</summary>
    Completed = 4
    # <summary>The bulk request is failed.</summary>
    Failed = 5
    # <summary>The bulk request is cancelled.</summary>
    Cancelled = 6
    # <summary>The bulk request is archived.</summary>
    Archived = 7 
    
class BulkRequest:
    # Properties
    bulkRequestId: str
    customerId: str
    workflowId: str
    status: BulkRequestStatus
    createdOn: datetime
    updatedOn: datetime
    completedOn: datetime
    deletedOn: datetime
    
    def __str__(self) -> str:
        stringOutput = f"BulkRequestId: {self.bulkRequestId}\n"
        stringOutput += f"CustomerId: {self.customerId}\n"
        stringOutput += f"WorkflowId: {self.workflowId}\n"
        stringOutput += f"Status: {self.status}\n"
        stringOutput += f"CreatedOn: {self.createdOn}\n"
        stringOutput += f"UpdatedOn: {self.updatedOn}\n"
        stringOutput += f"CompletedOn: {self.completedOn}\n"
        stringOutput += f"DeletedOn: {self.deletedOn}\n"
        return stringOutput

class BulkRequestDataElement:
    # Properties
    BulkRequestDataElementId: str
    BulkRequestId: str
    DataField: str
    DataValue: str
    CreatedOn: datetime
    UpdatedOn: datetime
    DeletedOn: datetime
    
    def __str__(self):
        stringOutput = f"BulkRequestDataElementId: {self.BulkRequestDataElementId}\n"
        stringOutput += f"BulkRequestId: {self.BulkRequestId}\n"
        stringOutput += f"DataField: {self.DataField}\n"
        stringOutput += f"DataValue: {self.DataValue}\n"
        stringOutput += f"CreatedOn: {self.CreatedOn}\n"
        stringOutput += f"UpdatedOn: {self.UpdatedOn}\n"
        stringOutput += f"DeletedOn: {self.DeletedOn}\n"
        return stringOutput