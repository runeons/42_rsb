# import matplotlib.pyplot as plt

C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

class ZCurve:
    def __init__(self):
        self.y_min = self.z_curve_to_number(0, 0)
        self.y_max = self.z_curve_to_number(65535, 65535)

    def check_param(self, p):
        if (not isinstance(p, int)) or (p < 0 or p > 65535):
            raise ValueError(f"{C_RED}Error: {C_RES}Parameter {p} must be a natural number between 0 and 65535.")

    def normalise(self, raw_nb):
        return (raw_nb - self.y_min) / (self.y_max - self.y_min)

    def map(self, x, y):
        for p in [x, y]:
            self.check_param(p)
        res = self.z_curve_to_number(x, y)
        return self.normalise(res)

    def check_injectivity(self, x_max=65536, y_max=65536):
        print(C_YELLOW, "check_injectivity", C_RES)
        all_results = set()
        for x in range(x_max):
            for y in range(y_max):
                res = self.normalise(self.z_curve_to_number(x, y))
                if res in all_results:
                    raise ValueError(f"{C_RED}Error: {C_RES}NOT INJECTIVE {res} for {x}, {y}")
                all_results.add(res)

    # 0x55555555 = 01010101 01010101 01010101 01010101   0
    # 0x33333333 = 00110011 00110011 00110011 00110011   1
    # 0x0F0F0F0F = 00001111 00001111 00001111 00001111   2
    # 0x00FF00FF = 00000000 11111111 00000000 11111111   3

    # Interleave lower 16 bits of x and y, so the bits of x are in the even positions and bits from y in the odd
    def z_curve_to_number(self, init_x, init_y):
        SHIFTS = [1, 2, 4, 8]
        MASKS = [0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF]        
        x = init_x  
        y = init_y
        for i in range(3, -1, -1): # start, end, jump
            x = (x | (x << SHIFTS[i])) & MASKS[i]
            y = (y | (y << SHIFTS[i])) & MASKS[i]
        result = x | (y << 1)
        # print(f"{C_BLUE}z_curve de {init_x}-{init_y} = {result}{C_RES}      x = {x} y = {y}")
        return result
    
    # 0x55555555 = 01010101 01010101 01010101 01010101
    # 0x33333333 = 00110011 00110011 00110011 00110011
    # 0x0F0F0F0F = 00001111 00001111 00001111 00001111
    # 0x00FF00FF = 00000000 11111111 00000000 11111111
    def number_to_z_curve(self, value):
        SHIFTS = [1, 2, 4, 8]
        MASKS = [ 0x33333333, 0x0F0F0F0F, 0x00FF00FF, 0xFFFFFFFF]        
        # print(C_GREEN, value, C_RES)
        x = int(value) & 0x55555555
        y = (int(value) & 0xAAAAAAAA) >> 1
        for i in range(0, 4, 1): # start, end, jump
            x = (x | (x >> SHIFTS[i])) & MASKS[i]
            y = (y | (y >> SHIFTS[i])) & MASKS[i]
        return x, y

    def reverse_map(self, p):
        if (p < 0 or p > 1):
            raise ValueError(f"{C_RED}Error: {C_RES} input {p} must be between 0 and 1.")
        x, y = self.number_to_z_curve(p)
        return x, y

    # def draw(self, x_min=0, x_max=10, y_min=0, y_max=10):
    #     print(C_YELLOW, "draw", C_RES)
    #     for p in [x_min, y_min, x_max, y_max]:
    #         self.check_param(p)
    #     if (x_min > x_max) or (y_min > y_max):
    #         raise ValueError(f"{C_RED}Error: {C_RES} x_min > x_max or y_min > y_max")
    #     all_results = set()
    #     # all_results.add(self.normalise(self.z_curve_to_number(0, 0)))
    #     for x in range(x_min, x_max + 1):
    #         for y in range(y_min, y_max + 1):
    #             res = self.normalise(self.z_curve_to_number(x, y))
    #             all_results.add(res)
    #     # all_results.add(self.normalise(self.z_curve_to_number(65535, 65535)))
    #     x_coords = list(range(len(all_results)))
    #     y_coords = list(all_results)
    #     plt.plot(x_coords, y_coords, 'b.')
    #     plt.xlabel('Itérations')
    #     plt.ylabel('f(x, y)')
    #     plt.title(f"Z Curve for x=[{x_min}, {x_max}], y=[{y_min}, {y_max}]")
    #     plt.show()

def main():
    try:
        tests = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 1),
            (255, 255),
            (255, 256),
            # (4096, 4096),
            # (40000, 40000),
            # (40000, 40000),
            # (41000, 65535),
            # (42000, 0),
            # (42000, 65535),
            # (65535, 65535),
        ]
        zcurve = ZCurve()
        for t in tests:
            res = zcurve.z_curve_to_number(t[0], t[1])
            x, y = zcurve.number_to_z_curve(res)
            if (t[0] == x and t[1] == y):
                print(f"{C_GREEN}True: {res} = f({x}, {y}) == f({t[0]}, {t[1]}){C_RES}")
            else:
                raise ValueError(f"{C_RED}False: {res} = f({x}, {y}) != f({t[0]}, {t[1]}){C_RES}")
                print(f"{C_RED}False: {res} = f({x}, {y}) != f({t[0]}, {t[1]}){C_RES}")
        for t in range(0, 3000):
            x, y = zcurve.number_to_z_curve(t)
            res = zcurve.z_curve_to_number(x, y)
            if (res == t):
                print(f"{C_GREEN}True: f({x}, {y}) = {t}{C_RES}")
            else:
                raise ValueError(f"{C_RED}False: f({x}, {y}) = {t} != {res}{C_RES}")
                # print(f"{C_RED}False: f({x}, {y}) = {t} != {res}{C_RES}")
        # zcurve.draw()
    except ValueError as e:
        print(e)

if (__name__ == "__main__"):
    main()