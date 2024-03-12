# This is the entry point to your code
from decouple import config

from src.project_name import generate_chart, load_data, transform_data


def main() -> None:
    secret_password = config("SUPER_SECRET_PASSWORD")
    print(f"This is my password: {secret_password}")

    load_data()
    transform_data()
    generate_chart()


if __name__ == "__main__":
    main()
