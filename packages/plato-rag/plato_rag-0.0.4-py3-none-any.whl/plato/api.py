import requests
import re
import os 

from plato.constants import (
    BASE_FILE_UPLOAD_ENDPOINT,
    BASE_QUERY_API_ENDPOINT,
)

class OrganizationNameError(Exception):
    pass 

class APIKeyMissingError(Exception):
    pass

class LinkUploadFailed(Exception):
    pass

class FileUploadFailed(Exception):
    pass 

class NoFileSpecifiedError(Exception):
    pass 

class OnlyOneUploadType(Exception):
    pass 

class PromptCompletionError(Exception):
    pass

class FileTypeNotSupported(Exception): 
    pass

class FileNotFound(Exception):
    pass 


class Plato:
    def __init__(self, api_key=None, org_id=None):
        if api_key is None:
            self.api_key = os.environ["PLATO_API_KEY"]
        else:
            self.api_key = api_key
        
        if org_id is None:
            self.organization_id = os.environ["PLATO_ORG_ID"]
        else:
            self.organization_id = org_id

    def _is_website_link(text):
        pattern = r'^https?:\/\/[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#\[\]@!$&\'()*+,;=]+$'
        if re.match(pattern, text):
            return True
        else:
            return False


    def _link_upload(self, link):
        # Assume this is a valid website link
        files = {
            'link': (None, link),
            'id': (None, int(self.organization_id))
        }
        headers = {
            'Authorization': f"Api-Key {self.api_key}"
        }
        response = requests.post(
            url=BASE_FILE_UPLOAD_ENDPOINT,
            headers=headers,
            files=files)

        if response.status_code == 201:
            print(f"{link} uploaded successfully")
        else:
            raise LinkUploadFailed(
                f"Plato: {str(response.text)}"
            )


    def _file_upload(self, file_name):
        _, extension = os.path.splitext(file_name)
        extension = extension.lower() 
        valid_extensions = {
            '.html' : 'text/html', 
            '.md' : 'text/markdown',
            '.tex' : 'application/x-tex',
            '.docx' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        }

        ext = valid_extensions.get(extension, None)

        if ext is None:
            print("Plato: File type is not supported")
            return
            # raise FileTypeNotSupported(
            #     "Plato: File type is not supported"
            # )
        else:
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, file_name)

            if not os.path.isfile(file_path):
                raise FileNotFound(
                    "Plato: File to be uploaded not found"
                )
            with open(file_path, 'rb') as f:
                headers = {'Authorization': f"Api-Key {self.api_key}"}
                files = {
                    'file': (file_path, f, ext),
                    'extension': (None, str(extension[1:])),
                    'id': (None, int(self.organization_id))
                }
                response = requests.post(url=BASE_FILE_UPLOAD_ENDPOINT, 
                                         files=files, 
                                         headers=headers)
            
            if response.status_code == 201:
                print(f"{file_name} uploaded successfully")
            else:
                raise FileUploadFailed(
                    f"Plato: {str(response.text)}"
                )


    def upload(self, file=None, dir=None, link=None):
        if self.api_key == 'None':
            raise APIKeyMissingError(
                "Plato: Missing API key"
            )

        if file is None and dir is None and link is None:
            raise NoFileSpecifiedError

        if file is not None and dir is not None:
            raise OnlyOneUploadType

        if file:
            self._file_upload(file_name=file)
        elif link:
            self._link_upload(link=link)
        else:
            directory_path = os.path.join(os.getcwd(), dir)
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    print(f"Uploading file {file_path}")
                    self._file_upload(file_path)
                else:
                    print(f"Recursing into {file_path}")
                    self.upload(dir=file_path)
        return


    def complete(self, prompt):
        if self.api_key == 'None':
            raise APIKeyMissingError(
                "Plato: Missing API key"
            )

        headers = {
            "Authorization": f"Api-Key {self.api_key}",
        }
        request_body = {
            "prompt": prompt,
            "id": self.organization_id,
        }
        response = requests.post(
            BASE_QUERY_API_ENDPOINT,
            headers=headers,
            json=request_body,
        )

        if response.status_code == 201:
            return response.json()["response"]
        else:
            raise PromptCompletionError(
                "Plato: Prompt completion failed"
            )
