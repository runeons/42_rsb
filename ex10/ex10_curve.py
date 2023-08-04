# import matplotlib.pyplot as plt

C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

class ZCurve:
    def __init__(self):
        self.y_min = self._coordinates_to_int(0, 0)
        self.y_max = self._coordinates_to_int(65535, 65535)

    def _check_param(self, p):
        if (not isinstance(p, int)) or (p < 0 or p > 65535):
            raise ValueError(f"{C_RED}Error: {C_RES}Parameter {p} must be a natural number between 0 and 65535.")

    def check_injectivity(self, x_max=65536, y_max=65536):
        print(C_YELLOW, "check_injectivity", C_RES)
        all_results = set()
        for x in range(x_max):
            for y in range(y_max):
                res = self._normalise(self._coordinates_to_int(x, y))
                if res in all_results:
                    raise ValueError(f"{C_RED}Error: {C_RES}NOT INJECTIVE {res} for {x}, {y}")
                all_results.add(res)
        print(C_YELLOW, "OK - injective", C_RES)

    ################## map ################## f(x, y) -> float

    def _normalise(self, raw_nb):
        return (raw_nb - self.y_min) / (self.y_max - self.y_min)

    def _coordinates_to_int(self, init_x, init_y):
        SHIFTS = [1, 2, 4, 8]
        MASKS = [0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF]        
        # 0x55555555 = 01010101 01010101 01010101 01010101
        # 0x33333333 = 00110011 00110011 00110011 00110011
        # 0x0F0F0F0F = 00001111 00001111 00001111 00001111
        # 0x00FF00FF = 00000000 11111111 00000000 11111111
        x = init_x  
        y = init_y
        for i in range(3, -1, -1):
            x = (x | (x << SHIFTS[i])) & MASKS[i]
            y = (y | (y << SHIFTS[i])) & MASKS[i]
        result = x | (y << 1)
        return result
    
    def map(self, x, y):
        for p in [x, y]:
            self._check_param(p)
        res = self._coordinates_to_int(x, y)
        return self._normalise(res)

    # def draw(self, x_min=0, x_max=10, y_min=0, y_max=10):
    #     print(C_YELLOW, "draw", C_RES)
    #     for p in [x_min, y_min, x_max, y_max]:
    #         self._check_param(p)
    #     if (x_min > x_max) or (y_min > y_max):
    #         raise ValueError(f"{C_RED}Error: {C_RES} x_min > x_max or y_min > y_max")
    #     all_results = set()
    #     # all_results.add(self._normalise(self._coordinates_to_int(0, 0)))
    #     for x in range(x_min, x_max + 1):
    #         for y in range(y_min, y_max + 1):
    #             res = self._normalise(self._coordinates_to_int(x, y))
    #             all_results.add(res)
    #     # all_results.add(self._normalise(self._coordinates_to_int(65535, 65535)))
    #     x_coords = list(range(len(all_results)))
    #     y_coords = list(all_results)
    #     plt.plot(x_coords, y_coords, 'b.')
    #     plt.xlabel('Itérations')
    #     plt.ylabel('f(x, y)')
    #     plt.title(f"Z Curve for x=[{x_min}, {x_max}], y=[{y_min}, {y_max}]")
    #     plt.show()

def map(x: int, y:int) -> float:
    zcurve = ZCurve()
    # zcurve.check_injectivity(x_max=10000, y_max=10000)
    return zcurve.map(x, y)

def main():
    try:
        tests = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1),
            (0, 2), (40000, 40000), (41000, 65535), (42000, 0), (42000, 65535), (65535, 65535),
        ]
        for t in tests:
            unique_float = map(t[0], t[1])
            print(f"{C_GREEN}f({t[0]}, {t[1]}){C_RES} = {unique_float}")
        # ZCurve().draw()
        # ZCurve().check_injectivity(x_max=100, y_max=1000)

    except ValueError as e:
        print(e)

if (__name__ == "__main__"):
    main()