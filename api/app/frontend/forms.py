import reflex as rx
from ..backend.stock_state import StockInfor

def stock_input_form():
    return rx.el.div(
        rx.vstack(
            rx.heading("Stock Code Input"),
            rx.form.root(
                rx.hstack(
                    rx.input(
                        value=StockInfor.ticker,
                        on_change=StockInfor.set_ticker,
                        placeholder="Enter ticker",
                        type="text",
                        required=True
                    ),
                    rx.button("Submit", 
                        type="submit"
                    ),
                    width="100%"
                ),
                on_submit=StockInfor.handle_submit,
            )
        ),
        class_name="p-8 max-w bg-white rounded-xl shadow-2xl space-y-4 border"
    )