# Installing screenlamp

---

### PyPI

You can install the latest stable release of screenlamp from the Python Packaging Index directly using `pip`:

```bash
pip install screenlamp  
```

Alternatively, you can download the latest `screenlamp` release from the GitHub repository at [https://github.com/psa-lab/screenlamp/releases](https://github.com/psa-lab/screenlamp/releases), unzip it, and install it by executing

```bash
python setup.py install
```

### Upgrading via `pip`

To upgrade an existing version of screenlamp from PyPI, execute

```bash
pip install screenlamp --upgrade --no-deps
```

Please note that the dependencies (NumPy and SciPy) will also be upgraded if you omit the `--no-deps` flag; use the `--no-deps` ("no dependencies") flag if you don't want this.

### Dev Version

The screenlamp version on PyPI may always one step behind; you can install the latest development version from the GitHub repository by executing

```bash
pip install git+git://github.com/psa-lab/screenlamp.git
```

Or, you can fork the GitHub repository from https://github.com/rasbt/screenlamp and install screenlamp from your local drive via

```bash
python setup.py install
```
