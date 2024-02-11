import random

class RandomPointDistributor:
    """
    Used to generate a set of random points in an area.
    """
    def generate_points(self, amount, min_bounds, max_bounds):
        """
        Generates a set of random points in an area.

        Args:
            amount: The number of points to generate.
            min_bounds: The point located at the south-west corner of a set of bounds encompassing the area in which to generate points.
            max_bounds: The point located at the north-east corner of a set of bounds encompassing the area in which to generate points.
        """
        points = []
        for i in range(amount):
            newp = random.randint(min_bounds[0], max_bounds[0]), random.randint(min_bounds[1], max_bounds[1])
            if newp not in points:
                points.append(newp)
            else:
                amount += 1
        return points
