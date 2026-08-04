def create_pool():
    # Create a pool of mana
    pool = {
        "white": 0,
        "blue": 0,
        "black": 0,
        "red": 0,
        "green": 0,
        "colorless": 0
    }
    return pool

def add_mana(pool, color, amount):
    # Add mana to the pool
    pool[color] = pool[color] + amount
    return pool

def get_total_multiplier(doublers):
    multiplier = 1
    for doubler in doublers:
        if doubler["active"]:
            multiplier *= doubler["factor"] ** doubler["copies"]
    return multiplier
  
def tap_source(pool, source, multiplier):
  tap = source["amount"] * multiplier
  tap += 1
  add_mana(pool, source["color"], tap)
  return pool

def pay_cost(pool, amount):
    for color in ["colorless", "green", "blue"]:
      pay = min(pool[color], amount)
      pool[color] -= pay
      amount -= pay
    return pool

def pay_pips(pool, pips):
  for pip in pips:
    if pool[pip] < 1:
      return None
  for color in pips:
    pool[color] -= 1
  return pool

def can_afford(pool, generic_cost, pips):
  for pip in pips:
    if pool[pip] < 1:
      return False
  
  leftover = 0
  for color in ["colorless", "green", "blue"]:
    available = pool[color]
    if color in pips:
      available -= 1
    leftover += available
    
  return leftover >= generic_cost

def activate_kinnan(pool, generic_cost, pips):
  if not can_afford(pool, generic_cost, pips):
    return None
  else:
    pool = pay_pips(pool, pips)
    pool = pay_cost(pool, generic_cost)
    return pool

def get_reduced_cost(base_cost, reducers):
  reduced_cost = 0
  for reducer in reducers:
    if reducer["active"]:
      reduced_cost -= reducer["reduction"]
  return max(0, base_cost + reduced_cost)

def find_untapped(battlefield, exclude_name):
  for permanent in battlefield:
    if not permanent["tapped"] and permanent["name"] != exclude_name:
      return permanent
  return None

def tap_permanent(battlefield, name):
  for permanent in battlefield:
    if not permanent["tapped"] and permanent["name"] == name:
      permanent["tapped"] = True
      return True
  return False

def can_tap_with_extra(battlefield, name):
  itself_untapped = False
  for permanent in battlefield:
    if permanent["name"] == name and not permanent["tapped"]:
      itself_untapped = True
  if not itself_untapped:
    return False
  result = find_untapped(battlefield, name)
  return result is not None

def tap_with_extra(pool, battlefield, source, multiplier):
  if not can_tap_with_extra(battlefield, source["name"]):
    return None
  else:
    tap_permanent(battlefield, source["name"])
    result = find_untapped(battlefield, source["name"])
    tap_permanent(battlefield, result["name"])
    pool = tap_source(pool, source, multiplier)
    return pool
  
def is_infinite_loop(source, untap_cost, multiplier):
  one_tap = source["amount"] * multiplier + 1
  if untap_cost < one_tap:
    return True
  else:
    return False

def devoted_druid_total(source, multiplier, tap_twice = True):
  single_tap = source["amount"] * multiplier + 1
  if tap_twice:
    return single_tap * 2
  else:
    return single_tap

def add_to_battlefield(battlefield, name, permanent_type):
  battlefield.append({"name": name, "tapped": False, "type": permanent_type})
  return battlefield

def enduring_vitality_count(battlefield):
  count = 0
  for permanent in battlefield:
    if permanent["type"] == "creature" and not permanent["tapped"]:
      count += 1
  return count
