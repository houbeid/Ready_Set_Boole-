def gray_code(n: int) -> int:
    return n ^ (n >> 1);
def main():
    print(gray_code(1))
    print(gray_code(2))
    print(gray_code(3))
    print(gray_code(4))
    print(gray_code(5))
    print(gray_code(6))


if __name__ == "__main__":
    main()