from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

calpoly_email_addresses = ["eiming@calpoly.edu","ejow@calpoly.edu"]

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
  
example_region_conditions : List[RegionCondition] = [RegionCondition( Region( GlobeRect ( 40.45, 41.05,  -74.45, -73.55 ), "New York City", "Other"), 2022, 19000000, 150000000), 
  RegionCondition( Region( GlobeRect ( 33.60, 34.35,  -118.90, -117.65), "Los Angeles", "Other"), 2021, 12990000, 26900000),
  RegionCondition( Region( GlobeRect ( -10, 5,  150, 160), "Western Pacific Ocean", "Ocean"), 2020, 9700000, 12000000),
  RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Mountains"), 2020, 282000, 1000000)]

#returns the Co2 emmisions per person for a certain region
def emmisions_per_capita(place : RegionCondition) -> float:
  try:
    if place.pop !=0:
      return place.ghg_rate/place.pop
  except ValueError:
    print(f"Population is must be greater than 0.")
    return 0

#returns an the area of certain rectangular region
def area(rect : GlobeRect) -> float:
  EarthArea : float = (6371*6371*math.pi)
  width : float = abs(rect.east_long-rect.west_long)
  heightArea : float = 2*EarthArea*(math.sin(math.radians(rect.hi_lat))-math.sin(math.radians(rect.lo_lat)))
  area_sect : float = heightArea*(width/360)
  return area_sect

#returns the emmisions of a region in tons of Co2 per square kilometer
def emissions_per_square_km(region_area : RegionCondition)-> float:
    area_of_region : float = area(region_area.region.rect)
    return region_area.ghg_rate/area_of_region

# Returns the name of the region with the highest density of people per square km
def densest( regions : List[RegionCondition] ) -> str:
  highest : float = 0
  name : str = ""
  for i in regions:
    region_area : float = area( i.region.rect )
    density : float =  i.pop/region_area
    if density > highest:
      highest = density
      name = i.region.name
  return name

# Returns a new RegionCondition object that estimates the condition of the region after a certain number of years has passed
def project_condition( place : RegionCondition, years_passed : int ) -> RegionCondition:
  if place.region.terrain == "Ocean":
    return project_condition_ocean( place, years_passed)
  elif place.region.terrain == "Mountains":
    return project_condition_mountain( place, years_passed)
  elif place.region.terrain == "Forrest":
    return project_condition_forrest( place, years_passed)
  elif place.region.terrain == "Other":
    return project_condition_other( place, years_passed)
  

# Returns a new RegionCondition object that estimates the condition of the ocean region after a certain number of years has passed
def project_condition_ocean( place : RegionCondition, years_passed : int ) -> RegionCondition:
  new_pop : int = place.pop 
  new_ghg : float = place.ghg_rate
  for i in range( years_passed ):
   new_pop += round(new_pop * 0.0001)
  new_conditions : RegionCondition = replace( place, place.year + years_passed, new_pop, place.ghg_rate)
  new_ghg = new_ghg + emmisions_per_capita( new_conditions )
  new_conditions = replace( place, place.year + years_passed, new_pop, new_ghg)
  return new_conditions

# Returns a new RegionCondition object that estimates the condition of the mountain region after a certain number of years has passed
def project_condition_mountain( place : RegionCondition, years_passed : int ) -> RegionCondition:
  new_pop : int = place.pop 
  new_ghg : float = place.ghg_rate
  for i in range ( years_passed ):
   new_pop += round(new_pop * 0.0005)
  new_conditions : RegionCondition = replace( place, place.year + years_passed, new_pop, place.ghg_rate)
  new_ghg = new_ghg + emmisions_per_capita( new_conditions )
  new_conditions = replace( place, place.year + years_passed, new_pop, new_ghg)
  return new_conditions

# Returns a new RegionCondition object that estimates the condition of the forrest region after a certain number of years has passed
def project_condition_forrest( place : RegionCondition, years_passed : int ) -> RegionCondition:
  new_pop : int = place.pop 
  new_ghg : float = place.ghg_rate
  for i in range ( years_passed ):
   new_pop += round(new_pop * 0.00001)
  new_conditions : RegionCondition = replace( place, place.year + years_passed, new_pop, place.ghg_rate)
  new_ghg = new_ghg + emmisions_per_capita( new_conditions )
  new_conditions = replace( place, place.year + years_passed, new_pop, new_ghg)
  return new_conditions

# Returns a new RegionCondition object that estimates the condition of the "other" region after a certain number of years has passed
def project_condition_other( place : RegionCondition, years_passed : int ) -> RegionCondition:
  new_pop : int = place.pop 
  new_ghg : float = place.ghg_rate
  for i in range ( years_passed ):
   new_pop += round(new_pop * 0.00003)
  new_conditions : RegionCondition = replace( place, place.year + years_passed, new_pop, place.ghg_rate)
  new_ghg = new_ghg + emmisions_per_capita( new_conditions )
  new_conditions = replace( place, place.year + years_passed, new_pop, new_ghg)
  return new_conditions



# Returns a new RegionCondition object with a new year, population, and emissions
def replace( place : RegionCondition, year : int, pop : int, ghg : float ) -> RegionCondition:
  new_conditions : RegionCondition = RegionCondition( Region( GlobeRect( place.region.rect.lo_lat, place.region.rect.hi_lat, place.region.rect.west_long, place.region.rect.east_long ), place.region.name, place.region.terrain ), year, pop, ghg )
  return new_conditions

class Tests(unittest.TestCase):
  # Put your test cases in here.
  def test_emmisions_per_cap(self):
    self.assertAlmostEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Mountains"), 2020, 282000, 1000000)), 3.54609929078, delta=1e-9)
    self.assertAlmostEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( -10, 5,  150, 160), "Western Pacific Ocean", "Ocean"), 2020, 9700000, 12000000)), 1.237113402, delta=1e-9)
    self.assertEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( 33.60, 34.35,  -118.90, -117.65), "Los Angeles", "Other"), 2021, 0, 26900000)), None)
    self.assertAlmostEqual(emmisions_per_capita(RegionCondition( Region( GlobeRect ( 40.45, 41.05,  -74.45, -73.55), "New York City", "Other"), 2022, 19000000, 150000000)), 7.894736842, delta=1e-9)
 
  def test_area(self):
    self.assertAlmostEqual(area(GlobeRect(0.0,10.0,10.0,100.0)), 11071470.754972488, delta=1e-9)
    self.assertAlmostEqual(area(GlobeRect(0.0,90,0,90)), 63758058.98872353, delta=1e-9)
    self.assertAlmostEqual(area(GlobeRect(66.5,90,-179.9999,180)), 21152348.803840335, delta=1e-9)
    self.assertAlmostEqual(area(GlobeRect(0,1,0,180)), 2225463.118247001, delta=1e-9)
  
  def test_emissions_per_square_km(self):
    self.assertAlmostEqual(emissions_per_square_km(example_region_conditions[0]),29655.800092,delta=1e-7)
    self.assertAlmostEqual(emissions_per_square_km(example_region_conditions[1]),2798.41544027,delta=1e-7)
    self.assertAlmostEqual(emissions_per_square_km(example_region_conditions[2]),6.49493116779,delta=1e-7)
    self.assertAlmostEqual(emissions_per_square_km(example_region_conditions[3]),33.0743284426,delta=1e-7)

  def test_densest(self):
    self.assertEqual( densest( example_region_conditions ), "New York City")
    self.assertEqual( densest( [RegionCondition( Region( GlobeRect ( 33.60, 34.35,  -118.90, -117.65 ), "Los Angeles", "Other" ), 2021, 12990000, 26900000 ),
      RegionCondition( Region( GlobeRect ( -10, 5,  150, 160 ), "Western Pacific Ocean", "Ocean" ), 2020, 9700000, 12000000 ) ] ), "Los Angeles" )
    
  def test_project_conditions(self):
    self.assertEqual( project_condition( example_region_conditions[0], 1), RegionCondition( Region( GlobeRect ( 40.45, 41.05,  -74.45, -73.55), "New York City", "Other"), 2023, 19000570, 15000007.894) )
    self.assertEqual( project_condition( example_region_conditions[2], 2), RegionCondition( Region( GlobeRect ( -10, 5,  150, 160), "Western Pacific Ocean", "Ocean"), 2022, 9701940, 12000001.237) )
    self.assertEqual( project_condition( RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Forrest"), 2020, 282000, 1000000) , 2), RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Forrest"), 2022, 282006, 1000003.546) )
    self.assertEqual( project_condition( example_region_conditions[3], 1), RegionCondition( Region( GlobeRect ( 34.8, 36,  -122, -119.5), "Cal Poly SLO", "Mountains"), 2021, 282141, 1000003.544) )


# Remember from Lab 1: this if statements checks
# whether this module (ghg.py) is the module
# being executed or whether it's just being
# imported from some other module.
if (__name__ == '__main__'):
  unittest.main()
