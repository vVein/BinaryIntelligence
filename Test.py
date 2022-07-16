

surrounding_pixels_weighted = [[33, 545, 67, 67, 67, 55], [31, 422, 26, 67, 67, 82], [33, 365, 67, 67, 67, 22]]

surrounding_pixels_weighted.sort(key = lambda surrounding_pixels_weighted : surrounding_pixels_weighted[5], reverse = True)

xyrgb_n = surrounding_pixels_weighted[0][0:5]

print(xyrgb_n)