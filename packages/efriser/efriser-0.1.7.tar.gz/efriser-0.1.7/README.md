# EFRIS Package

This Python package provides a simple interface to interact with the EFRIS (Electronic Fiscal Receipt Information System) API provided by the Uganda Revenue Authority (URA) for invoicing.

## Features

- Create EFRIS invoices
- Retrieve the status of EFRIS invoices
- Easily integrate with your existing application

## Why I Created This Package

While working with the Uganda Revenue Authority (URA) API, I encountered numerous obstacles. My experiences led me to a deep understanding of the API's intricacies. This package is the result of my efforts to alleviate the "pain" for others—ensuring that you don't have to face the same challenges. Designed to be user-friendly, this guide will assist you, irrespective of your programming language, through the entire process from setting up the offline enabler to generating your first e-invoice. So grab a cup of chai and let's get started.

### Setting Up the Offline Enabler

1. **Download the Enabler**:
   Navigate to the [URA eFris test site](https://efristest.ura.go.ug/efrissite) and download the offline enabler. Follow the installation instructions provided on the website.

2. **Installation and Configuration**:
   After installation, you will receive an IP address from the enabler, for example, `199.82.32.128`. Append a port, such as `9880`, resulting in `http://199.82.32.128:9880` — this will serve as your base URL. To access the GUI of your enabler, visit `http://199.82.32.128:9880/efristcs`.

   Ensure you follow the detailed installation procedures in the guide to initialize your enabler and configure both a public and private key.

### Consuming the API

Once everything is set up, you're ready to dive into using the API to produce your e-invoices and more. The detailed steps provided in this guide will ensure a smooth experience as you integrate with the URA's systems.
