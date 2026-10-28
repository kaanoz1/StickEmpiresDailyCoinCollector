class StickEmpiresEmpirePointTracker:
    @staticmethod
    def is_empire_points_in_message(message: bytes) -> bool:
        return b"empirePoints" in message

    @staticmethod
    def extract_empire_points_from_message(message: bytes) -> int:
        index: int = message.find(b"empirePoints")
        length = "empirePoints".__len__()
        amount_in_bytes = message[index + length + 1:index+length+5]
        return int.from_bytes(amount_in_bytes, byteorder="big")
