# utility file for parsing SVG files in a robot-friendly way.

from svgpathtools import svg2paths
import math


class WWSVG(object):

    class ListOfListsOfPoints(object):
        def __init__(self):
            self.data = []

    def __init__(self):
        self.named_paths   = {}
        self.unnamed_paths = []

    def read_file(self, filename):
        paths, attributes = svg2paths(filename)
        cc = 0
        for n in xrange(len(paths)):
            p = paths     [n]
            a = attributes[n]
            if 'id' in a:
                self.named_paths[a['id']] = p
            else:
                self.unnamed_paths.append(p)

            cc += len(p.continuous_subpaths())
        print("loaded %d paths with %d total continuous sub-paths" % (len(self.all_paths()), cc))

    def all_paths(self):
        """returns an iterator over all named and un-named paths"""
        return self.named_paths.values() + self.unnamed_paths

    def rotate(self, degrees, center=(0, 0)):
        """modifies all the contained SVG paths in-place by rotating them the given amount around the given point"""
        z = complex(center[0], center[1])

        for k in self.named_paths.keys():
            self.named_paths[k] = self.named_paths[k].rotated(degrees, z)

        for n in xrange(len(self.unnamed_paths)):
            self.unnamed_paths[n] = self.unnamed_paths[n].rotated(degrees, z)

    def scale(self, factor, center=(0, 0)):
        """modifies all the contained SVG paths in-place by scaling them the given amount around the given point"""
        z = complex(center[0], center[1])

        for k in self.named_paths.keys():
            self.named_paths[k] = self.named_paths[k].scaled(factor, factor, z)

        for n in xrange(len(self.unnamed_paths)):
            self.unnamed_paths[n] = self.unnamed_paths[n].scaled(factor, factor, z)

    def translate(self, offset):
        """modifies all the contained SVG paths in-place by translating them the given amount"""
        z = complex(offset[0], offset[1])

        for k in self.named_paths.keys():
            self.named_paths[k] = self.named_paths[k].translated(z)

        for n in xrange(len(self.unnamed_paths)):
            self.unnamed_paths[n] = self.unnamed_paths[n].translated(z)

    def center(self, on_point=(0, 0)):
        """modifies all the contained SVG paths in-place by centering the overall bounding-box on the given point"""
        xmin, xmax, ymin, ymax = self.global_bbox()
        if not (xmin and xmax and ymin and ymax):
            return None
        xcen = (xmin + xmax) * 0.5
        ycen = (ymin + ymax) * 0.5
        dx   = on_point[0] - xcen
        dy   = on_point[1] - ycen
        self.translate((dx, dy))

    def fit_to_bbox(self, new_min_x, new_max_x, new_min_y, new_max_y):
        """
        Apply a uniform scaling factor to all paths and also translation so that all paths lie within the given bounds.
        Expand or shrink as necessary so that the overall figure is tangent to the box on at least two opposite faces.
        """
        old_min_x, old_max_x, old_min_y, old_max_y = self.global_bbox()
        old_cntr_x = (old_min_x + old_max_x) * 0.5
        old_cntr_y = (old_min_y + old_max_y) * 0.5
        new_cntr_x = (new_min_x + new_max_x) * 0.5
        new_cntr_y = (new_min_y + new_max_y) * 0.5
        trans_x    = new_cntr_x - old_cntr_x
        trans_y    = new_cntr_y - old_cntr_y

        old_size_x = (old_max_x - old_min_x)
        old_size_y = (old_max_y - old_min_y)
        new_size_x = (new_max_x - new_min_x)
        new_size_y = (new_max_y - new_min_y)

        fit_ratio_x = new_size_x / old_size_x
        fit_ratio_y = new_size_y / old_size_y
        fit_ratio   = min(fit_ratio_x, fit_ratio_y)

        self.scale(fit_ratio, (old_cntr_x, old_cntr_y))
        self.translate((trans_x, trans_y))

    def global_bbox(self):
        """returns the union of all the bounding-boxes of all the paths"""
        gxmin = gymin = gxmax = gymax = None
        for p in self.all_paths():
            xmin, xmax, ymin, ymax = p.bbox()
            gxmin = xmin if gxmin is None else min(gxmin, xmin)
            gymin = ymin if gymin is None else min(gymin, ymin)
            gxmax = xmax if gxmax is None else max(gxmax, xmax)
            gymax = ymax if gymax is None else max(gymax, ymax)
        return gxmin, gxmax, gymin, gymax

    def total_length(self):
        """returns the combined length of all the paths in the overall figure"""
        ret = 0.0
        for p in self.all_paths():
            ret += p.length()

    def convert_to_list_of_lists_of_robot_points(self, units_per_point):
        """
        converts all the paths into a list of lists of points. each sub-list represents a continuous sub-path.
        Each point is a tuple of two real numbers.
        The number of points returned is determined by sampling each sub-path at a rate of units_per_point.
        This can be thought of as the distance between points. Larger values mean fewer points."""
        lolop = WWSVG.ListOfListsOfPoints()

        for p in self.all_paths():
            lolop.data.extend(WWSVG.convert_path_to_list_of_lists_of_robot_coords(p, units_per_point))

        return lolop

    @staticmethod
    def convert_path_to_list_of_lists_of_robot_coords(path, units_per_point):
        """
        converts all the sub-paths in the svg path into a list of lists of points.
        each sub-list represents a continuous sub-path.
        See convert_to_list_of_lists_of_robot_points() for more discussion.
        """
        ret = []
        for sp in path.continuous_subpaths():
            robot_points = []
            num_points = int(math.ceil(sp.length() / units_per_point)) + 1
            for n in xrange(num_points):
                t = float(n) / float(num_points - 1)
                robot_points.append(WWSVG.convert_svg_point_to_robot_point(sp.point(t)))

            ret.append(robot_points)

        return ret

    @staticmethod
    def convert_svg_point_to_robot_point(svg_point):
        return (svg_point.real, -svg_point.imag)
