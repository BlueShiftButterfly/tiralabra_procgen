import random

class RandomPointDistributor:
    def generate_points(self, amount, min_bounds, max_bounds):
        points = []
        for i in range(amount):
            newp = random.randint(min_bounds[0], max_bounds[0]), random.randint(min_bounds[1], max_bounds[1])
            if newp not in points:
                points.append(newp)
            else:
                amount += 1
        return points
