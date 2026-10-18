from fastapi import APIRouter

from app.modules.fleet import service
from app.modules.fleet.models import ServiceIn, logs

router = APIRouter(prefix="/fleet", tags=["Fleet & Insurance"])


@router.get("")
def index():
    return {"vehicles": service.list_vehicles(), "logs": logs.all(), "alerts": service.alerts()}


@router.post("/{vehicle_id}/service")
def service_vehicle(vehicle_id: int, body: ServiceIn):
    return service.log_service(vehicle_id, body)


@router.post("/{vehicle_id}/renew-insurance")
def renew(vehicle_id: int):
    return service.renew_insurance(vehicle_id)
