import reflex as rx

def footer_item(text: str) -> rx.Component:
    return rx.text(text, size="3")

def footer() -> rx.Component:
    return rx.box(
        rx.divider(),
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
                        "University of Economics Ho Chi Minh City",
                        size="6",
                        weight="bold"
                    ),
                    rx.text(
                        "Department of Business Information Technology",
                        size="2",
                    ),
                    align_items="start",
                    spacing="1"
                ),
                spacing="3",
                align="center"
            ),
            justify="between",
            align="center",
            width="100%",
            padding_x="4em",
            padding_y="1.5em"
        ),
        width="100%",
        bg=rx.color("gray", 1)
    )