import threading
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long
import time


class Plc(threading.Thread):
    def __init__(self, host: str):
        threading.Thread.__init__(self, daemon=True)
        self.mb = ModbusClient(host=host, debug=False, timeout=5)
        self.connected = False
        self.data = {}

    def parse_data(self, data) -> None:
        pass

    def null_data(self) -> None:
        self.data['t_prod'] = 0
        self.data['t_smoke'] = 0
        self.data['sp_max_t'] = 0
        self.data['dp'] = 0
        self.data['sp_dp_min'] = 0
        self.data['drum'] = False
        self.data['mixer'] = False
        self.data['drum_speed'] = 0
        self.data['sp_dp'] = 0
        self.data['cooler'] = 0
        self.data['sp_cooler'] = 0
        self.data['fire'] = 0
        self.data['t_box'] = 0
        self.data['plc_work_time'] = 0
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
        self.data['pid_kp'] = 0
        self.data['pid_ti'] = 0
        self.data['pid_out'] = 0

    def run(self) -> None:
        while True:
            reg_vals = self.mb.read_holding_registers(99, 106)
            if reg_vals is not None:
                self.connected = True
                self.parse_data(reg_vals)
            else:
                self.connected = False
                self.null_data()

            # print(self.data)
            time.sleep(1)
