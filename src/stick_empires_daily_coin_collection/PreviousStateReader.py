class PreviousStateReader:
    
    @staticmethod
    def read_previous_state(self) -> int:
        try:
            with open(self.file_path, "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    @staticmethod
    def save_current_state(amount: int) -> None:
        with open("previous_coin.txt", "w") as f:
            f.write(str(amount))