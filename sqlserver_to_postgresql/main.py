from common.config import Config
from logic_migrator.main import SQLLogicMigrator


def main():
    SQLLogicMigrator().migrate()

if __name__ == "__main__":
    main()