from network.tspiot import RequestRegistrationTSPIOT_DTO, TspiotSetup



data = RequestRegistrationTSPIOT_DTO(
    id="00106327428745",
    kktSerial="00106327428745",
    fnSerial="9999078902018941",
    kktInn="9717169631",
)

tspiot = TspiotSetup()
result = tspiot.register_tspiot(data)
print(result)
# print(result.status_code)
# print(result.json())