
from dataclasses import dataclass, field



def get_product_image(name: str):
    return f"static/images/products/{name}"


class Image:
    attributes = {"src":get_product_image("unknown.jpg"), "alt":"Unknown"} 
    
    def __init__(self, **kwargs) -> None:
        self.attributes = self.attributes.copy()
        self.set_attributes(**kwargs)

    def set_attributes(self, **kwargs):
        self.attributes.update(kwargs)

    def get_tag_attributes(self):
        return " ".join(f"{k}={v}" for k, v in self.attributes.items())


@dataclass
class product:
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

    product_1 = product(display_name="Shampoo bottle",
                        price=600, description="Yummy", image=image_1)

    product_2 = product(display_name="Premium Pencil",
                        price=1500, description="Don't put in your...", image=image_2)

    product_3 = product(display_name="Toilet Paper",
                        price=5000, original_price=500_000, description="Limited supply special", image=image_3)
    return product_1, product_2, product_3


shades_of_gray_image = Image(
    src=get_product_image("shadesOgrey.jpg"), alt="shades")

shades_of_gray = product(display_name="shades of grey", price=500,
                         description="Quench your heart's desires", image=shades_of_gray_image)
shades_of_gray.set_data(author="Unknown")

unknown_book = product("some random book found on the street", 50, 1)

books = (*get_default_database(), unknown_book, shades_of_gray)


def get_featured_products():
    return books[:3]
