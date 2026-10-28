import asyncio
import socket
from socket import socket as SocketClass
import time  
import inspect 
from collections.abc import Callable
from stick_empires_daily_coin_collection.PreviousStateReader import PreviousStateReader
from stick_empires_daily_coin_collection.StickEmpiresEmpirePointTracker import StickEmpiresEmpirePointTracker
from stick_empires_daily_coin_collection.StickEmpiresServerConnector import StickEmpiresServerConnector
from stick_empires_daily_coin_collection.StickEmpiresLoginValidator import StickEmpiresLoginValidator


class StickEmpiresDailyCoinCollectorLoop:

    @staticmethod # Safety function for async or sync callbacks
    async def _execute_callback(callback: Callable | None, *args) -> None:
        if callback is None:
            return
            
        if inspect.iscoroutinefunction(callback):
            await callback(*args)
        else:
            callback(*args)

    @staticmethod
    async def run(execution_period: int = 60 * 60 * 24, loop_timeout: float = 5.0, *, 
                  call_back_if_loop_timeouted: Callable | None = None, 
                  callback_if_empire_points_found: Callable | None = None, 
                  call_back_if_no_empire_points_found: Callable | None = None, 
                  callback_login_process_started: Callable | None = None,
                  callback_if_login_validated: Callable | None = None,
                  callback_if_login_failed: Callable | None = None, 
                  callback_if_coin_amount_changed: Callable | None = None, 
                  callback_if_coin_amount_not_changed: Callable | None = None,
                  callback_previous_state_fetched: Callable | None = None,
                  callback_new_state_saved: Callable | None = None,
                  callback_loop_started: Callable | None = None,
                  callback_loop_ended: Callable | None = None,
                  callback_execution_started: Callable | None = None,
                  callback_execution_ended: Callable | None = None
                  ) -> None:        


        await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_execution_started)
        
        server_connector = StickEmpiresServerConnector()
        try:
            server_connector.connect()

            await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_login_process_started)

            server_connector.send_login_message()
            login_response = server_connector.get_next_message()
        

            if StickEmpiresLoginValidator.is_login_validated_by_server(login_response):
                await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_if_login_validated)

                starting_time: float = time.time()
                while True:
                  
                    await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_loop_started)

                    
                    now = time.time()
                    timeout: float = loop_timeout
                    passed = now - starting_time
                    

                    is_timeouted = passed > timeout

                    if is_timeouted:
                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(call_back_if_loop_timeouted)
                        break
                    empire_points_message = server_connector.get_next_message()

                    if StickEmpiresEmpirePointTracker.is_empire_points_in_message(empire_points_message):

                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_if_empire_points_found)
                        
                        current_coin_amount = StickEmpiresEmpirePointTracker.extract_empire_points_from_message(empire_points_message)
                        previous_coin_amount = PreviousStateReader.read_previous_state()

                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_previous_state_fetched, previous_coin_amount)   

                        diff = current_coin_amount - previous_coin_amount

                        if diff == 0:
                            await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_if_coin_amount_not_changed, current_coin_amount)
                            await asyncio.sleep(60 * 60) # Sleep for 1 hour before checking again if empire points changed
                            break

                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_if_coin_amount_changed, diff, current_coin_amount, previous_coin_amount)
                        
                        PreviousStateReader.save_current_state(current_coin_amount)

                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_new_state_saved)

                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_execution_ended)

                        execution_period = execution_period + 30 # Little time so that StickEmpires server would not block the next request.
                        await asyncio.sleep(execution_period)
                    else:
                        await StickEmpiresDailyCoinCollectorLoop._execute_callback(call_back_if_no_empire_points_found)
                        await asyncio.sleep(60 * 1) # Sleep for 1 minute before checking again if empire points are found
            
            
                await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_loop_ended)
            else:
                await StickEmpiresDailyCoinCollectorLoop._execute_callback(callback_if_login_failed)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            server_connector.close()

            
