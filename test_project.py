import pytest
import project

def test_spawn():
    assert len(project.spawn(3))==3
def test_compass():
    player=project.Player()
    home=[0,9]
    assert project.compass(player,home)=='9 To The North'
    home=[9,9]
    assert project.compass(player,home)=='12 To The North-East'
def test_encounter():
    coordinates={'Home':[[0,0]]}
    mobs=project.Mob.spawn()
    player=project.Player()
    with pytest.raises(SystemExit):
            project.encounter(player,coordinates,*mobs)
def test_attack():
     player=project.Player()
     golem=project.Mob('Golem',10,'Quake',phy=4,pres=9)
     assert project.attack(player,golem,golem.hp,'P')==10