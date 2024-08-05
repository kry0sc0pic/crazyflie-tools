import json
from rich.console import Console
import time
import argparse
import os
from simple_term_menu import TerminalMenu

parser = argparse.ArgumentParser(description='Swarm')
parser.add_argument('pattern',type=str,help='Config File')
parser.add_argument('--scale',type=float,default=1.0)
parser.add_argument('--mode',type=str,default='run',choices=['verify','run'])
parser.add_argument('--scaleh',action='store_true')
parser.add_argument('--unsafe',action='store_true')
args = parser.parse_args()

print(args)

PATTERN = args.pattern
MODE = args.mode.lower()
SHOULD_CHECK = not args.unsafe
SCALE_HEIGHT = args.scaleh
SCALE = args.scale

c = Console()
c.print("MODE: "+MODE)
c.print("SCALING HEIGHT: "+('YES' if SCALE_HEIGHT else 'NO'))
c.print("SCALE: "+str(SCALE))
c.print("CHECKS: " + ('YES' if SHOULD_CHECK else 'NO'))

path = os.path.join(os.getcwd(),'patterns',PATTERN+'.json')
c.print(f"📂 Config File: {path}")
if os.path.exists(path):
    c.print("📝 Config File Found")
else:
    c.print("⛔️ Config File Not Found")
    exit(1)

with open(path,'r') as f:
    try:
        config = json.load(f)
        c.print(f"✅ [b cyan]{config['NAME']}[/b cyan] Loaded")
    except:
        c.print("⛔️ Error Loading Config File")
        exit(1)


URIS: list = config.get('URIS',None)
POSITIONS: list = config.get('POSITIONS',None)
BOUNDS = config.get('BOUNDS',None)
LOOPS: int = config.get('LOOPS',1)
LOOP_DELAY: int = config.get('STEP_DELAY',3)

if(URIS is None): 
    c.print("⛔️ URIS not found in config.json")
    exit(1)
else:
    if MODE == 'verify':
        terminal_menu = TerminalMenu(URIS)
        choice = terminal_menu.show()
        c.print(f"MODE: [green]Verification Mode[/green]")
        c.print(f"📡 Using {URIS[choice]} for verification run")
        URIS = [URIS[choice]]
    else:
        c.print("📡 Using all URIS for run")
        c.print(f"MODE: [yellow]All Drones Mode[/yellow]")

if(POSITIONS is None): 
    c.print("⛔️ POSITIONS not found in config.json")
    exit(1)
if(BOUNDS is None):
    c.print("⛔️ BOUNDS not found in config.json")
    exit(1)

if SHOULD_CHECK:
    min_x = BOUNDS['x']['min']
    max_x = BOUNDS['x']['max']
    min_y = BOUNDS['y']['min']
    max_y = BOUNDS['y']['max']
    min_z = BOUNDS['z']['min']
    max_z = BOUNDS['z']['max']

    if(len(URIS) > len(POSITIONS)):
        c.print("⛔️ You cannot have more drones than positions!")
        exit(1)
    else:
        c.print("✅ Positions >= Drones")

    for n,position in enumerate(POSITIONS):
        if(position['x'] * SCALE < min_x or position['x'] * SCALE> max_x):
            c.print(f"⛔️ X position of {n+1} out of bounds!")
            exit(1)
        if(position['y'] * SCALE < min_y or position['y'] * SCALE> max_y):
            c.print(f"⛔️ Y position of {n+1} out of bounds!")
            exit(1)
        if(position['z'] * (SCALE if SCALE_HEIGHT else 1) < min_z or position['z'] * (SCALE if SCALE_HEIGHT else 1) > max_z):
            c.print(f"⛔️ Z position of {n+1} out of bounds!")
            exit(1)
    c.print("✅ All Positions are valid")
else:
    # Warning
    c.print("⚠️ [yellow]Unsafe Mode[/yellow] is enabled")
c.print("-----------")
c.print(f"➾ {len(URIS)} Drones")
c.print(f"➾ {len(POSITIONS)} Positions")
c.print(f"➾ {LOOPS} Loops")
c.print("-----------")

N_POSITIONS = len(POSITIONS)

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory,Swarm
from procedures import hover_testing, land
from utils import wait_for_position_estimator
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.positioning.motion_commander import MotionCommander

