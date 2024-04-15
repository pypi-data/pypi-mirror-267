# ipgogogo

image to pdf, I(mage)P(DF)gogogo!

## envs

```text
pillow
loguru
```

run `pip install -r requirements.txt`

## usage

### for pypi

command line:

```python
import ipgogogo as ig
converter = ig.IPGoGoGo("input_dir", "output_dir")
converter.run()
```

ui:

```python
import ipgogogo as ig
ig.run_ui()
```

### for source code

```shell
python ipgogogo/run.py -i {input files dir path} -o {output files dir path} -l {log level}
```

## TODO

- [x] ui
