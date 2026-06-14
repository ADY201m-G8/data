from src.preprocess import (
    _1_extract_csv,
    _2_extract_img,
    _3_process_csv,
    _4_process_img,
    _5_build_sqlite,
    _6_build_vector,
)


def run_pipeline():
    steps = [
        _1_extract_csv,
        _2_extract_img,
        _3_process_csv,
        _4_process_img,
        _5_build_sqlite,
        _6_build_vector,
    ]

    for index, step in enumerate(steps, start=1):
        print(f"\033[92m Step {index}/{len(steps)} \033[0m")

        try:
            step.main()
        except Exception as e:
            print(f"\033[91m [ERR] {e} \033[0m")
            exit(1)

    print("\033[92m Done. \033[0m")


def main():
    run_pipeline()


if __name__ == "__main__":
    main()
