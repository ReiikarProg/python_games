# file that contains all portals

from dataclasses import dataclass


@dataclass()
class Portal:
    from_world: str  # current world
    origin_point: str  # name of the rect where the TP starts
    target_world: str  # name of the world after TP
    teleport_point: str  # point after TP


starting_toon = [Portal(from_world="starting_toon", origin_point="enter_home", target_world="home",
                 teleport_point="enter_home_location"),
                 Portal(from_world="starting_toon", origin_point="enter_neighbor_home", target_world="neighbor_home",
                 teleport_point="enter_neighbor_home"),
                 Portal(from_world="starting_toon", origin_point="from_starting_toon_to_road1", target_world="road1",
                 teleport_point="entering_road1")]

home = [Portal(from_world="home", origin_point="exit_home", target_world="starting_toon",
        teleport_point="starting_point")]

neighbor_home = [Portal(from_world="neighbor_home", origin_point="exit_neighbor_home", target_world="starting_toon",
                 teleport_point="exit_neighbor_home_in_toon")]

road1 = [Portal(from_world="road1", origin_point="from_road1_to_starting_toon", target_world="starting_toon",
                teleport_point="entering_starting_toon"),
         Portal(from_world="road1", origin_point="from_road1_to_center", target_world="poke_center",
                teleport_point="enter_center_location"),
         Portal(from_world="road1", origin_point="from_road1_to_shop", target_world="shop",
                teleport_point="enter_shop_location"),
         Portal(from_world="road1", origin_point="from_road1_to_forest1", target_world="forest1",
                teleport_point="enter_forest1_location"),
         Portal(from_world="road1", origin_point="from_road1_to_beach1", target_world="beach1",
                teleport_point="enter_beach1_location"),
         Portal(from_world="road1", origin_point="from_road1_to_road2", target_world="road2",
                teleport_point="from_road1_to_road2_point")]

poke_center = [Portal(from_world="poke_center", origin_point="exit_center", target_world="road1",
                      teleport_point='exit_center_location')]

shop = [Portal(from_world="shop", origin_point="exit_shop", target_world="road1",
               teleport_point='exit_shop_location')]

forest1 = [Portal(from_world="forest1", origin_point="enter_forest1", target_world="road1",
                  teleport_point="exit_forest1_location")]

beach1 = [Portal(from_world="beach1", origin_point="enter_beach1", target_world="road1",
                 teleport_point="exit_beach1_location")]

road2 = [Portal(from_world="road2", origin_point="from_road2_to_road1", target_world="road1",
                teleport_point="from_road2_to_road1_point"),
         Portal(from_world="road2", origin_point="from_road2_to_random_house", target_world="random_house",
                teleport_point="from_road2_to_random_house_point"),
         Portal(from_world="road2", origin_point="from_road2_to_starfall", target_world="starfall",
                teleport_point="from_road2_to_starfall_point")]

random_house = [Portal(from_world='random_house', origin_point='from_random_house_to_road2', target_world='road2',
                teleport_point="from_random_house_to_road2_point")]

# Portals related to the city StarFall

starfall = [Portal(from_world='starfall', origin_point='from_starfall_to_road2', target_world='road2',
                   teleport_point='from_starfall_to_road2_point'),
            Portal(from_world='starfall', origin_point='from_starfall_to_shop', target_world='starfall_shop',
                   teleport_point='from_starfall_to_shop_point'),
            Portal(from_world='starfall', origin_point='from_starfall_to_poke_center', target_world='starfall_poke_center',
                   teleport_point='from_starfall_to_poke_center_point'),
            Portal(from_world='starfall', origin_point='from_starfall_to_school', target_world='school',
                   teleport_point='from_starfall_to_school_point')]

starfall_shop = [Portal(from_world="starfall_shop", origin_point='from_shop_to_starfall', target_world='starfall',
                        teleport_point='from_shop_to_starfall_point')]

starfall_poke_center = [Portal(from_world="starfall_poke_center", origin_point='from_poke_center_to_starfall', target_world='starfall',
                        teleport_point='from_poke_center_to_starfall_point')]

school = [Portal(from_world='school', origin_point='from_school_to_starfall', target_world='starfall',
                 teleport_point='from_school_to_starfall_point')]

