import os
from tpds.devices import TpdsDevices
from tpds.app.vars import get_app_ref
from .api.apis import router
from .sha10x_symm_auth_user_inputs import sha10x_symm_auth_user_inputs

TpdsDevices().add_device_info(os.path.dirname(__file__))

if get_app_ref():
    get_app_ref()._messages.register(sha10x_symm_auth_user_inputs)
