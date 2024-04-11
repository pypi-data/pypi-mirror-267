from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .message import Message

import requests
import logging
import uuid
import os


SERVER = "https://api-service-bofkvbi4va-ey.a.run.app"
if os.environ.get("EEZO_DEV_MODE") == "True":
    print("Running in dev mode")
    SERVER = "http://localhost:8082"

CREATE_STATE_ENDPOINT = SERVER + "/v1/create-state/"
READ_STATE_ENDPOINT = SERVER + "/v1/read-state/"
UPDATE_STATE_ENDPOINT = SERVER + "/v1/update-state/"


class StateProxy:
    def __init__(self, interface):
        self.interface = interface
        self._state = {}

    def load(self):
        logging.info("<< Loading state")
        result = self.interface.read_state(self.interface.user_id)
        if result is not None:
            self.interface.state_was_loaded = True
            self._state = result

    def __getitem__(self, key):
        return self._state.get(key, None)

    def __setitem__(self, key, value):
        self._state[key] = value

    def __delitem__(self, key):
        if key in self._state:
            del self._state[key]

    def __str__(self):
        return str(self._state)

    def __repr__(self):
        return f"StateProxy({repr(self._state)})"

    def items(self):
        return self._state.items()

    def keys(self):
        return self._state.keys()

    def values(self):
        return self._state.values()

    def __iter__(self):
        return iter(self._state)

    def __len__(self):
        return len(self._state)

    def get(self, key, default=None):
        return self._state.get(key, default)

    def save(self):
        logging.info(">> Saving state")
        if self._state and self.interface.state_was_loaded:
            self.interface.update_state(self.interface.user_id, self._state)

        if not self.interface.state_was_loaded:
            # Check if logging warning is enabled otherwise display infor
            if logging.getLogger().getEffectiveLevel() <= logging.WARNING:
                logging.warning("State was not loaded, skipping save")
            else:
                logging.info("State was not loaded, skipping save")


class Interface:
    def __init__(
        self,
        job_id: str,
        user_id: str,
        api_key: str,
        cb_send_message: callable,
        cb_invoke_connector: callable,
        cb_get_result: callable,
    ):
        self.job_id = job_id
        self.message = None
        self.user_id = user_id
        self.api_key = api_key
        self.send_message = cb_send_message
        self.invoke_connector = cb_invoke_connector
        self.get_result = cb_get_result
        self._state_proxy = StateProxy(self)
        self.state_was_loaded = False

        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def new_message(self):
        self.message = Message(notify=self.notify)
        return self.message

    def notify(self):
        if self.message is None:
            raise Exception("Please create a message first")

        message_obj = self.message.to_dict()
        self.send_message(
            {
                "message_id": message_obj["id"],
                "interface": message_obj["interface"],
            }
        )

    def _run(self, skill_id, **kwargs):
        """Invoke a skill and get the result."""
        if not skill_id:
            raise ValueError("skill_id is required")

        job_id = str(uuid.uuid4())
        self.invoke_connector(
            {
                "new_job_id": job_id,
                "skill_id": skill_id,
                "skill_payload": kwargs,
            }
        )
        return self.get_result(job_id)

    def get_thread(self, nr=5, to_string=False):
        return self._run(
            skill_id="s_get_thread", nr_of_messages=nr, to_string=to_string
        )

    def invoke(self, agent_id, **kwargs):
        return self._run(skill_id=agent_id, **kwargs)

    def __request(self, method, endpoint, payload):
        try:
            payload["api_key"] = self.api_key
            response = self.session.request(method, endpoint, json=payload)
            # Raises HTTPError for bad responses
            response.raise_for_status()
            result = response.json()
            return result.get("data", {}).get("state", {})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [401, 403]:
                raise Exception("Authorization error. Check your API key.")
            elif e.response.status_code == 404:
                if endpoint == READ_STATE_ENDPOINT or endpoint == UPDATE_STATE_ENDPOINT:
                    result = self.create_state(self.user_id, {})
                    return result.get("data", {}).get("state", {})
                else:
                    raise Exception("State not found.")
            else:
                raise Exception(f"Unexpected error: {e.response.content}")

    def create_state(self, state_id, state={}):
        return self.__request(
            "POST", CREATE_STATE_ENDPOINT, {"state_id": state_id, "state": state}
        )

    def read_state(self, state_id):
        return self.__request("POST", READ_STATE_ENDPOINT, {"state_id": state_id})

    def update_state(self, state_id, state):
        return self.__request(
            "POST", UPDATE_STATE_ENDPOINT, {"state_id": state_id, "state": state}
        )

    @property
    def state(self):
        return self._state_proxy

    def load_state(self):
        self._state_proxy.load()

    def save_state(self):
        self._state_proxy.save()
