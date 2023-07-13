
new_name = "SINC_R3_L"
#new_name = "SINC_R3_R"
import storage
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = new_name
storage.remount("/", readonly=True)