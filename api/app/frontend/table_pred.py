import pandas as pd
import reflex as rx 
import reflex as rx
from ..backend.stock_state import StockInfor

previous_stockinfo = StockInfor.table_data

# class RowObject(rx.State):
#     stock_data: list[list] = [ 
#         previous_stockinfo.get("StockData")
#     ]

def show_stock(stockdata: list):
    return rx.table.row(
        rx.table.cell(stockdata[0]),
        rx.table.cell(stockdata[1]),
        rx.table.cell(stockdata[2]),
        rx.table.cell(stockdata[3]),
        rx.table.cell(stockdata[4]),
        rx.table.cell(stockdata[5]),
    )


def table_pred() -> rx.Component:
    return rx.box(
        rx.cond(
            StockInfor.table_data,
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Date"),
                        rx.table.column_header_cell("Close"),
                        rx.table.column_header_cell("Open"),
                        rx.table.column_header_cell("High"),
                        rx.table.column_header_cell("Low"),
                        rx.table.column_header_cell("Volume")
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        StockInfor.table_data,
                        show_stock
                    )
                )
            ),
            rx.text("No data available", text_align="center", class_name="p-4")
        ),
        class_name="bg-white-800 p-2 rounded-xl shadow-2xl border w-full"
    )
    
# def table_pred():
#     return rx.el.div(
#         rx.data_table(
#             data = [date, close, open, high, low, volume],
#             columns = ["Date", "Close", "Open", "High", "Low", "Volume"]
#         )
#     )