from src.preprocess import (
    _1_extract_csv,
    _2_extract_img,
    _3_process_csv,
    _4_process_img,
    _5_build_sqlite,
    _6_build_vector,
)


def main():
    print("\033[92m" + "Step 1" + "\033[0m")
    _1_extract_csv.main()
    
    print("\033[92m" + "Step 2" + "\033[0m")
    _2_extract_img.main()
    
    print("\033[92m" + "Step 3" + "\033[0m")
    _3_process_csv.main()
    
    print("\033[92m" + "Step 4" + "\033[0m")
    _4_process_img.main()
    
    print("\033[92m" + "Step 5" + "\033[0m")
    _5_build_sqlite.main()
    
    print("\033[92m" + "Step 6" + "\033[0m")
    _6_build_vector.main()


if __name__ == "__main__":
    main()
