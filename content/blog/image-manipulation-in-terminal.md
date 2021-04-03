+++
title = "Image manipulation in the terminal"
date = "2021-04-03T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Image","Manipulation","Terminal"]
categories = ["Tools"]
+++

Lately I have been in need of cropping some images, the easy thing to do would have been to install Gimp and do it there, but that is not fun.

I end up using **ImageMagick** to do some basic image manipulations. Since it took me few searches to find what I needed I decided to write a post in my blog so whenever I need it again, I know where I can find it easily.

## Crop Images

The most important part of the crop command is where the measures and offsets are provided. In the example below the output image will be of 600px by 500px with 10 offset from the X-axis and 20 offset from the Y-axis.

```bash
convert input_file.png -crop 600x500+10+20 output_file.png
```

## Add Transparency

If the image has a uniform background it can be replaced with an alpha-channel (transparency) with the following command. The mention of the color white in the command makes reference to the current background color that you want to replace with the transparency.

```bash
convert input_file.png -transparent white output_file.png
```

## The End?

I will keep updating this post with any other image manipulation commands that I find useful.