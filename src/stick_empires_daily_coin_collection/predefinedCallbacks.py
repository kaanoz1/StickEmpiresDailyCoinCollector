from stick_empires_daily_coin_collection.NtfyService import NtfyService

# These functions are written by author. 
# You can customize them as you want. They are just examples of how to use the callbacks.

from stick_empires_daily_coin_collection.logger import logger

async def callback_if_coin_amount_not_changed(current_coin_amount: int) -> None:
    await NtfyService.send_notification(
        title="Stick Empires Daily Coin Collector",
        message=f"Coin amount has not changed. Going to check again for each 1 hour. Current balance: {current_coin_amount}"
    )
    logger.info(f"Coin amount has not changed. Going to check again for each 1 hour. Current balance: {current_coin_amount}")

async def callback_if_coin_amount_changed(previous_coin_amount: int, current_coin_amount: int, diff: int) -> None:
    await NtfyService.send_notification(
        title="Stick Empires Daily Coin Collector",
        message=f"Coin amount changed! Current: {current_coin_amount} | Previous: {previous_coin_amount} | Difference: +{diff}"
    )
    logger.info(
        f"Coin amount changed! "
        f"Current: {current_coin_amount} | "
        f"Previous: {previous_coin_amount} | "
        f"Difference: +{diff}"
    )

def callback_previous_state_fetched(previous_coin_amount: int) -> None:
    logger.info(f"Previous state successfully fetched. Previous coin amount: {previous_coin_amount}")

async def callback_new_state_saved(current_coin_amount: int) -> None:
    await NtfyService.send_notification(
        title="Stick Empires Daily Coin Collector",
        message=f"New state successfully saved. Current coin amount: {current_coin_amount}"
    )
    logger.info(f"New state successfully saved. Current coin amount: {current_coin_amount}")

async def callback_login_validated() -> None:
    await NtfyService.send_notification(
        title="Stick Empires Daily Coin Collector",
        message="Login validated successfully."
    )
    logger.info("Login validated successfully.")

async def callback_if_empire_points_found() -> None:
    await NtfyService.send_notification(
        title="Stick Empires Daily Coin Collector",
        message="Empire points found in the message."
    )
    logger.info("Empire points found in the message.")


async def callback_if_loop_timeouted() -> None:
    await NtfyService.send_notification(
        title="Stick Empires Daily Coin Collector",
        message="Loop timed out. Exiting the loop. Please re-run the program."
    )
    logger.warning("Loop timed out. Exiting the loop.")