c.print("🟣 Initializing Drivers")
try:
    cflib.crtp.init_drivers()
    c.print("✅ Drivers initialized")
except:
    c.print("⛔️ Error initializing drivers!")
    exit(1)

if N_POSITIONS > 0:
    FIRST_NEXT = (0,POSITIONS[0])
if N_POSITIONS > 1:
    SECOND_NEXT = (1,POSITIONS[1])
if N_POSITIONS > 2:
    THIRD_NEXT = (2,POSITIONS[2])
if N_POSITIONS > 3:
    FOURTH_NEXT = (3,POSITIONS[3])
if N_POSITIONS > 4:
    FIFTH_NEXT = (4,POSITIONS[4])
if N_POSITIONS > 5:
    SIXTH_NEXT = (5,POSITIONS[5])

ID_MAP = [int(x.split('/')[3]) for x in URIS]

def get_id_from_uri(uri):
    index = URIS.index(uri)
    return ID_MAP[index]

def next_point_from_uri(uri):
    index = URIS.index(uri)
    if(index == 0):
        return FIRST_NEXT
    elif(index == 1):
        return SECOND_NEXT
    elif(index == 2):
        return THIRD_NEXT
    elif(index == 3):
        return FOURTH_NEXT
    elif(index == 4):
        return FIFTH_NEXT
    elif(index == 5):
        return SIXTH_NEXT


def dynamic_loop(scf):
    link_uri = scf.cf.link_uri
    c.print(f"🚁 Dyanmic Loop -> {link_uri}")
    def set_next(pos_data):
        global FIRST_NEXT,SECOND_NEXT,THIRD_NEXT,FOURTH_NEXT,FIFTH_NEXT
        norm_id = URIS.index(link_uri)
        if(norm_id == 0):
            FIRST_NEXT = pos_data
        elif(norm_id == 1):
            SECOND_NEXT = pos_data
        elif(norm_id == 2):
            THIRD_NEXT = pos_data
        elif(norm_id == 3):
            FOURTH_NEXT = pos_data
        elif(norm_id == 4):
            FIFTH_NEXT = pos_data
        elif(norm_id == 5):
            SIXTH_NEXT = pos_data
            
        c.print(f"⏩ {link_uri} | Setting next point to {pos_id} [{pos_x} {pos_y} {pos_z}]")

    with PositionHlCommander(scf,x = 0.0,y = 0.0,z = 0.0,default_velocity=0.5,default_height = PositionHlCommander.CONTROLLER_PID) as pc:
        for i in range((LOOPS*N_POSITIONS)+1):
            pos_id,pos_meta = next_point_from_uri(scf.cf.link_uri)
            
            pos_x = pos_meta['x']*SCALE
            pos_y = pos_meta['y']*SCALE
            pos_z = pos_meta['z'] * (SCALE if SCALE_HEIGHT else 1)
            c.print(f"🛸 {link_uri} | Step {i+1} | Moving to Point {pos_id} [{pos_x} {pos_y} {pos_z}]")
            if(pos_id == N_POSITIONS-1):
                pos_id = 0
                pos_meta = POSITIONS[0]
            else:
                pos_id += 1
                pos_meta = POSITIONS[pos_id]
            set_next((pos_id,pos_meta))
            pc.go_to(pos_x,pos_y,pos_z)
            if MODE != 'verify':
                time.sleep(LOOP_DELAY)
    

        

factory = CachedCfFactory(rw_cache='./cache')
try:
    c.print("🛰  Setting Up Swarm")
    with Swarm(URIS,factory=factory) as swarm:
        c.print("🛸 Swarm Ready")
        c.print("🔄 Resetting Estimators")
        swarm.reset_estimators()
        swarm.parallel(wait_for_position_estimator)
        c.print("🚀 Starting Sequence")
        try:
            swarm.parallel_safe(dynamic_loop)
        except KeyboardInterrupt:
            c.print("🛑 Keyboard Interrupt")
            c.print("⏬ Landing Drones")
            swarm.parallel_safe(land)
            exit(0)
    
except Exception as e:
    c.print("⛔️ Error setting up swarm!")
    exit(1)
