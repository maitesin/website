+++
title = "Resume Application"
description = "img/projects/resume.png"
+++

This resume is an **interactive application** written in **Go** and using the [Bubble Tea library](https://github.com/charmbracelet/bubbletea) it can be found in [https://github.com/maitesin/tui-cv/](https://github.com/maitesin/tui-cv/).

The idea for this project was inspired by [S0ulshake's CV](https://github.com/soulshake/cv.soulshake.net), however, I preferred to use other technologies, since I do not know JavaScript.

I have packaged the application inside a **Docker** image, so people can run it on their computers with the following command.

```bash
docker run -it --rm maitesin/resume
```
