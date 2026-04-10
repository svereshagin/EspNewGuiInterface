from services.tspiot import TSPIoTService

service_id="00106327428745"
kkt_serial="00106327428745"
fn_serial="9999078902018941"
kkt_inn="9717169631"

service_agent = TSPIoTService()
service_agent.create_and_registrate_service(kkt_serial,fn_serial,kkt_inn)