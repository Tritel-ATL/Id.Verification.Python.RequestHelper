import importlib
import os
from pathlib import Path
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = Path(file_dir)
parent_dir = current_dir.parent
module_dir = parent_dir / "src" / "id_verification_python_requesthelper"

print(f"File Directory: {file_dir}")
print(f"Parent Directory: {parent_dir}")
print(f"Module Directory: {module_dir}")

sys.path.append(str(module_dir))

from id_verification_python_requesthelper import RequestHelper

#idModule = importlib.import_module('id_verification_python_requesthelper', package=module_dir) 
#example_module = importlib.import_module('RequestHelper', package=module_dir)
#from ..src.id_verification_python_requesthelper.id_verification_python_requesthelper import RequestHelper
from id_verification_python_userhelper import UserHelper

userhelper: UserHelper = UserHelper("werebear73","workFl@bread73")

requesthelper: RequestHelper = RequestHelper(userhelper)

bulkRequests = requesthelper.getBulkRequest("669b7fb6-9f8c-46df-b0d6-89203f1ddd0b")

print(f"Bulk Request: {bulkRequests}")

exists = requesthelper.checkBulkRequestFileExists("f21ffc01-4485-4015-abb9-21c100c8d294","e11ffc01-4485-4015-abb9-21c100c8d200","myfile.txt")

print(f"Exists: {exists}")

bulkRequest = requesthelper.createBulkRequest("669b7fb6-9f8c-46df-b0d6-89203f1ddd0b","669b7fb6-9f8c-46df-b0d6-89203f1ddd0b")

print(f"Bulk Request: {bulkRequest}")