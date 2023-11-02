import base64
from datetime import datetime
import io
from typing import Any
import uuid
import zipfile
from pydantic import BaseModel, Field
import pydantic

from edutap.models_apple.models import Pass


class PassTemplateBase(BaseModel):
    """
    Contains meta information about the pass template.
    intended to be stored in a database, passes will be created off this template
    by patching the template data with the parameters defined during creation
    
    TODO: versionierung
    
    PassTemplates are stored historically, that means, every update is a creation of a new record 
        template_id stays the same, id is a new uuid, (template_id, timestamp) are unique
    
    storage should be adaptable, concrete storage in a relational database is defined in the edutap.passdata_apple service
    """
    
    id: pydantic.types.UUID4 = Field(default_factory=uuid.uuid4) # unique over whole table
    template_id: str  # uniqe name for lookup
    backoffice_id: str  # unique id for backoffice
    title: str = ""
    description: str = ""
    creator: str = ""
    email: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    pass_type: str = ""    # references Apple Pass Type Identifier as defined in models.@passmodel registry
    blob: bytes = b""  # TODO: define blob structure model for sqlalchemy
    
    def create_pass(self, **kwargs):
        """create a pass from this template"""
        ...
    
    def import_passfile(self, passfile: bytes | io.IOBase):
        """
        import a passfile into the template
        fetches pass.json and validates/parses it,
        gets all attachments and stores them in the template
        ignores all other files(manifest, signature, etc.)
        """
        ignorefiles = ["manifest.json", "signature", "manifest", "pass.json"]
        if isinstance(passfile, bytes):
            passfile = io.BytesIO(passfile)
            
        zf = zipfile.ZipFile(passfile)
        
        for filename in zf.namelist():
            if filename in ignorefiles:
                continue
            with zf.open(filename) as f:
                self.attachments[filename] = base64.b64encode(f.read()).decode("utf-8")
        
        passjson = zf.read("pass.json")

        passobject = Pass.model_validate_json(passjson)
        self.pass_type = passobject.passType
        self.pass_json = passobject.model_dump(exclude_none=True)
    
    
    @classmethod
    def from_passfile(cls, passfile: bytes | io.IOBase, template_id: str, backoffice_id: str):
        """
        constructor method to create a template from a passfile.
        sutomatically sets pass_type, pass_json and attachments
        """
        template = cls(template_id=template_id, backoffice_id=backoffice_id, pass_type="generic")
        template.import_passfile(passfile)
        
        return template
        
        
    def attachment_filenames(self):
        """return a list of all attachment filenames"""
        return self.attachments.keys()
    
    
    def get_attachment(self, filename: str) -> bytes:
        """return an attachment by filename"""
        b64str = self.attachments[filename]
        data = base64.b64decode(b64str)
        return data
        
        
class PassTemplate(PassTemplateBase):
    """bare pydantic class for validation and serialization"""
    pass_json: dict[str, Any] = Field(default_factory=dict)# TODO: define pass_json structure model for sqlalchemy
    attachments: dict[str, str] = Field(default_factory=dict)# TODO: define attachment structure model for sqlalchemy
