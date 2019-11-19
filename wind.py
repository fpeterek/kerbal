import random


class Wind:
    max_wind = 10
    wind_change_threshold = 300.0

    def __init__(self):
        self.counter = 0.0
        self.wind = random.randint(-Wind.max_wind, Wind.max_wind)

    def tick(self, timedelta: float):
        self.counter += timedelta
        if random.randint(0, int(Wind.wind_change_threshold)) < self.counter:
            delta = int((10 - random.randint(1, 9)) ** 0.5)
            self.wind += random.choice([-1, 1]) * delta
            self.wind = max(self.wind, -Wind.max_wind)
            self.wind = min(self.wind, Wind.max_wind)
        return self.wind
