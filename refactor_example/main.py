import receipt
from colorama import Fore


def print_receipt(receipt: receipt.Receipt) -> None:
    balance = 0
    print(Fore.CYAN + f"Receipt for \033[1m{receipt.customer_name}\033[0m")
    print(Fore.YELLOW + "===========================================================")
    print(Fore.WHITE + "\033[1mItems:\033[0m")
    for list_item in receipt.item_list:
        price = list_item.item.price * list_item.quantity
        print(
            f"{list_item.item.name}:\n\t Price: ${list_item.item.price/100:.2f} * Quantity: {list_item.quantity} = ${price/100:.2f} "
        )
        balance += price
    print(Fore.YELLOW + "---------------------------------------------------------")
    print(
        Fore.WHITE + f"TOTAL BALANCE: {Fore.RED} \033[1m${balance / 100:.2f}\033[0m\n"
    )


if __name__ == "__main__":
    print_receipt(receipt.RECIEPT_ONE)
    print_receipt(receipt.RECIEPT_TWO)
