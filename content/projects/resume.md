+++
title = "Resume Application"
description = "img/projects/resume.jpg"
+++

This resume is an **interactive application** written in **Rust** and it can be found in [https://github.com/maitesin/rust-cv/](https://github.com/maitesin/rust-cv/).

The idea for this project was inspired by [S0ulshake's CV](https://github.com/soulshake/cv.soulshake.net), however, I preferred to use other technologies, since I do not know JavaScript.

The **Rust** library I used for creating the UI is [tui](https://github.com/fdehau/tui-rs).

I have packaged the application inside a **Docker** image, so people can run it on their computers with the following command.

```bash
docker run -it maitesin/resume
```

You should get something similar to:

![cv](/img/projects/cv.gif)
