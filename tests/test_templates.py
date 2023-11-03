import zipfile
import io
import pytest
from common import passes
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


def test_create_pass_object(imported_template: PassTemplate):
    pass_ = imported_template.create_pass_object(
        [
            {
                "path": "/barcodes/0/message",
                "op": "replace",
                "value": "new barcode message",
            }
        ],
        [],
    )
    assert pass_ is not None
    pass_.barcode.message = "new barcode message"
