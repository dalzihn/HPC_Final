import reflex as rx
from ..backend.stock_state import StockInfor

# Sample data for the chart when no prediction is available
sample_data = [
    {"name": "Page A", "uv": 4000, "pv": 2400, "amt": 2400},
    {"name": "Page B", "uv": 3000, "pv": 1398, "amt": 2210},
    {"name": "Page C", "uv": 2000, "pv": 9800, "amt": 2290},
    {"name": "Page D", "uv": 2780, "pv": 3908, "amt": 2000},
    {"name": "Page E", "uv": 1890, "pv": 4800, "amt": 2181},
    {"name": "Page F", "uv": 2390, "pv": 3800, "amt": 2500},
    {"name": "Page G", "uv": 3490, "pv": 4300, "amt": 2100},
]

def line_pred():
    return rx.box(
        rx.recharts.line_chart(
            rx.recharts.line(
                data_key="predicted_price",
            ),
            rx.recharts.x_axis(data_key="timestamp"),
            rx.recharts.y_axis(),
            rx.recharts.graphing_tooltip(),
            data=rx.cond(
                StockInfor.line_data.length() > 0,
                StockInfor.line_data,
                sample_data,
            ),
            width="100%",
            height=370,
            class_name="p-1.5 bg-white rounded-xl shadow-2xl space-y-4 w-full h-screen border"
        )
    )