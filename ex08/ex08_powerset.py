C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

class Powerset:
    def __init__(self, init_set: set):
        self.init_set = init_set
        self.subsets = set()
        self.compute()

    def compute(self):
        set_len = len(self.init_set)
        l = list(self.init_set)
        masks = [1 << i for i in range(set_len)]
        for i in range(1 << set_len):
            subset = []
            for m, nb in zip (masks, l):
                if i & m:
                    subset.append(nb)
            self.subsets.add(tuple(subset))

    def print(self):
        print(C_GREEN, "Powerset of", self.init_set, C_RES)
        for s in self.subsets:
            print(s)

def powerset(s: int) -> set():
    p = Powerset(s)
    # p.print()
    return p.subsets

def main():
    sets_test = [{1, 2, 3}, {1, 2}, {1}, {1, 2, 8, 18}]
    for s in sets_test:
        ps = powerset(s)
        print(C_GREEN, "Powerset of", s, C_RES)
        for ss in ps:
            print(ss)

if (__name__ == "__main__"):
    main()