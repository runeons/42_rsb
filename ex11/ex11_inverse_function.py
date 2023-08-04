# import matplotlib.pyplot as plt
from typing import Tuple

C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

class ZCurve:
    def __init__(self):
        self.y_min = self._coordinates_to_int(0, 0)
        self.y_max = self._coordinates_to_int(65535, 65535)
        self.denormalise_max = 4294967295

    def _check_param(self, p):
        if (not isinstance(p, int)) or (p < 0 or p > 65535):
            raise ValueError(f"{C_RED}Error: {C_RES}Parameter {p} must be a natural number between 0 and 65535.")

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

    ################## reverse_map ################## f(float) -> (x, y)

    def _denormalise(self, input_float):
        ret = input_float * self.denormalise_max
        return (int(ret))

    def _int_to_coordinates(self, value):
        SHIFTS = [1, 2, 4, 8]
        MASKS = [ 0x33333333, 0x0F0F0F0F, 0x00FF00FF, 0xFFFFFFFF]        
        x = int(value) & 0x55555555
        y = (int(value) & 0xAAAAAAAA) >> 1
        for i in range(0, 4, 1):
            x = (x | (x >> SHIFTS[i])) & MASKS[i]
            y = (y | (y >> SHIFTS[i])) & MASKS[i]
        return x % 65536, y % 65536

    def reverse_map(self, p):
        if (p < 0 or p > 1):
            raise ValueError(f"{C_RED}Error: {C_RES} input {p} must be between 0 and 1.")
        tmp = p
        p = self._denormalise(p)
        x, y = self._int_to_coordinates(p)
        return x, y

    ################## reverse_map draw ################## f(float) -> x, y

    def _iterate_floats(self, start, stop, step):
        current = start
        while current < stop:
            yield current
            current += step

    # def reverse_draw(self):
    #     print(C_YELLOW, "reverse_draw", C_RES)
    #     x_coords = []
    #     y_coords = []
    #     precisions = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    #     for p in precisions:
    #         for f in self._iterate_floats(0, 1 - p, p):
    #             i = self._denormalise(f)
    #             x, y = self._int_to_coordinates(i)
    #             x_coords.append(x)
    #             y_coords.append(y)
    #         plt.plot(x_coords, y_coords, 'b.')
    #         plt.xlabel('X')
    #         plt.ylabel('Y')
    #         plt.title('Z-curve')
    #         plt.axis('equal') 
    #         plt.show()

def map(x: int, y:int) -> float:
    zcurve = ZCurve()
    return zcurve.map(x, y)

def reverse_map(f: float) -> Tuple[int, int]:
        zcurve = ZCurve()
        x, y = zcurve.reverse_map(f)
        return (x, y)

def main():
    try:
        float_tests = [
            0, 0.2, 0.4, 0.6, 0.8, 1,
            # 0.48, 0.99,
            # 0.9000000001164153, 0.9899999999883584,  0.9900000002211891, 0.9899999999883584, 0.9899999997555278, 0.9899999999883584, 0.9900000002211891, 0.9900000004540197,
        ]
        for f in float_tests:
            x, y = reverse_map(f)
            check = map(x, y)
            if (f == check):
                print(f"{C_GREEN}True: {C_RES}{f} = f({x}, {y}) = {check}{C_RES}")
            else:
                print(f"{C_RED}False: {C_RES}{f} = f({x}, {y}) != {check}{C_RES}")
        # ZCurve().reverse_draw()
    except ValueError as e:
        print(e)

if (__name__ == "__main__"):
    main()

