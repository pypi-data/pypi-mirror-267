class printShape:
	"""Easily print various shapes on the terminal integer digits.
		You can print a huge variety of shapes- squares, rectangles, various triangles, diamonds, circles.
	"""
	def square(side, value=0,spacing=2):
		"""
			Print a Square pattern of integer digits.

			:param side: The sidelength of square.
        	:type side: int

			:param value: The integer used to make the pattern
			:type value: int

			:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
			:type  spacing: int
		"""
		for i in range(side):
			print((str(value)+(" "*spacing))*side)

	def rectangle( l, b, value=0, spacing=2):
		"""
			Print a Rectangle pattern of integer digits.

			:param l: The horizontal side length of Rectangle.
        	:type l: int

			:param b: The vertical side length of Rectangle.
        	:type b: int

			:param value: The integer used to make the pattern
			:type value: int

			:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
			:type  spacing: int
		"""
		for i in range(b):
			print((str(value)+(" "*spacing))*l)

	class triangle:
		class right:
			def bottom_left( h, b, value=0,spacing=2):
				"""
					Print a right angled triangle pattern of integer digits in the bottom left.

					:param h: The height of triangle.
					:type h: int

					:param b: The base length of triangle.
					:type b: int

					:param value: The integer used to make the pattern
					:type value: int

					:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
					:type  spacing: int
				"""
					for i in range(h):
						print((str(value)+(" "*spacing))*(int(b*(i+1)/h)))
			def top_left(h,b,value=0,spacing=2):
				"""
					Print a right angled triangle pattern of integer digits in the top left.

					:param h: The height of triangle.
					:type h: int

					:param b: The base length of triangle.
					:type b: int

					:param value: The integer used to make the pattern
					:type value: int

					:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
					:type  spacing: int
				"""
					for i in range(h,0,-1):
						print((str(value)+(" "*spacing))*(int(b*(i)/h)))
			def bottom_right( h, b, value=0,spacing=2):
				"""
					Print a right angled triangle pattern of integer digits in the bottom right.

					:param h: The height of triangle.
					:type h: int

					:param b: The base length of triangle.
					:type b: int

					:param value: The integer used to make the pattern
					:type value: int

					:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
					:type  spacing: int
				"""
					for i in range(h):
						printLen=int(b*(i+1)/h)
						print((str(value)*(b-printLen)+(" "*spacing))*printLen)
			def top_right(h,b,value=0,spacing=2):
				"""
					Print a right angled triangle pattern of integer digits in the top right.

					:param h: The height of triangle.
					:type h: int

					:param b: The base length of triangle.
					:type b: int

					:param value: The integer used to make the pattern
					:type value: int

					:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
					:type  spacing: int
				"""
					for i in range(h,0,-1):
						print(((" "*(spacing+1))*(b-(int(b*(i)/h))))+(str(value)+(" "*spacing))*(int(b*(i)/h)))

	def diamond(d, value=0, spacing=2):
		"""
			Print a diamond pattern of integer digits.

			:param d: The diagonal length of diamond.
        	:type d: int

			:param value: The integer used to make the pattern
			:type value: int

			:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
			:type  spacing: int
		"""
		if(d%2):
			for i in range(d):
				if(i<=(d-1)/2):
					print(" "*((1+spacing)*(int((d-1)/2)-i))+(str(value)+" "*spacing)*((2*i)+1))
				else:
					print(" "*((1+spacing)*(i-int((d-1)/2)))+(str(value)+" "*spacing)*(2*d-2*i-1))
		else:
			for i in range(d):
				if(i<d/2):
					print(" "*(1+spacing)*int(d/2-i-1)+(str(value)+" "*spacing)*2*(i+1)) 
				else:
					print(" "*(1+spacing)*(i-int(d/2))+(str(value)+" "*spacing)*2*(d-i)) 
	
	def circle(radius, value=0, spacing=2):
		"""
			Print a circular pattern of integer digits.

			:param radius: The radius of circle.
        	:type radius: int

			:param value: The integer used to make the pattern
			:type value: int

			:param spacing: Number of spaces between characters to make it look like an actual shape (Depends on your font tho, so adjust accordingly) 
			:type  spacing: int
		"""
		for y in range(-radius,radius+1):
			for x in range(-radius,radius+1):
				if(x*x+y*y<=radius*radius):
					print(value,end=(" "*spacing))
				else:
					print(" ",end=(" "*spacing))
			print("")