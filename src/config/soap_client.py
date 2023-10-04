from zeep import Client
from .environment import variables

soap_wsdl = f"{variables['GATEWAY_BASEURL']}/service?wsdl"
soap_client = Client(soap_wsdl)
