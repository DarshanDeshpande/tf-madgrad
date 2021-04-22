<h2>MADGRAD Optimization Algorithm For Tensorflow</h2>

This package implements the MadGrad Algorithm proposed in <a href="https://arxiv.org/abs/2101.11075">Adaptivity without Compromise: A Momentumized, Adaptive, Dual Averaged Gradient Method for Stochastic Optimization</a> (Aaron Defazio and Samy Jelassi, 2021).


<!-- PROJECT SHIELDS -->
[![MIT License][license-shield]][license-url]
![version-shield]
![release-shield]
![python-shield]
![code-style]

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Citations</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The MadGrad algorithm of optimization uses Dual averaging of gradients along with momentum based adaptivity to attain results that match or outperform Adam or SGD + momentum based algorithms. This project offers a Tensorflow implementation of the algorithm along with a few usage examples and tests.
<br>

<img src="https://i.imgur.com/czLMClK.jpg" height="400px" width="700px"></img>
<br><br>

## Prerequisites

Prerequisites can be installed separately through the `requirements.txt` file as below

```sh
pip install -r requirements.txt
```


 
## Installation

This project is built with Python 3 and can be `pip` installed directly

```sh
pip install tf-madgrad
```

<!-- USAGE EXAMPLES -->
## Usage
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Tq6mH4ULsj7PzuOuMN13lOxSr_IbXgYq?usp=sharing)

To use the optimizer in any tf.keras model, you just need to import and instantiate the ```MadGrad``` optimizer from the `tf_madgrad` package.
```python
from madgrad import MadGrad

# Create the architecture
inp = tf.keras.layers.Input(shape=shape)
...
op = tf.keras.layers.Dense(classes, activation=activation)

# Instantiate the model
model = tf.keras.models.Model(inp, op)

# Pass the MadGrad optimizer to the compile function
model.compile(optimizer=MadGrad(lr=0.01), loss=loss)

# Fit the keras model as normal
model.fit(...)
```
This implementation is also supported for distributed training using ```tf.strategy```

See a MNIST example <a href="https://github.com/DarshanDeshpande/tf-madgrad/blob/master/examples/mnist_example.py">here</a> 

<!-- CONTRIBUTING -->
## Contributing

Any and all contributions are welcome. Please raise an issue if the optimizer gives incorrect results or crashes unexpectedly during training. 
<br>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact
Feel free to reach out for any issues or requests related to this implementation

Darshan Deshpande - [Email](https://mail.google.com/mail/u/0/?view=cm&fs=1&to=darshan1504@gmail.com&tf=1) | [LinkedIn](https://www.linkedin.com/in/darshan-deshpande/)



<!-- ACKNOWLEDGEMENTS -->
## Citations
```citation
@misc{defazio2021adaptivity,
      title={Adaptivity without Compromise: A Momentumized, Adaptive, Dual Averaged Gradient Method for Stochastic Optimization}, 
      author={Aaron Defazio and Samy Jelassi},
      year={2021},
      eprint={2101.11075},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/CONTRIBUTORS-1-orange?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[license-shield]: https://img.shields.io/badge/LICENSE-MIT-brightgreen?style=for-the-badge
[license-url]: https://github.com/DarshanDeshpande/tf-madgrad/blob/master/LICENSE.txt
[version-shield]: https://img.shields.io/badge/VERSION-1.0.0-orange?style=for-the-badge
[python-shield]: https://img.shields.io/badge/PYTHON-3.6%7C3.7%7C3.8-blue?style=for-the-badge
[release-shield]: https://img.shields.io/badge/Build-Stable-yellow?style=for-the-badge
[code-style]: https://img.shields.io/badge/Code_Style-Black-black?style=for-the-badge
