from PIL import Image
class Asciifier:
    def __init__(self, path):
        self.original_image = Image.open(path).convert("LA")
        self.img = self.original_image.copy()
        self.symbols = \
            ["@", "&", "/", "(", "*", ",", ".", " "]
            #["@", "&", "#", "/", "(", "*", ",", "."]
        self.borders = [32, 64, 96, 128, 160, 192, 224, 256]
        self.text = ""

        # print("Reverse the colour gradient? (Looks better on dark backgrounds)\nY - yes\n[N] - no")
        # inp = input().lower()
        # if (inp == "y" or inp == "yes"):
        #     self.symbols = self.symbols[::-1]

    def make_ascii(self, lps: int = 1) -> str:
        ascii_img = []

        for y in range(self.img.height):
            row = []
            for x in range(self.img.width):
                colour, alpha = self.img.getpixel((x, y))
                # make rows out of letters
                if alpha == 0:
                    row.append(" " * lps)
                else:
                    for i in range(len(self.symbols)):
                        if colour <= self.borders[i]:
                            row.append(self.symbols[i] * lps)
                            break
            # make each row
            ascii_img.append("".join(row))

        self.text = "\n".join(row for row in ascii_img)
        return self.text

    def save_to_file(self, file_path: str):
        with open(file_path, "w") as file:
            file.write(self.text)

    def resize_image(self, width, height) -> None:
        # Don't change the image if the input width and height can't be worked with at all
        if width == 0 and height == 0:
            return

        # If one dimension is 0, calculate new dimension based on the known one
        if width == 0:
            width = self.img.width * height // self.img.height
        elif height == 0:
            height = self.img.height * width // self.img.width

        self.img = self.original_image.resize((width, height), Image.NEAREST)

    def reverse_gradient(self):
        self.symbols = self.symbols[::-1]