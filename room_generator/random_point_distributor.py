import random
from room_generator.geometry import Point

class RandomPointDistributor:
    """
    Used to generate a set of random points in an area.
    """
    def generate_points(self, amount, min_bounds, max_bounds, seed : int = None, minimum_distance : float = 1):
        """
        Generates a set of random points in an area.

        Args:
            amount: The number of points to generate.
            min_bounds: The point located at the south-west corner of a set of bounds encompassing the area in which to generate points.
            max_bounds: The point located at the north-east corner of a set of bounds encompassing the area in which to generate points.
        """
        points_generated = 0
        if seed is not None:
            random.seed(seed)
        points : list[Point] = []
        for i in range(amount * 2):
            if not points_generated < amount:
                break
            newp = Point(random.randint(min_bounds[0], max_bounds[0]), random.randint(min_bounds[1], max_bounds[1]))
            if newp not in points:
                valid_point =  True
                for p in points:
                    if p.get_distance_to(newp) < minimum_distance:
                        valid_point = False
                if valid_point == False:
                    continue
                points.append(newp)
                points_generated += 1
        return points
