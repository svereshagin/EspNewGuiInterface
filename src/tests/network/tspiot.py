import time

import pytest
from dto.tspiot import TSPIoTRequestRegistration, TSPIoTRequestCreateInstance
from network.tspiot import TSPIoTNetwork

service_id="00106327428745"
kkt_serial="00106327428745"
fn_serial="9999078902018941"
kkt_inn="9717169631"



def create_and_register():
    """Тест создания сервиса и регистрации"""
    # Проверяем что переменные загружены
    assert service_id is not None, "SERVICE_ID не загружен в глобальную переменную!"
    assert kkt_serial is not None, "KKT_SERIAL не загружен!"

    register_dto = TSPIoTRequestRegistration(service_id, kkt_serial, fn_serial, kkt_inn)
    create_instance_dto = TSPIoTRequestCreateInstance(kkt_serial)

    tspiot_agent = TSPIoTNetwork()

    result = tspiot_agent.create_esm_service(create_instance_dto)
    print(f"\nCreate service result: {result}")
    assert result is not None

    tries = 0
    is_registrated = False
    while not is_registrated:
        tries += 1
        start_time = time.time()
        result_registration = tspiot_agent.register_tspiot(register_dto)
        end_time = time.time()
        print(f"⏱️ регистрация выполнена за {end_time - start_time:.4f} секунд")
        print(f"Registration result 1 try: {result_registration}")
        if not result_registration.success and result_registration.error_message == 'Превышено время ожидания ответа от оркестратора':
            result_registration = tspiot_agent.register_tspiot(register_dto)
            print(f"Registration resul 2 try: {result_registration}")
        else:
            is_registrated = True

    print(f"Registration result 3 try: {result_registration}")
    assert result_registration is not None

def instance_info():
    tspiot_agent = TSPIoTNetwork()
    result = tspiot_agent.get_instance_info(service_id)
    print(result)

def get_instances_info():
    tspiot_agent = TSPIoTNetwork()
    tspiot_agent.get_instances_info()

instance_info()
get_instances_info()
create_and_register()
