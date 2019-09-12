<h1 align="center">Open eyes using Deep Learning 👀 [WIP]</h1>
<p>
  <img src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
</p>
Have you ever had the perfect picture but closed your eyes? 🤦 It is a very common issue, you can fix it by going to Photoshop and editing the picture there.... But why not let an AI to do the hard work for us?

### Demo
You can find a demo in the following link: [https://overflow.ai/open-eyes-using-pix2pix](https://overflow.ai/open-eyes-using-pix2pix)

![](https://github.com/jesusmartinoza/Open-eyes-using-Pix2Pix/blob/master/assets/demo_1.png?raw=true)

### Motivation
The idea of this project had been in my head for a long time, I couldn't find the time to carry it out. Then the Youtuber [DotCSV](https://www.youtube.com/channel/UCy5znSnfMsDwaLlROnZ7Qbg) launched the challenge [#RetoDotCSV2080Super](https://www.youtube.com/watch?v=BNgAaCK920E) where you have to build a project using Pix2Pix model. So perfect timing to start to code.

### Dataset
This was the first big challenge. As you may know there is no dataset for people with open and closed eyes.  The dataset *Closed Eyes In The Wild(CEW)* is very useful but does not have a data labeled by person with open/closed eyes.

So what I propose is to generate the dataset **manually** with the help of OpenCV. Basically I take a picture from CEW dataset and overlay on it the eyes of a random photo of the UTKFace dataset. Then I manually clean the patches using Photoshop.

I did this process several times until I achieved a final dataset of **48 samples**.

![](https://github.com/jesusmartinoza/Open-eyes-using-Pix2Pix/blob/master/assets/training_process.png?raw=true)

### Training process
GIF: From FacePatcher image to (hopefully) Photoshop level

![](https://github.com/jesusmartinoza/Open-eyes-using-Pix2Pix/blob/master/assets/process.gif?raw=true)


### Results

### Future work and improvements
 - In order to achieve **better accuracy** it is necessary to increase the dataset samples and this way try with more interesting approaches to solve the task.
 - Currently the output of the app is a 256x256 picture. The output is only for the face, so a nice thing to do would be to **overlay** the result on the original photo.

### Author
Developed by Jesús Alberto Martínez Mendoza.

<a href="https://twitter.com/jesusmartinoza">
  <img alt="Twitter: Jesús" src="https://img.shields.io/twitter/follow/jesusmartinoza.svg?style=social" target="_blank" />
</a>

### Dataset credits
###### UTKFace dataset
```
Authors: Zhang, Zhifei, Song, Yang, and Qi, Hairong.
https://susanqq.github.io/UTKFace/
```

###### Closed Eyes In The Wild (CEW)
```
F.Song, X.Tan, X.Liu and S.Chen, Eyes Closeness Detection from Still Images with Multi-scale Histograms of Principal Oriented Gradients, Pattern Recognition, 2014.
```

### License
```
    The MIT License (MIT)

    Copyright (c) 2018 Jesús Alberto Martínez Mendoza(@jesusmartinoza)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

```
