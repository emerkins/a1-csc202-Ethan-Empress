from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

calpoly_email_addresses = ["eiming@calpoly.edu","_@calpoly.edu"]

# Your data definitions and functions go here.
@dataclass( frozen = True )
class GlobeRect:
  lo_lat : float 
  hi_lat : float
  west_long : float
  east_long : float

@dataclass( frozen = True )
class Region:
  rect : GlobeRect
  name : str
  terrain : Literal[ "Ocean", "Mountains", "Forrest", "Other" ]

@dataclass( frozen = True )
class RegionCondition:
  region : Region
  year : int
  pop : int
  ghg_rate : float # Emissions in tons of Co2 equivalent per year
  
example_region_conditions : List[RegionCondition] = [RegionCondition( Region( GlobeRect ( 40.45, 41.05,  -74.45, -73.55), "New York City", "Other"), 2022, 19000000, 150000000), 
  RegionCondition( Region( GlobeRect ( 33.60, 34.35,  -118.90, -117.65), "Los Angeles", "Other"), 2021, 12990000, 26900000),
  RegionCondition( Region( GlobeRect ( -10, 5,  150, 160), "Western Pacific Ocean", "Ocean"), 2020, 9700000, 12000000),
  RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Mountains"), 2020, 282000, 1000000)]

#Header:
#returns a float representing Co2 emmisions from arr
def emmisions_per_capita(place : RegionCondition) -> float:
  try:
    if place.pop !=0:
      return place.ghg_rate/place.pop
  except ValueError:
    print(f"Population is must be greater than 0.")
    return 0


class Tests(unittest.TestCase):
  # Put your test cases in here.
  def test_emmisions_per_cap(self):
    self.assertAlmostEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Mountains"), 2020, 282000, 1000000)), 3.54609929078, delta=1e-9)
    self.assertAlmostEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( -10, 5,  150, 160), "Western Pacific Ocean", "Ocean"), 2020, 9700000, 12000000)), 1.237113402, delta=1e-9)
    self.assertEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( 33.60, 34.35,  -118.90, -117.65), "Los Angeles", "Other"), 2021, 0, 26900000)), None)
    self.assertAlmostEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( 40.45, 41.05,  -74.45, -73.55), "New York City", "Other"), 2022, 19000000, 150000000)), 7.894736842, delta=1e-9)
# Remember from Lab 1: this if statements checks
# whether this module (ghg.py) is the module
# being executed or whether it's just being
# imported from some other module.
if (__name__ == '__main__'):
  unittest.main()
