import zipfile
from common import passes
from edutap.models_apple.template import PassTemplate


def test_pass_template_import():
    """test the pass template model"""
    
    passfilename = passes / "Coupon.pkpass"
    with open(passfilename, "rb") as f:
        template = PassTemplate(template_id="test", backoffice_id="test")
        template.import_passfile(f)



def test_pass_template_import1():
    """test the pass template model"""
    
    passfilename = passes / "Coupon.pkpass"
    with open(passfilename, "rb") as f:
        template = PassTemplate(template_id="test", backoffice_id="test")
        pt = PassTemplate.from_passfile(f, template_id="test", backoffice_id="test")
        assert pt.pass_json is not None
        assert "coupon" in pt.pass_json
        assert pt.pass_type == "coupon"
