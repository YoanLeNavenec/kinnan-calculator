# Mana doublers/triplers — stack multiplicatively via get_total_multiplier()
doublers = [
    {"name": "Nyxbloom Ancient", "factor": 3, "active": False, "copies": 1},
    {"name": "Mana Reflection",  "factor": 2, "active": False, "copies": 1},
]

# Cost reducers for Kinnan's activation — used by get_reduced_cost()
reducers = [
    {"name": "Training Grounds",     "reduction": 2, "active": False},
    {"name": "Biomancer's Familiar", "reduction": 2, "active": False},
]

# Flat per-tap bonuses restricted to creature sources — used alongside tap_source()
creature_bonuses = [
    {"name": "Badgermole Cub", "color": "G", "amount": 1, "active": False, "copies": 1},
]

# Tier 1 (fixed) + Tier 2 (flexible) — plain single taps, feed into tap_source()
sources = [
    {"name": "Sol Ring",        "type": "artifact", "color": "C", "amount": 2, "flexible": False},
    {"name": "Mana Vault",      "type": "artifact", "color": "C", "amount": 3, "flexible": False},
    {"name": "Llanowar Elves",  "type": "creature", "color": "G", "amount": 1, "flexible": False},
    {"name": "Elvish Mystic",   "type": "creature", "color": "G", "amount": 1, "flexible": False},
    {"name": "Fyndhorn Elves",  "type": "creature", "color": "G", "amount": 1, "flexible": False},

    {"name": "Birds of Paradise",      "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Chrome Mox",              "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Mox Diamond",             "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Mox Opal",                "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Mox Amber",               "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Arcane Signet",           "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Fellwar Stone",           "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Talisman of Curiosity",   "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Armored Scrapgorger",     "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Ornithopter of Paradise", "type": "artifact", "color": None, "amount": 1,    "flexible": True},
    {"name": "Three Tree Rootweaver",   "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Tender Wildguide",        "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Trailtracker Scout",      "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Twitching Doll",          "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Llanowar Loamspeaker",    "type": "creature", "color": None, "amount": 1,    "flexible": True},
    {"name": "Shang-Chi, Master of Kung Fu", "type": "creature", "color": None, "amount": 2, "flexible": True},
    {"name": "Marvin, Murderous Mimic",      "type": "creature", "color": None, "amount": None, "flexible": True},
    {"name": "Priest of Titania",       "type": "creature", "color": "G",  "amount": None, "flexible": True},
    {"name": "Circle of Dreams Druid",  "type": "creature", "color": "G",  "amount": None, "flexible": True},
    {"name": "Ilysian Caryatid",        "type": "creature", "color": None, "amount": None, "flexible": True},
    {"name": "Fanatic of Rhonas",       "type": "creature", "color": "G",  "amount": None, "flexible": True},
    {"name": "Sanctum Weaver",          "type": "creature", "color": None, "amount": None, "flexible": True},
    {"name": "Bloom Tender",            "type": "creature", "color": None, "amount": None, "flexible": True},

    # Fixed, but 2 different colors at once — needs a small tap_source tweak later, not yet wired
    {"name": "Simic Signet", "type": "artifact", "colors": ["G", "U"], "amount": 1, "flexible": False},
]

# Self-untap loop rocks — paired with is_infinite_loop(source, untap_cost, multiplier)
untap_loop_sources = [
    {"name": "Basalt Monolith", "type": "artifact", "color": "C", "amount": 3, "untap_cost": 3},
    {"name": "Grim Monolith",   "type": "artifact", "color": "C", "amount": 3, "untap_cost": 4},
    # Mana Vault deliberately NOT here — its untap is a once-per-turn upkeep trigger,
    # not a repeatable activated ability, so it can't loop mid-turn. See "sources" above.
]

# Bounded 2-tap card, not an infinite loop — paired with devoted_druid_total()
devoted_druid = {"name": "Devoted Druid", "type": "creature", "color": "G", "amount": 1}

# "Tap an additional untapped permanent" cards — paired with tap_with_extra()/can_tap_with_extra()
extra_tap_sources = [
    {"name": "Citanul Stalwart", "type": "creature", "color": None, "amount": 1},
    {"name": "Jaspera Sentinel", "type": "creature", "color": None, "amount": 1},
    {"name": "Saruli Caretaker", "type": "creature", "color": None, "amount": 1},
    {"name": "Loam Dryad",       "type": "creature", "color": None, "amount": 1},
    {"name": "Gene Pollinator",  "type": "creature", "color": None, "amount": 1},
]

# Not a source at all — a toggle, paired with enduring_vitality_count(battlefield)
enduring_vitality_active = False