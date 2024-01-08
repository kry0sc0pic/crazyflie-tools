import time
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.positioning.motion_commander import MotionCommander
from rich.console import Console

c = Console()

def land(scf):
    c.print(f"🟡 Landing -> {scf.cf.link_uri} ")
    scf.cf.high_level_commander.land(0.0,2.5)
    c.print(f"🟢 Landed -> {scf.cf.link_uri} ")

def hover_testing(scf):
    c.print(f"🟡 Launching -> {scf.cf.link_uri} ")
    scf.cf.high_level_commander.takeoff(1.0,2.0)
    c.print(f"⚪️ Hovering | 2s -> {scf.cf.link_uri} ")
    time.sleep(4)
    c.print(f"🟠 Landing -> {scf.cf.link_uri} ")
    scf.cf.high_level_commander.land(0.0,2.0)
    c.print(f"🟢 Hover Test Complete -> {scf.cf.link_uri} ")
    
def two(scf):
    c.print(f"🟡 Launching -> {scf.cf.link_uri} ")
    with MotionCommander(scf,default_height=1) as mc:
                
            c.print(f"⚪️ 2 Initial -> {scf.cf.link_uri} ")
            c.print(f"⚪️ Turning Left 90deg -> {scf.cf.link_uri} ")
            mc.turn_left(90)
            c.print(f"⚪️ Starting Turn for 6.25sec -> {scf.cf.link_uri} ")
            mc.start_circle_right(0.3)
            time.sleep(5.5)
            c.print(f"⚪️ Stopping Turn -> {scf.cf.link_uri} ")
            mc.stop()
            c.print(f"⚪️ Moving Forward 1m -> {scf.cf.link_uri} ")
            mc.forward(1.2)
            c.print(f"⚪️ Turning Left -> {scf.cf.link_uri} ")
            mc.turn_left(60)
            mc.stop()
            mc.forward(0.7)
            c.print(f"⚪️ Landing -> {scf.cf.link_uri} ")
            mc.land()
            c.print(f"🟢 Two Complete -> {scf.cf.link_uri} ")
        
            
