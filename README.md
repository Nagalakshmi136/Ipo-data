# ipopy

*ipopy* is a genuine, lightweight library for collecting details of newly launching ipo's in the market from different websites along with grey market premium and send this data to your whatsapp contact and email. It is designed to be simple and easy to use, allowing you to get the data you need with as few steps as possible.

## Documentation

Detailed documentation about the usage of the library can be found at [ipopy](https://nagalakshmi136.github.io/ipopy/). This is recommended for most cases. If you want to send ipo data to whatsapp contact the [quick start](#Quickstart) guide below might be what you're looking for.

## Description

The *ipopy* project is a lightweight library designed to collect details of newly launching IPOs in the market from different websites. It provides information about the IPOs, including the grey market premium, and allows you to send this data to your WhatsApp contacts and email. The library is built to be simple and easy to use, minimizing the steps required to obtain the desired data. With *ipopy*, you can quickly gather IPO information and stay updated with the latest market trends.

## Quickstart

This guide covers the most basic usage of the library. For more detailed information, please refer to [ipopy.io](https://nagalakshmi136.github.io/ipopy/).

### Installation

ipopy requires an installation of Python 3.6 or greater, as well as pip. (Pip is typically bundled with Python [installations](https://python.org/downloads).)

To install from PyPI with pip:

```bash
$ python -m pip install ipopy
```

Sometimes, the PyPI release becomes slightly outdated. To install from the source with pip:

```bash
$ python -m pip install git+https://github.com/Nagalakshmi136/ipopy
```
### Using ipopy in a Python script


```python
 >>> from ipopy.data_fetchers.all_fetchers import fetch_ipo_data

 >>> ipo_data = fetch_ipo_data
 >>> from ipopy.notifiers.whatsapp_notifier import WhatsappNotifier
 >>> WhatsappNotifier.send_notification(contact_name,
 ipo_data)
```

## Cloning the repository

Clone the repository through the terminal using the command below:

```shell
git clone https://github.com/Nagalakshmi136/ipopy.git
```

create conda enviroment with the following command:  

    $ conda create --name ipo-py python=3.12

If poetry not available install poetry:  

    $ sudo apt install poetry

Install required pacakages from poetry with the following command:  

    $ poetry install

To execute the code run the command:

    $ python main.py