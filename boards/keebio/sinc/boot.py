
#device_name = "SINC_R3_R"
device_name = "SINC_R3_L"
import storage
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = device_name
storage.remount("/", readonly=True)