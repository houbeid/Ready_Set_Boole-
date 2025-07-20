def adder(a: int, b: int) -> int:
    while b != 0:
        c = a & b
        a = a ^ b
        b = c << 1
    return a;
def main():
    print(adder(1000, 155))  # 7

if __name__ == "__main__":
    main()