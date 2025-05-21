import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(
                    src="/logoUEH.png",
                    width="6em",
                    height="6em",
                    border_radius="25%",
                    object_fit="contain"
                ),
                rx.vstack(
                    rx.heading(
                        "Tính toán hiệu suất cao (HPC)", 
                        size="6", 
                        weight="bold"
                    ),
                    rx.text("Group 02, Stock Price Prediction using distributed LSTM", size="3"),
                    align_items="start",
                    spacing="1"
                ),
                align="center"
            ),
            justify="between",
            align="center",
            width="100%",
            padding_x="4em"
        ),
        bg=rx.color("accent", 3),
        padding_y="1em",
        width="100%",
    )
