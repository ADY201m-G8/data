from src.preprocess import (
    _1_extract_csv,
    _2_extract_img,
    _3_process_csv,
    _4_build_sqlite,
    _5_build_vector,
)


def main():
    _1_extract_csv.main()
    _2_extract_img.main()
    _3_process_csv.main()
    _4_build_sqlite.main()
    _5_build_vector.main()


if __name__ == "__main__":
    main()
