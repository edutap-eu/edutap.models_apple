import os
import zipfile
import io
import pytest
import common
from common import passes
from edutap.models_apple.models import Pass
from edutap.models_apple.template import PassTemplate


def test_pass_template_import():
    """test the pass template model"""

    passfilename = passes / "Coupon.pkpass"
    with open(passfilename, "rb") as f:
        template = PassTemplate(template_id="test", backoffice_id="test")
        template.import_passfile(f)


@pytest.fixture
def imported_template():
    """test the pass template model"""

    passfilename = passes / "StoreCard.pkpass"
    with open(passfilename, "rb") as f:
        template = PassTemplate(template_id="test", backoffice_id="test")
        pt = PassTemplate.from_passfile(f, template_id="test", backoffice_id="test")
        return pt


def test_imported_template(imported_template):
    assert imported_template.pass_json is not None
    assert "storeCard" in imported_template.pass_json
    assert imported_template.pass_type == "storeCard"


@pytest.fixture
def created_pass_object(imported_template: PassTemplate):
    

    pass_ = imported_template.create_pass_object(
        # paths in the first param are relative to the root of the pass.json
        [
            {
                "path": "/barcodes/0/message",
                "op": "replace",
                "value": "new barcode message",
            },
            # we have to replace the passTypeIdentifier and teamIdentifier
            # so that the pass can be signed with our certificates
            {
                "path": "/passTypeIdentifier",
                "op": "replace",
                "value": common.passtype_identifier,
            },
            {
                "path": "/teamIdentifier",
                "op": "replace",
                "value": common.team_identifier,
            }
        ],
        # the path below is relative to the "storeCard" object in the pass.json
        [
            {
                "path": "/primaryFields/0/changeMessage",
                "op": "replace",
                "value": "new msg",
            }
        ],
    )
    
    return pass_
    
    
def test_create_pass_object(created_pass_object: Pass, tmp_path):

    assert created_pass_object is not None
    assert created_pass_object.barcode.message == "new barcode message"
    assert created_pass_object.storeCard.primaryFields[0].changeMessage == "new msg"
    
    assert "icon.png" in created_pass_object.files
    # pass_.passTypeIdentifier="pass.demo.lmu.de"
    # pass_.teamIdentifier="JG943677ZY"
   
   
@pytest.mark.integration
def test_create_pkpass_from_template(created_pass_object: Pass, tmp_path):
    """
    this test needs real certificates to be installed in data/certs/private
    see README.md for more information
    """
 
    pkpass = created_pass_object.create(
        # common.certs /  "certificate.pem",
        # common.certs /  "private.key",
        # common.certs / "wwdr_certificate.pem",
        

        common.certs / "private" / "certificate.pem",
        common.certs / "private" / "private.key",
        common.certs / "private" / "wwdr_certificate.pem",
        "",
    )
    
    pass_filename = tmp_path / "pass1.pkpass"
    with open(pass_filename, "wb") as f:
        f.write(pkpass.getvalue())
    
    os.system("open " + str(pass_filename))
    
