
from dataclasses import dataclass, field
from typing import Any, Sequence


def get_product_image(name: str):
    return f"static/images/products/{name}"


class Image:
    attributes = {"src": get_product_image("unknown.jpg"), "alt": "Unknown"}

    def __init__(self, **kwargs) -> None:
        self.attributes = self.attributes.copy()
        self.set_attributes(**kwargs)

    def set_attributes(self, **kwargs):
        self.attributes.update(kwargs)

    def get_html_attributes(self):
        return " ".join(f"{k}={v}" for k, v in self.attributes.items())


@dataclass
class Product:
    display_name: str
    price: float
    original_price: float = 0
    author = "Unknown"
    description: str = "N/A"
    image: Image = field(default_factory=Image)

    def set_data(self, **kwargs):
        for name, attribute in kwargs.items():
            setattr(self, name, attribute)


def get_default_database():
    image_1 = Image(src=get_product_image("shampoo_bottle.png"), alt="Shampoo")
    image_2 = Image(src=get_product_image("premium_pencil.png"), alt="Pencil")
    image_3 = Image(src=get_product_image(
        "toilet_paper.png"), alt="ToiletPaper")

    product_1 = Product(display_name="Shampoo bottle",
                        price=600, description="Yummy", image=image_1)

    product_2 = Product(display_name="Premium Pencil",
                        price=1500, description="Don't put in your...", image=image_2)

    product_3 = Product(display_name="Toilet Paper",
                        price=5000, original_price=500_000, description="Limited supply special", image=image_3)
    return product_1, product_2, product_3


shades_of_gray_image = Image(
    src=get_product_image("shadesOgrey.jpg"), alt="shades")

shades_of_gray = Product(display_name="shades of grey", price=500,
                         description="Quench your heart's desires", image=shades_of_gray_image)
shades_of_gray.set_data(author="Unknown")

unknown_book = Product("some random book found on the street", 50, 1)

books: Sequence[Product] = (*get_default_database(),
                            unknown_book, shades_of_gray)

class cart[T=Any]:
    def __init__(self) -> None:
        self.items:list[T] = []

    def __iter__(self):
        yield from self.items
        
    def __setitem__(self, key, value:T):
        self.items[key] = value
    def __getitem__(self, key)->T:
        return self.items[key]
        
    def __delitem__(self, key):
        del self.items[key]

    def get_items(self)->Sequence[T]:
        return self.items.copy()

    def add_items(self,items:Sequence[T]):
        self.items.extend(items)

    def add_item(self,item:T):
        self.items.append(item)

