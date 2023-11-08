import os
from pathlib import Path
import uuid

from edutap.models_apple.models import Barcode, BarcodeFormat, Coupon, Field, Pass, StoreCard

from dotenv import load_dotenv

load_dotenv()

cwd = Path(__file__).parent
data = cwd / "data"
jsons = data / "jsons"
resources = data / "resources"
certs = data / "certs"
password_file = certs / "password.txt"
cert_file = certs / "certificate.pem"
key_file = certs / "private.key"
wwdr_file = certs / "wwdr_certificate.pem"
passes = data / "passes"

passtype_identifier = os.environ.get("APPLE_PASSTYPE_IDENTIFIER")
team_identifier = os.environ.get("APPLE_TEAM_IDENTIFIER")

def create_shell_pass(barcodeFormat=BarcodeFormat.CODE128, passTypeIdentifier="Pass Type ID", teamIdentifier="Team Identifier"):
    cardInfo = StoreCard()
    cardInfo.addPrimaryField("name", "Jähn Doe", "Name")
    stdBarcode = Barcode(
        message="test barcode", format=barcodeFormat, altText="alternate text"
    )
    passfile = Pass(
        storeCard=cardInfo,
        organizationName="Org Name",
        passTypeIdentifier=passTypeIdentifier,
        teamIdentifier=teamIdentifier,
        # serialNumber="1234567",
        description="A Sample Pass"
    )
    passfile.barcode = stdBarcode
    return passfile

def create_shell_pass_loyalty(barcodeFormat=BarcodeFormat.CODE128, passTypeIdentifier="Pass Type ID", teamIdentifier="Team Identifier"):
    cardInfo = Coupon()
    cardInfo.addPrimaryField("name", "Jähn Doe", "Name")
    stdBarcode = Barcode(
        message="test barcode", format=barcodeFormat, altText="alternate text"
    )
    sn = uuid.uuid4().hex
    passfile = Pass(
        coupon=cardInfo,
        organizationName="eduTAP",
        passTypeIdentifier=passTypeIdentifier,
        teamIdentifier=teamIdentifier,
        serialNumber=sn,
        description="edutap Sample Pass"
    )
    
    # passfile.passInformation.primaryFields.append(
    #     Field(key="balance", label="Balance", value="100", currencyCode="EUR")
    # )
    # passfile.passInformation.secondaryFields.append(
    #     Field(key="points", label="Points", value="101")
    # )
    # passfile.passInformation.backFields.append(
    #     Field(key="terms", label="Terms", value="Terms and Conditions")
    # )
        
    passfile.barcode = stdBarcode
    return passfile
