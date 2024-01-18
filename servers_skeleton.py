#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from abc import ABC, abstractmethod
import re

class Product:
    
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price
    
    def __hash__(self):
        return hash((self.name, self.price))
    
class ServerError(Exception):
    pass

class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def get_entries(self, n_letters: int = 1) -> list[Product]:
        searching_pattern = '^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters)
        entries = [product for product in self.get_products(n_letters)
                   if re.match(searching_pattern, product.name)]
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        if entries:
            return sorted(entries, key=lambda product: product.price)
        return []

    @abstractmethod
    def get_products(self, n_letters: int = 1) -> list[Product]:
        return self.get_entries(n_letters)

class ListServer:
    def __init__(self, products: list[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: list[Product] = products

    def get_all(self, n_letters: int = 1) -> list[Product]:
        return self.products


class MapServer:
    def __init__(self, products: list[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products: dict[str, Product] = {p.name: p for p in products}

    def get_all(self, n_letters: int = 1) -> list[Product]:
        return list(self.products.values())


class Client:

    def __init__(self, server):
        self.server = server
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        # ilosc liter przy danym produkcie np. n=2, [AB12, ab2000, xp099] <- zwrocone wg posortowanej ceny rosnaco 
        raise NotImplementedError()