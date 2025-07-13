def adder(a: int, b: int) -> int:
    while b != 0:
        c = a & b
        a = a ^ b
        b = c << 1
    return a;

def multiplier(a: int, b: int) -> int:
    result = 0
    while b != 0:
        if b & 1 != 0:
            result = adder(result, a)
        a = a << 1
        b = b >> 1
    return result
def main():
    print(multiplier(3, 4))     # 12
    print(multiplier(0, 10))    # 0
    print(multiplier(7, 6))     # 42
    print(multiplier(123, 0))   # 0
    print(multiplier(13, 13))   # 169

if __name__ == "__main__":
    main()