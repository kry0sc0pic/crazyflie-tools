# Swarm Patterns
Let's you fly crazyflie drones in a pattern using the swarm interface & lighthouse positioning system.

### Setup
```bash
# Clone Repository
git clone https://github.com/kry0sc0pic/crazyflie-tools.git
# Open Folder
cd pattern-swarm
# (Optional) Create a virtual environment and activate it
virtualenv venv
source venv/bin/activate # <- linux/macos
venv\Scripts\activate # <- windows
# Install Dependencies
pip install -r requirements.txt
# 🎉 setup is done
```

### Creating a Pattern Configurations
All patterns configurations are stored in the `patterns` folder.

Here is a list of the parameters you can specify.

`NAME` - Name of the configuration
```json
"NAME": "Lighthouse Pentagon",
```
`URIS` - List of the URIS of the drones you want to control. The program currently only supports a maximum of six drones.
```json
"URIS": [
    "radio://0/10/2M/E7E7E7E7E7",
    "radio://0/20/2M/E7E7E7E7E7"
]
```
`LOOPS` - Number of times to repeat the pattern
```json
"LOOPS": 1
```
`POSITIONS` - Waypoints in the pattern
```json
    "POSITIONS": [
    {
        "x": 0.06,
        "y": 1.79,
        "z": 1
    },
    {
        "x": -1.33,
        "y": 0.36,
        "z": 1
    },
]
```
`BOUNDS` - The bounds of the lighthouse flying area. Used to ensure drones won't go out of bounds.
```json
"BOUNDS": {
    "x": {
        "min": -2.3,
        "max": 2.3
    
    },
    "y": {
        "min": -2.3,
        "max": 2.3
    },
    "z": {
        "min": 0,
        "max": 2
    }
},
```
`STEP_DELAY` - Delay between navigating waypoints.
```json
"STEP_DELAY": 2 
```

You can have a look at some of the existing configurations in the `patterns` as well.

***NOTE***

When the pattern starts running. The first drone in the `URIS` list will go the first position in `POSITIONS` and so on. So keep that in mind when placing your drones before launching.

## Running the Swarm
```bash
python swarm.py pentagon
```
#### Script Options and Flags
| Option | Required | Description |
| --- | --- | --- |
|`pattern` | YES | The name of the configuration file without `.json` in the `patterns` folder
| `--scale` | NO (default: `1.0`) | Scales the X & Y coordinates of the pattern to make it larger or smaller. Z can be scaled by the `--scaleh` flag |
| `--mode` | NO (default: `run`) | Use `verify` to control only one drone to check if the pattern is configured correctly. mode `run` will control all drones as normal |
| `--scaleh` | NO (default: `False`) | Applies scale the Z (altitude) coordinates |
| `--unsafe` | NO (default: `False`) | Disables out of bounds check for coordinates |

## Demonstrations
This is the `patterns/pentagon.json` configuration in action using 5 crazyflie drones.
<video src="docs/PentagonDemo.mp4" />

## License
GNU Affero General Public License v3.0
