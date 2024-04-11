# Python SDK for Oogway AI

[![PyPI][pypi-badge]][pypi-url]
[![Supported Versions][ver-badge]][ver-url]
[![MIT licensed][mit-badge]][mit-url]

[pypi-badge]: https://img.shields.io/pypi/v/oogway_py
[pypi-url]: https://pypi.org/project/oogway_py
[ver-badge]: https://img.shields.io/pypi/pyversions/oogway_py.svg
[ver-url]: https://pypi.org/project/oogway_py
[mit-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[mit-url]: https://github.com/ngrok/ngrok-rust/blob/main/LICENSE-MIT

`oogway_py` is the official Python SDK for `Oogway AI` that requires no binaries. Quickly allow users to gain knowledge from Master Oogway in a few lines of code.

## Installation

The `oogway_py` SDK can be installed from [PyPI](https://pypi.org/project/oogway_py) via `pip`:

```shell
pip install oogway_py
```

## Quickstart

1. [Install `oogway_py`](#installation)
2. Export your `OPENAI_API_KEY` in your terminal
3. Add the following code to your application to add Oogway AI to your app:

    ```python
    # import oogway ai python sdk
    import asyncio
    import sys
    import oogway_py as oogway


    ai = oogway.Oogway()

    # change model name from python

    ai.model_name = "gpt-4-0125-preview"

    async def talk_to_oogway(question: str):
        print(f"\n> You : {question}");
        while True:
            print("\n> Oogway : ", end="");
            # python async generator for chunk streaming
            async for chunk in ai.ask(question):
                sys.stdout.write(chunk)
                sys.stdout.flush()
            question = input("\n\n> You: ")

    ```

That's it! Your application should now be able to allow users to converse with Master Oogway 🐢.

> **Note**
> You can run the example above from [the demo file](https://github.com/cs50victor/oogway_py/tree/main/python/oogway_py/demo.py).

Run `python python/oogway_py/demo.py` or checkout the [Jupyter Notebook Example](./example.ipynb)

## Demo

https://github.com/cs50victor/oogway_py/assets/52110451/aa762411-a8a9-4e50-a746-8374f8455700
