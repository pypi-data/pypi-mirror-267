# pyPrintShape
This is a library that lets you easily print various shapes on the terminal using integer digits.\
You can print a huge variety of shapes- squares, rectangles, various triangles, diamonds, circles.

You can find the package [here]()

The source code can be found [here](https://github.com/code-IM-perfect/pyPrintShapes)

## Installation
```
pip install pyPrintShape
```

## Usage
First you need to import the library.
```
from pyPrintShape import printShape
```

The following methods can be used for the actual printing-

### `printShape.square(side, value, spacing)`
Print a Square pattern of integer digits.

:param side: The sidelength of square.\
:type side: int

:param value:\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int

### `printShape.rectangle( l, b, value, spacing)`
Print a Rectangle pattern of integer digits.

:param l: The horizontal side length of Rectangle.\
:type l: int

:param b: The vertical side length of Rectangle.\
:type b: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int

### `printShape.triangle.right.bottom_left( h, b, value,spacing)`
Print a right angled triangle pattern of integer digits in the bottom left.

:param h: The height of triangle.\
:type h: int

:param b: The base length of triangle.\
:type b: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int


### `printShape.triangle.right.top_left( h, b, value,spacing)`
Print a right angled triangle pattern of integer digits in the top left.

:param h: The height of triangle.\
:type h: int

:param b: The base length of triangle.\
:type b: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int


### `printShape.triangle.right.bottom_right( h, b, value,spacing)`
Print a right angled triangle pattern of integer digits in the bottom right.

:param h: The height of triangle.\
:type h: int

:param b: The base length of triangle.\
:type b: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int


### `printShape.triangle.right.top_right( h, b, value,spacing)`
Print a right angled triangle pattern of integer digits in the top right.

:param h: The height of triangle.\
:type h: int

:param b: The base length of triangle.\
:type b: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int


### `printShape.diamond(d, value, spacing)`
Print a diamond pattern of integer digits.

:param d: The diagonal length of diamond.\
:type d: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int

### `printShape.circle(radius, value, spacing)`
Print a circular pattern of integer digits.

:param radius: The radius of circle.\
:type radius: int

:param value: The integer used to make the pattern\
:type value: int

:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) \
:type  spacing: int

