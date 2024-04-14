import contextlib
import random
from datetime import datetime
from typing import List

import pendulum
from postgrest._sync.request_builder import SyncRequestBuilder
from postgrest.base_request_builder import APIResponse
from rich import print
from supabase.client import PostgrestAPIError
from supamodel._client import client as supabase
from supamodel._logging import logger
from supamodel.enums import OrderSide, OrderStatus, OrderType
from supamodel.exceptions import EmptyResponseError
from supamodel.trading.order_management import Order, Trade
from supamodel.trading.portfolio import Portfolio, Position

# Can get the exchange_id from the asset_id. We can simply look at the asset's exchange_id and return it.

depth_logger = logger.opt(depth=1)


class MockExchangeAPI:
    def submit_order(self, order: Order) -> Order:
        order.status = OrderStatus.FILLED
        return order

    def get_order(self, order_id: str) -> Order:
        return Order()

    def calculate_fees(self, order: Order) -> float:
        return random.uniform(0.0, 0.1)

    def get_exchange_id(self, asset_id: str) -> str:
        return "exchange_id"

    def get_current_price(self, position: Position) -> float:
        return random.uniform(0.0, 100.0)

    def get_fill_timestamp(order: Order) -> float:
        return pendulum.now("UTC").timestamp()

    def get_fill_details(self, order: Order) -> dict:
        return random.uniform(0.1, 100), random.uniform(0.1, 8.0)


exchange_api = MockExchangeAPI()


def submit_order(order: Order) -> Order:
    """
    Submits an order to the database.

    Args:
        order (Order): The order to be submitted.

    Returns:
        Order: The submitted order.

    Raises:
        EmptyResponseError: If the response from the database is empty.
    """
    response = supabase.table("orders").insert(order.supa_dump(by_alias=True)).execute()
    resp_data = response.data
    resp_data if resp_data else []
    if not resp_data:
        raise EmptyResponseError("Failed to add order to the database.")
    return resp_data


def change_order_status(order_id: str, status: OrderSide) -> Order:
    """
    Change the status of an order.

    Args:
        order_id (str): The ID of the order to update.
        status (OrderSide): The new status of the order.

    Returns:
        Order: The updated order object.

    """
    result = (
        supabase.table("orders")
        .update({"status": status.value})
        .eq("id", order_id)
        .execute()
    )
    results = process_results(result)
    return Order(**results[0])
    # return resp_data


def create_position(order: Order) -> Position:
    """
    Creates a new position based on the given order and saves it to the database.

    Args:
        order (Order): The order object containing the details of the position.

    Returns:
        Position: The newly created position object.

    """

    new_position = Position(
        portfolio_id=order.portfolio_id,
        asset_id=order.asset_id,
        quantity=order.quantity,
        average_price=order.price,
    )
    result: APIResponse = (
        supabase.table("positions")
        .insert(new_position.supa_dump(by_alias=True))
        .execute()
    )
    results = process_results(result)

    return Position(**results[0])


def process_results(results: APIResponse, need_data: bool = True) -> List[dict]:
    """
    Process the results from the API response.

    Args:
        results (APIResponse): The API response object.
        need_data (bool, optional): Flag indicating whether data is required. Defaults to True.

    Returns:
        List[dict]: The processed result data.

    Raises:
        EmptyResponseError: If the result data is empty and need_data is True.
    """
    result_data = results.data if results.data else []
    if not result_data and need_data:
        depth_logger.error("Failed to process Supabase results.")
        raise EmptyResponseError()

    return result_data


def transact_trade_position(order: Order) -> Trade:
    with contextlib.suppress(Exception):
        position: Position = create_position(order)

        trade = Trade(
            position_id=position.id,
            order_id=order.id,
            quantity=order.quantity,
            price=order.price,
            fee=exchange_api.calculate_fee(order),
            timestamp=exchange_api.get_fill_timestamp(order),
        )
        result = (
            supabase.table("trades").insert(trade.supa_dump(by_alias=True)).execute()
        )

        results = process_results(result)
        return Trade(**results[0])


# @retry(exception=PostgrestAPIError, tries=5, delay=1)
def get_position(position_id: str) -> Position:
    result = supabase.table("positions").select("*").eq("id", position_id).execute()
    results = process_results(result)
    return Position(**results[0])


def save_position(position: Position) -> Position:
    result = (
        supabase.table("positions")
        .update(position.supa_dump(by_alias=True))
        .eq("id", position.id)
        .execute()
    )
    results = process_results(result)
    return Position(**results[0])


def update_position(order: Order, trade: Trade) -> Position:
    position = get_position(trade.position_id)
    fill_quantity, fill_price = exchange_api.get_fill_details(order)
    if order.side == OrderSide.BUY:
        position.quantity += fill_quantity
        position.average_price = (
            position.average_price * position.quantity + fill_price * fill_quantity
        ) / (position.quantity + fill_quantity)
    else:
        position.quantity -= fill_quantity
    position.updated_at = datetime.now()
    return save_position(position)


def main():
    #
    portfolio_json = [
        {
            "id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "user_id": "b3209dcc-3097-430e-8ad1-c9bb4660aa4c",
            "name": "USD Portfolio",
            "exchange_id": "6663abed-f538-40ad-9ebc-8aa183944b34",
            "base_currency_id": "0cef4f9b-d607-408e-92ed-5a0382e0fe35",
            "created_at": pendulum.DateTime.now().subtract(days=3),
            "updated_at": pendulum.DateTime.now(),
            "balance": "186205.7935856367730908",
        }
    ]
    man_portfolio = Portfolio(**portfolio_json[0])
    [
        {
            "id": "0b085f9d-d0db-498f-8b36-5cd6b3524c0d",
            "portfolio_id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "asset_id": "b77e616c-9139-45ad-9b2d-3b3cbed953f9",
            "quantity": "95.18501283",
            "average_price": "370.86070974",
            "created_at": "2024-04-09 06:06:18.065308+00",
            "updated_at": "2024-04-09 06:06:18.065308+00",
        }
    ]
    man_position = Position(
        **{
            "id": "0b085f9d-d0db-498f-8b36-5cd6b3524c0d",
            "portfolio_id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "asset_id": "b77e616c-9139-45ad-9b2d-3b3cbed953f9",
            "quantity": "95.18501283",
            "average_price": "370.86070974",
            "created_at": pendulum.DateTime.now().subtract(days=2),
            "updated_at": pendulum.DateTime.now(),
        }
    )
    man_order = Order(
        **{
            "id": "0b085f9d-d0db-498f-8b36-5cd6b3524c0d",
            "portfolio_id": "149ba2ba-289c-4bd1-8cad-4b7c3925c1ca",
            "asset_id": "b77e616c-9139-45ad-9b2d-3b3cbed953f9",
            "exchange_id": "6663abed-f538-40ad-9ebc-8aa183944b34",
            "order_type": OrderType.MARKET,
            "side": OrderSide.BUY,
            "quantity": 10,
            "price": 100,
            "status": OrderStatus.PENDING,
            "created_at": pendulum.DateTime.now().subtract(days=1),
            "updated_at": pendulum.DateTime.now(),
        }
    )
    print(man_portfolio)
    print(man_position)
    print(man_order)

    # print(manual)

    # manual_order = Order(
    #     asset_id=manual.asset_id,
    #     portfolio_id=portfolio.id,
    #     quantity=10,
    #     price=100,
    #     side=OrderSide.BUY,
    #     type=OrderType.MARKET,
    # )
    # print(manual_order)


if __name__ == "__main__":
    main()
