from unittest import TestCase, skip
import json
import shapely
from shapely import Polygon, Point, Geometry
from shapely.ops import transform as sh_transform
from pyproj import Transformer
import os

import footprint_facility


#############################################################################
# Private Utilities to manipulate input test Footprint file
# - load
# - retrieve longitude/Latitude list according to the input
# - build shapely geometry
#############################################################################
def _load_samples():
    path = os.path.join(os.path.dirname(__file__),
                        'samples', 'footprints_basic.json')
    with open(path) as f:
        return json.load(f)['footprint']


def _split(txt, seps):
    """
    Split with list of separators
    """
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def get_odd_values(fp):
    # [1::2] odd indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[1::2]]


def get_even_values(fp):
    # [::2] even indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[::2]]


def get_longitudes(fp):
    func = get_even_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[1][:3:] == 'lon':
            func = get_odd_values
    return func(fp)


# Extract latitude coord list
def get_latitudes(fp):
    func = get_odd_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[0][:3:] == 'lat':
            func = get_even_values
    return func(fp)


def fp_to_geometry(footprint) -> Geometry:
    lon = get_longitudes(footprint)
    lat = get_latitudes(footprint)
    return Polygon([Point(xy) for xy in zip(lon, lat)])


def disk_on_globe(lon, lat, radius, func=None):
    """Generate a shapely.Polygon object representing a disk on the
    surface of the Earth, containing all points within RADIUS meters
    of latitude/longitude LAT/LON."""

    # Use local azimuth projection to manage distances in meter
    # then convert to lat/lon degrees
    local_azimuthal_projection = \
        "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon)
    lat_lon_projection = "+proj=longlat +datum=WGS84 +no_defs"

    wgs84_to_aeqd = Transformer.from_crs(lat_lon_projection,
                                         local_azimuthal_projection)
    aeqd_to_wgs84 = Transformer.from_crs(local_azimuthal_projection,
                                         lat_lon_projection)

    center = Point(float(lon), float(lat))
    point_transformed = sh_transform(wgs84_to_aeqd.transform, center)
    buffer = point_transformed.buffer(radius)
    disk = sh_transform(aeqd_to_wgs84.transform, buffer)
    if func is None:
        return disk
    else:
        return func(disk)


