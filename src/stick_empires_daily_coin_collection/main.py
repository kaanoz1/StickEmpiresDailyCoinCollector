import asyncio

import requests

from stick_empires_daily_coin_collection.StickEmpiresDailyCoinLoop import StickEmpiresDailyCoinCollectorLoop
from stick_empires_daily_coin_collection.predefinedCallbacks import callback_if_coin_amount_not_changed, callback_if_coin_amount_changed, callback_previous_state_fetched, callback_new_state_saved
from stick_empires_daily_coin_collection.predefinedCallbacks import callback_login_validated
async def main():
    await StickEmpiresDailyCoinCollectorLoop.run(
        callback_if_coin_amount_not_changed=callback_if_coin_amount_not_changed,
        callback_if_coin_amount_changed=callback_if_coin_amount_changed,
        callback_previous_state_fetched=callback_previous_state_fetched,
        callback_new_state_saved=callback_new_state_saved,
        callback_if_login_validated=callback_login_validated
    )

if __name__ == "__main__":
    asyncio.run(main())
        
