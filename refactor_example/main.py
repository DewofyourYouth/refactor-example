from dataclasses import dataclass
from typing import List

from colorama import Fore

import inventory


@dataclass
class OrderRow:
    item: inventory.InventoryItem
    quantity: int = 1


def print_receipt(
    customer_name: str,
    item_list=List[OrderRow],
    html: bool = False,
) -> None:
    balance = 0
    if not html:
        print(Fore.CYAN + f"Receipt for \033[1m{customer_name}\033[0m")
        print(
            Fore.YELLOW + "==========================================================="
        )
        print(Fore.WHITE + "\033[1mItems:\033[0m")
        for list_item in item_list:
            price = list_item.item.price * list_item.quantity
            print(
                f"{list_item.item.name}:\n\t Price: ${list_item.item.price/100:.2f} * Quantity: {list_item.quantity} = ${price/100:.2f} "
            )
            balance += price
        print(Fore.YELLOW + "---------------------------------------------------------")
        print(
            Fore.WHITE
            + f"TOTAL BALANCE: {Fore.RED} \033[1m${balance / 100:.2f}\033[0m\n"
        )
    else:
        html_str = []
        html_str.append(
            f"<div class='receipt'><h3>Receipt for <strong>{customer_name}<strong></h3><hr>"
        )
        if len(item_list) > 0:
            html_str.append(
                "<table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody>"
            )
            for list_item in item_list:
                price = list_item.item.price * list_item.quantity
                html_str.append(
                    f"<tr><td>{list_item.item.name}</td><td>${list_item.item.price/100:.2f}</td><td>{list_item.quantity}</td><td></td>${price/100:.2f}</tr>"
                )
                balance += price
            html_str.append("</tbody></table>")
            html_str.append(f"<h4>Total: ${balance / 100:.2f}</h4>")
        html_str.append("</div>")
        print("".join(html_str))


def main():
    print(Fore.BLUE + "TERMINAL RECEIPTS")
    print("===================\n")
    print_receipt(
        customer_name="Joe Swanson",
        item_list=[
            OrderRow(item=inventory.MILK, quantity=2),
            OrderRow(item=inventory.BREAD, quantity=1),
            OrderRow(item=inventory.CHEESE),
        ],
    )
    print_receipt(
        customer_name="Peter Griffin",
        item_list=[
            OrderRow(item=inventory.BEEF, quantity=2),
            OrderRow(item=inventory.LUCKY_CHARMS),
            OrderRow(item=inventory.CHEESE, quantity=5),
            OrderRow(item=inventory.MILK, quantity=3),
        ],
    )
    print(Fore.BLUE + "TERMINAL RECEIPTS")
    print("===================\n" + Fore.WHITE)
    print_receipt(
        customer_name="Peter Griffin",
        item_list=[
            OrderRow(item=inventory.BEEF, quantity=2),
            OrderRow(item=inventory.LUCKY_CHARMS),
            OrderRow(item=inventory.CHEESE, quantity=5),
            OrderRow(item=inventory.MILK, quantity=3),
        ],
        html=True,
    )


if __name__ == "__main__":
    main()
