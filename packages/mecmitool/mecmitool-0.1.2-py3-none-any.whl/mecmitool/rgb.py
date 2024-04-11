color_list_rgb={
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "cyan": (0, 255, 255),
    "blue": (0, 0, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (128, 128, 128),
    "brown": (165, 42, 42),
    "pink": (255, 192, 203),
    "purple": (128, 0, 128),
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "violet": (238, 130, 238),
    "indigo": (75, 0, 130),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "beige": (245, 245, 220),
    "turquoise": (64, 224, 208),
    "lavender": (230, 230, 250),
    "salmon": (250, 128, 114),
    "coral": (255, 127, 80),
    "khaki": (240, 230, 140),
    "tan": (210, 180, 140),
}
def rgb(color):
    return color_list_rgb[color]
def bgr(color):
    return (color_list_rgb[color][2], color_list_rgb[color][1], color_list_rgb[color][0])