from src.dto.kkt import KktInfo


class KktMapper:
    @staticmethod
    def to_dict(kkt: KktInfo) -> dict:
        return {
            'kktSerial': kkt.kktSerial,
            'fnSerial': kkt.fnSerial,
            'kktInn': kkt.kktInn,
            'kktRnm': kkt.kktRnm,
            'modelName': kkt.modelName,
            'dkktVersion': kkt.dkktVersion,
            'developer': kkt.developer,
            'manufacturer': kkt.manufacturer,
            'shiftState': kkt.shiftState.value,
            'displayName': f"{kkt.kktRnm} ({kkt.kktSerial})",
            'isShiftOpen': kkt.shiftState.value
        }