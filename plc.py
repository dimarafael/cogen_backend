import threading
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long, get_bits_from_int, encode_ieee, long_list_to_word
import time


class Plc(threading.Thread):
    def __init__(self, host: str):
        threading.Thread.__init__(self, daemon=True)
        self.mb = ModbusClient(host=host, debug=False, timeout=5)
        self.connected = False
        self.data = {}
        self.null_data()
        self.alarms = {}

    def set_smoke_fan_speed(self, speed) -> bool:
        if 0 < speed <= 100:
            return self.mb.write_multiple_registers(117, long_list_to_word([encode_ieee(speed)], big_endian=False))
        else:
            return False

    def set_gaz_preset(self, preset) -> bool:
        if 0 <= preset <= 10:
            return self.mb.write_single_register(168, int(preset))
        else:
            return False

    def get_float_from_list(self, data_list: [int], number=1):
        if len(data_list) >= 2:
            return decode_ieee(word_list_to_long(val_list=data_list[:2], big_endian=False)[0])
        else:
            return None

    def parse_alarms(self, data: [int]):
        alarms_bits = get_bits_from_int(val_int=word_list_to_long(data[:2])[0], val_size=32)

    def parse_data(self, data_list) -> None:
        self.data['t_prod'] = self.get_float_from_list(data_list[3:5])
        self.data['t_smoke'] = self.get_float_from_list(data_list[5:7])
        self.data['sp_max_t'] = self.get_float_from_list(data_list[7:9])
        self.data['dp'] = self.get_float_from_list(data_list[9:11])
        self.data['sp_dp_min'] = self.get_float_from_list(data_list[11:13])
        self.data['drum'] = data_list[13] > 0
        self.data['mixer'] = data_list[14] > 0
        self.data['drum_speed'] = self.get_float_from_list(data_list[15:17])
        self.data['smoke_fan_speed'] = self.get_float_from_list(data_list[18:20])
        self.data['cooler'] = data_list[20] > 0
        self.data['cooler_speed'] = self.get_float_from_list(data_list[21:23])
        self.data['fire'] = self.get_float_from_list(data_list[23:25])
        self.data['t_box'] = self.get_float_from_list(data_list[28:30])
        self.data['plc_work_time'] = word_list_to_long(data_list[40:42])[0]
        self.data['ror'] = self.get_float_from_list(data_list[45:47])
        self.data['gaz_start'] = self.get_float_from_list(data_list[47:49])
        self.data['gaz1'] = self.get_float_from_list(data_list[49:51])
        self.data['gaz2'] = self.get_float_from_list(data_list[51:53])
        self.data['gaz3'] = self.get_float_from_list(data_list[53:55])
        self.data['gaz4'] = self.get_float_from_list(data_list[55:57])
        self.data['gaz5'] = self.get_float_from_list(data_list[57:59])
        self.data['gaz6'] = self.get_float_from_list(data_list[59:61])
        self.data['gaz7'] = self.get_float_from_list(data_list[61:63])
        self.data['gaz8'] = self.get_float_from_list(data_list[63:65])
        self.data['gaz9'] = self.get_float_from_list(data_list[65:67])
        self.data['gaz10'] = self.get_float_from_list(data_list[67:69])
        self.data['gaz_preset'] = data_list[69]
        # self.data['pid_kp'] = self.get_float_from_list(data[100:102])
        # self.data['pid_ti'] = self.get_float_from_list(data[102:104])
        # self.data['pid_out'] = self.get_float_from_list(data[104:106])
        self.data['alarm'] = word_list_to_long(data_list[:2])[0] > 0

    def null_data(self) -> None:
        self.data['t_prod'] = 0
        self.data['t_smoke'] = 0
        self.data['sp_max_t'] = 0
        self.data['dp'] = 0
        self.data['sp_dp_min'] = 0
        self.data['drum'] = False
        self.data['mixer'] = False
        self.data['drum_speed'] = 0
        self.data['smoke_fan_speed'] = 0
        self.data['cooler'] = False
        self.data['cooler_speed'] = 0
        self.data['fire'] = 0
        self.data['t_box'] = 0
        self.data['plc_work_time'] = 0
        self.data['ror'] = 0
        self.data['gaz_start'] = 0
        self.data['gaz1'] = 0
        self.data['gaz2'] = 0
        self.data['gaz3'] = 0
        self.data['gaz4'] = 0
        self.data['gaz5'] = 0
        self.data['gaz6'] = 0
        self.data['gaz7'] = 0
        self.data['gaz8'] = 0
        self.data['gaz9'] = 0
        self.data['gaz10'] = 0
        self.data['gaz_preset'] = 0
        # self.data['pid_kp'] = 0
        # self.data['pid_ti'] = 0
        # self.data['pid_out'] = 0
        self.data['alarm'] = 0

    def run(self) -> None:
        while True:
            reg_vals = self.mb.read_holding_registers(99, 70)
            if reg_vals is not None:
                self.connected = True
                self.parse_data(reg_vals)
                self.parse_alarms(reg_vals)
            else:
                self.connected = False
                self.null_data()
            self.data['connected'] = self.connected

            # print(self.data)
            time.sleep(1)
