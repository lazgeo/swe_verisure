# Node-RED integration

Expose Verisure actions via Home Assistant **service** nodes:

| Action | Service |
|--------|---------|
| Arm away | `my_verisure.arm_away` |
| Arm home | `my_verisure.arm_home` |
| Arm night | `my_verisure.arm_night` |
| Disarm | `my_verisure.disarm` |
| Refresh status | `my_verisure.get_status` |
| Refresh cameras | `my_verisure.refresh_camera_images` |

Pass `installation_id` in `data` JSON.

Trigger flows using **events: state changed** nodes watching Verisure entity IDs.
