# import matplotlib.pyplot as plt

C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

class ZCurve:
    def __init__(self):
        self.y_min = self.z_curve_to_float(0, 0)
        self.y_max = self.z_curve_to_float(65535, 65535)
        self.denormalise_max = 4294967295

    def check_param(self, p):
        if (not isinstance(p, int)) or (p < 0 or p > 65535):
            raise ValueError(f"{C_RED}Error: {C_RES}Parameter {p} must be a natural number between 0 and 65535.")

    def normalise(self, raw_nb):
        return (raw_nb - self.y_min) / (self.y_max - self.y_min)

    def denormalise(self, input_float):
        ret = input_float * self.denormalise_max
        return (int(ret))

    def map(self, x, y):
        for p in [x, y]:
            self.check_param(p)
        res = self.z_curve_to_float(x, y)
        return self.normalise(res)

    # 0x55555555 = 01010101 01010101 01010101 01010101
    # 0x33333333 = 00110011 00110011 00110011 00110011
    # 0x0F0F0F0F = 00001111 00001111 00001111 00001111
    # 0x00FF00FF = 00000000 11111111 00000000 11111111
    def z_curve_to_float(self, init_x, init_y):
        SHIFTS = [1, 2, 4, 8]
        MASKS = [0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF]        
        x = init_x  
        y = init_y
        for i in range(3, -1, -1):
            x = (x | (x << SHIFTS[i])) & MASKS[i]
            y = (y | (y << SHIFTS[i])) & MASKS[i]
        result = x | (y << 1)
        return result
    
    def number_to_z_curve(self, value):
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
        p = self.denormalise(p)
        print(C_YELLOW, tmp, "=====>", p, C_RES)
        x, y = self.number_to_z_curve(p)
        return x, y

    # def draw(self, x_min=0, x_max=10, y_min=0, y_max=10):
    #     print(C_YELLOW, "draw", C_RES)
    #     for p in [x_min, y_min, x_max, y_max]:
    #         self.check_param(p)
    #     if (x_min > x_max) or (y_min > y_max):
    #         raise ValueError(f"{C_RED}Error: {C_RES} x_min > x_max or y_min > y_max")
    #     all_results = set()
    #     # all_results.add(self.normalise(self.z_curve_to_float(0, 0)))
    #     for x in range(x_min, x_max + 1):
    #         for y in range(y_min, y_max + 1):
    #             res = self.normalise(self.z_curve_to_float(x, y))
    #             all_results.add(res)
    #     # all_results.add(self.normalise(self.z_curve_to_float(65535, 65535)))
    #     x_coords = list(range(len(all_results)))
    #     y_coords = list(all_results)
    #     plt.plot(x_coords, y_coords, 'b.')
    #     plt.xlabel('Itérations')
    #     plt.ylabel('f(x, y)')
    #     plt.title(f"Z Curve for x=[{x_min}, {x_max}], y=[{y_min}, {y_max}]")
    #     plt.show()

    # def reverse_draw(self):
    #     print(C_YELLOW, "reverse_draw", C_RES)
    #     z_curve_coordinates = []
    #     for f in range(0, 50000):
    #         x_coords, y_coords = self.number_to_z_curve(f)
    #         z_curve_coordinates.append((x_coords, y_coords))
    #     # for f in range(55325, 65535):
    #     #     x_coords, y_coords = self.number_to_z_curve(f)
    #     #     z_curve_coordinates.append((x_coords, y_coords))
    #     # for f in range(4294960000, 4294967295):
    #     #     x_coords, y_coords = self.number_to_z_curve(f)
    #     #     z_curve_coordinates.append((x_coords, y_coords))
    #     print(len(z_curve_coordinates))
    #     for i, (x_coords, y_coords) in enumerate(z_curve_coordinates):
    #         plt.plot(x_coords, y_coords, label=f'Z-Curve {i+1}')
    #     plt.plot(x_coords, y_coords, 'b.')
    #     plt.xlabel('X')
    #     plt.ylabel('Y')
    #     plt.title('Visualisation des coordonnées de la z-curve')
    #     plt.show()

def main():
    try:
        tests = [
            0, 
            1,
            0.9000000001164153,
            0.99,
            0.9899999999883584, 
            0.9900000002211891,
            0.9899999999883584,
            0.9899999997555278,
            0.9899999999883584,
            0.9900000002211891,
            0.9900000004540197,
            0.6,
        ]
        zcurve = ZCurve()
        for t in tests:
            x, y = zcurve.reverse_map(t)
            check = zcurve.map(x, y)
            if (t == check):
                print(f"{C_GREEN}True: {t} = f({x}, {y}) = {check}{C_RES}")
            else:
                print(f"{C_RED}False: {t} = f({x}, {y}) != {check}{C_RES}")
            print()
        # zcurve.reverse_draw()
    except ValueError as e:
        print(e)

if (__name__ == "__main__"):
    main()