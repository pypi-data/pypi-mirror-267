
from hdl_pi_if.hdl_services import HdlServices
from .hdl_services_dpi import HdlServicesDpi

services = None



def dpi_init(scope):
    global services

    services = HdlServicesDpi(scope)
    HdlServices.registerServices(services)
