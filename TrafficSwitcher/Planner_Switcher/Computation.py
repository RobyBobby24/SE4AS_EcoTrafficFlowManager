import requests
import time
from DbManager import DbManager

host = "configuration_module2"
#host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    _prediction: dict
    _early_turn_on_time: int
    _traffic_switcher_groups: dict
    _traffic_switcher_status: dict
    _traffic_switcher_turn_on_time: dict
    _turn_on_time: int
    _busy: bool


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            cls.instance._traffic_switcher_groups = requests.get(url + "traffic_switcher_groups").json()
            cls.instance._turn_on_time = requests.get(url + "data/turn_on_time").json()["data"]
            cls.instance._early_turn_on_time = requests.get(url + "data/early_turn_on_time").json()["data"]
            cls.instance._traffic_switcher_status = {switcher: False for switcher, _ in cls.instance._traffic_switcher_groups.items()}
            cls.instance._traffic_switcher_turn_on_time = {switcher: -1 for switcher, _ in cls.instance._traffic_switcher_groups.items()}
            cls.instance._prediction = {}
            cls.instance._busy = False
        return cls.instance

    # def send_msg_to_switcher(self, traffic_switcher_id,  data):
        # DbManager().store_data_tag("Traffic Switcher Status", traffic_switcher_id, data)

    def get_switcher(self,cross_road, tl_id):
        for switcher, crossRoad_dict in self._traffic_switcher_groups.items():
            for crossRoad, traffic_lights in crossRoad_dict.items():
                if int(tl_id) in traffic_lights and cross_road == crossRoad:
                    return switcher
        raise ValueError("the traffic_light do not exist")

    def check_status(self, traffic_switcher_id):
        return self._traffic_switcher_status[traffic_switcher_id] and \
               time.time() - self._traffic_switcher_turn_on_time[traffic_switcher_id] > self._turn_on_time 
    # check se switcher acceso e se è passato il tempo di accensione

    def set_status(self, traffic_switcher_id, status):
        if status and \
            traffic_switcher_id in self._traffic_switcher_status and \
                self._traffic_switcher_status[traffic_switcher_id] == False:
            
            self._traffic_switcher_turn_on_time[traffic_switcher_id] = time.time()
        self._traffic_switcher_status[traffic_switcher_id] = status
        DbManager().store_data_tag("Traffic Switcher Status", traffic_switcher_id, str(status))


    def set_prediction(self, traffic_switcher_id, prediction_time):
        self._prediction[traffic_switcher_id] = prediction_time

    def get_predictions(self):
        return self._prediction

    def get_early_turn_on_time(self):
        return self._early_turn_on_time

    def get_busy(self):
        return self._busy

    def set_busy(self, busy):
        self._busy = busy






