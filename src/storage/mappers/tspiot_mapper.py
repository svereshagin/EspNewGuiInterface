from dto.tspiot import TSPIoTInstanceInfoDTO


class TspiotMapper:

    @staticmethod
    def instance_info_to_dict(info: TSPIoTInstanceInfoDTO) -> dict:
        licenses = []
        if info.licenses:
            for lic in info.licenses:
                licenses.append({
                    'isActive': lic.isActive,
                    'activeTill': lic.activeTill,
                    'lastSync': lic.lastSync,
                })

        reg_data = {}
        if info.regData:
            reg_data = {
                'tspiotId': info.regData.tspiotId,
                'gismtTspiotId': info.regData.gismtTspiotId,
                'kktSerial': info.regData.kktSerial,
                'fnSerial': info.regData.fnSerial,
                'kktInn': info.regData.kktInn,
                'espToken': info.regData.espToken,
            }

        return {
            'logPath': info.logPath,
            'state': info.state,
            'clientPort': info.clientPort,
            'version': info.version,
            'licenses': licenses,
            'regData': reg_data,
        }