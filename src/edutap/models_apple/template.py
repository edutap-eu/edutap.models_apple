from datetime import datetime
from typing import Any
import uuid
from pydantic import BaseModel, Field
import pydantic


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
    title: str
    description: str
    creator: str  
    email: str
    timestamp: datetime = Field(default_factory=datetime.now)
    pass_type: str    # references Apple Pass Type Identifier as defined in models.@passmodel registry
    
    def create_pass(self, **kwargs):
        """create a pass from this template"""
        pass_ = PassTemplate(**self.dict())
        pass_.pass_json.update(kwargs)
        return pass_
    
class PassTemplate(PassTemplateBase):
    """bare pydantic class for validation and serialization"""
    pass_json: dict[str, Any] # TODO: define pass_json structure model for sqlalchemy
    attachments: dict[str, bytes] # TODO: define attachment structure model for sqlalchemy