#############################################################################
# Test Class
#############################################################################
class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.footprints = _load_samples()
        footprint_facility.check_time(enable=True,
                                      incremental=False,
                                      summary_time=True)

    @classmethod
    def tearDownClass(cls):
        footprint_facility.show_summary()

    def setUp(self):
        pass

    def test_check_contains_pole_north(self):
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_contains_pole_south(self):
        geom = disk_on_globe(-160, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_antimeridian(self):
        geom = disk_on_globe(-179, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_no_antimeridian(self):
        geom = disk_on_globe(0, 0, 500*1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))

    def test_check_samples(self):
        """
        Pass through all the entries of the sample file that are marked as
        testable, then ensure they can be managed and reworked without failure.
        """
        for footprint in self.footprints:
            if footprint.get('testable', True):
                geom = fp_to_geometry(footprint)
                result = footprint_facility.check_cross_antimeridian(geom)
                self.assertEqual(result, footprint['antimeridian'],
                                 f"longitude singularity not properly "
                                 f"detected({footprint['name']}).")

    def test_rework_with_north_pole(self):
        """This footprint contains antimeridian and North Pole.
        """
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_with_south_pole(self):
        """This footprint contains antimeridian and South Pole.
        """
        geom = disk_on_globe(0, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_close_to_north_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the North Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_close_to_south_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the South Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, -81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_no_pole(self):
        """This footprint contains antimeridian and no pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)

    def test_rework_no_pole_no_antimeridian(self):
        """This footprint none of antimeridian and pole.
          No change of the footprint is required here.
        """
        geom = disk_on_globe(0, 0, 500 * 1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertEqual(geom, rwkd)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprint is not equivalents to input.")
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_no_antimeridian(self):
        """
        Index 15 is a S3B SLSTR footprint located over Atlantic sea.
        It does not intersect antimeridian nor pole.

        Product available in CDSE as:
        S3B_OL_2_LRR____20240311T111059_20240311T115453_20240311T134014_2634_090_308______PS2_O_NR_002
        product id: 247c85f8-a78c-4abf-9005-2171ad6d8455
        """
        index = 15
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_cross_antimeridian(self):
        """
        Index 17 is a S3B OLCI Level 1 ERR footprint located over Pacific sea.
        It intersects antimeridian but does not pass over the pole.

        Product available in CDSE as:
        S3B_OL_1_ERR____20240224T213352_20240224T221740_20240225T090115_2628_090_086______PS2_O_NT_003
        product id: 07a3fa27-787f-479c-9bb3-d267249ffad3
        """
        index = 17
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_south_pole_antimeridian_overlapping(self):
        """
        Index 18 is a very long S3A SLSTR WST footprint.
        It intersects antimeridian and passes over the South Pole.
        At the South Pole location the footprint overlaps.

        Product available in CDSE as:
        S3A_SL_2_WST____20240224T211727_20240224T225826_20240226T033733_6059_109_228______MAR_O_NT_003
        product id: 67a2b237-50dc-4967-98ce-bad0fbc04ad3
        """
        index = 18
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 10850, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    @skip("Overlapping both north and south pole is still not supported")
    def test_rework_product_north_pole_antimeridian_overlapping(self):
        """
         Footprint with overlapping on the North Pole.It also passes other
         both North and South Pole.

         The fact the footprint cross both north and south pole fails with de
         manipulation and display.

         This product is an old historical product and this use case has not
         been retrieved in CDSE.
        """
        index = 10
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 10850, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.
           index 16 footprint is S3A product type SR_2_LAN_LI from CDSE
           S3A_SR_2_LAN_LI_20240302T235923_20240303T001845_20240304T182116_1161_109_330______PS1_O_ST_005
        """
        index = 16
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiLineString)
        self.assertAlmostEqual(int(rwkd.length), 180, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_no_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.

           index 21 footprint is S3A product type SR_2_WAT from CDSE
           S3A_SR_2_WAT____20240312T172025_20240312T180447_20240314T075541_2661_110_083______MAR_O_ST_005
           cdse product id: f4b8547b-45ff-430c-839d-50a9be9c6105
        """
        index = 21
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.LineString)
        self.assertAlmostEqual(int(rwkd.length), 220, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_south_hemisphere_no_pole_antimeridian(self):
        """
        Footprint index 2 is a small simple footprint crossing antimeridan
        """
        footprint = self.footprints[2]
        geom = fp_to_geometry(footprint)
        self.assertEqual(footprint_facility.check_cross_antimeridian(geom),
                         footprint['antimeridian'])
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 18, delta=1)
        print(footprint_facility.to_geojson(rwkd))

    def testSimplifySimple(self):
        """
        Ensure an already simple polygon is not affected by the algorithm
        """
        index = 0
        geom = fp_to_geometry(self.footprints[index])

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1)

        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifyAntimeridian(self):
        """
        Ensure an already simple polygon , crossing antimeridian
        is not affected by the algorithm
        """
        index = 3
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1)
        print(rwkd)

        self.assertEqual(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def test_best_tolerance_for_single_geom(self):
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        # Surface change is limiting to 0.5% vs 100% of points could disappear
        percentage_area_change = .5
        percentage_less_points = 100
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertAlmostEqual(best_tolerance, 0.27, delta=0.01)

        # Point reduction 50% is controlling the surface (See document: 50%
        # is quickly reached)
        percentage_area_change = 1
        percentage_less_points = 50
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertAlmostEqual(best_tolerance, 0.028, delta=0.001)

    def test_best_tolerance_for_synergy(self):
        index = 22
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        # Synergy does not require tolerance: area surface never change,
        # and points are reduced from 292 to 5 with tolerance 0
        # The following parameter can not be reached  by the algorithm:
        #   This use cas is the most time-consuming
        percentage_area_change = .5
        percentage_less_points = 100
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertEqual(best_tolerance, 0)

        # No area change for synergy
        percentage_area_change = 0
        percentage_less_points = 50
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))
        print(best_tolerance)
        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertEqual(best_tolerance, 0)

    def testLongNoAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 211)
        self.assertAlmostEqual(origin_area, 2976.02, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2976.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 211)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2977.53, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3005.78, delta=0.01)
        self.assertEqual(stats['Points']['new'], 26)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3015.72, delta=0.01)
        self.assertEqual(stats['Points']['new'], 21)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3036.00, delta=0.01)
        self.assertEqual(stats['Points']['new'], 13)

    def testLongWithAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 17
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 216)
        self.assertAlmostEqual(origin_area, 2961.08, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2961.08, delta=0.01)
        self.assertEqual(stats['Points']['new'], 216)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2963.40, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2982.90, delta=0.01)
        self.assertEqual(stats['Points']['new'], 33)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2993.12, delta=0.01)
        self.assertEqual(stats['Points']['new'], 24)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3049.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 18)

    def testLongWithAntimeridianAndPole(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 18
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))
        print(footprint_facility.to_geojson(geom))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 272)
        self.assertAlmostEqual(origin_area, 10857.59, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10857.59, delta=0.01)
        self.assertEqual(stats['Points']['new'], 272)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10862.31, delta=0.01)
        self.assertEqual(stats['Points']['new'], 166)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10951.32, delta=0.01)
        self.assertEqual(stats['Points']['new'], 70)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10964.73, delta=0.01)
        self.assertEqual(stats['Points']['new'], 55)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 11229.99, delta=0.01)
        self.assertEqual(stats['Points']['new'], 39)

    def iter_among_simplify_tolerance(self, geometry, min: float, max: float,
                                      step: float):
        for tolerance in (map(lambda x: x/10000.0,
                              range(int(min*10000),
                                    int(max*10000),
                                    int(step*10000)))):
            print(self.simplify_bench(geometry, tolerance))

    @staticmethod
    def simplify_bench(geometry, tolerance=.1):
        origin_area = getattr(geometry, 'area', 0)
        origin_points_number = len(shapely.get_coordinates(geometry))

        reworked = footprint_facility.simplify(geometry, tolerance=tolerance)
        new_area = reworked.area
        variation_area = (new_area - origin_area)/origin_area
        new_points_number = len(shapely.get_coordinates(reworked))
        variation_point = ((new_points_number - origin_points_number) /
                           origin_points_number)
        return dict(value=tolerance,
                    Points=dict(
                        origin=origin_points_number,
                        new=new_points_number,
                        variation=variation_point),
                    Area=dict(
                        origin=origin_area,
                        new=new_area,
                        variation=variation_area))

    def testSimplifySynergyEurope(self):
        """
        Europe Syngery footprint has 297 point to be simplified
        :return:
        """
        index = 22
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("EUROPE" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 297)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, 0, True)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifySynergyAustralia(self):
        """
        Australia Syngery footprint has 295 point to be simplified
        :return:
        """
        index = 23
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("AUSTRALASIA" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 295)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, 0, True)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def test_print_geojson_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_geojson(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_print_wkt_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_wkt(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_S1A_WV_SLC__1SSV_no_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data.
        convex hull algortihm generates a polygon reducing points number
        from 470 to 53.
        """
        filename = ('S1A_WV_SLC__1SSV_20240408T072206_20240408T074451_053339_'
                    '0677B9_0282.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))

        geometry = shapely.MultiPolygon(polygons)
        self.assertEqual(
            len(shapely.get_coordinates(geometry)), 470)
        self.assertEqual(len(
            shapely.get_coordinates(geometry.convex_hull)), 53)

    def test_S1A_WV_SLC__1SSV_crossing_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data. This data crosses
        the antimridian.
        Convex hull algortihm generates a polygon reducing points number
        from 470 to 53. But This algorithm does not support antimeridian
        singularity, it shall be split into 2 polygons before execution.
        :return:
        """
        filename = ('S1A_WV_SLC__1SSV_20240405T060850_20240405T062741_053294_'
                    '0675E8_157E.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))
        geometry = shapely.MultiPolygon(polygons)

        east_geometry = geometry.intersection(shapely.box(-180, -90, 0, 90))
        west_geometry = geometry.intersection(shapely.box(0, -90, 180, 90))

        self.assertEqual(len(shapely.get_coordinates(geometry)), 390)
        self.assertEqual(
            len(shapely.get_coordinates(east_geometry.convex_hull)) +
            len(shapely.get_coordinates(west_geometry.convex_hull)), 49)
