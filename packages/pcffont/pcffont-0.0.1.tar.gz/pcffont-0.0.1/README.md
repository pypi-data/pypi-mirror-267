# PcfFont

[![Python](https://img.shields.io/badge/python-3.11-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/pcffont)](https://pypi.org/project/pcffont/)

PcfFont is a library for manipulating [Portable Compiled Format (PCF) Fonts](https://en.wikipedia.org/wiki/Portable_Compiled_Format).

## Installation

```shell
pip install pcffont
```

## Usage

```python
import os
import shutil

from examples import assets_dir, build_dir
from pcffont import PcfFont


def main():
    outputs_dir = os.path.join(build_dir, 'demo')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = PcfFont.load(os.path.join(assets_dir, 'unifont', 'unifont-15.1.05.pcf'))
    print(f'name: {font.properties.font}')
    print(f'size: {font.properties.pixel_size}')
    print(f'ascent: {font.accelerators.font_ascent}')
    print(f'descent: {font.accelerators.font_descent}')
    for code_point, glyph_index in sorted(font.bdf_encodings.items()):
        print(f'{code_point:04X} {chr(code_point)} - {font.glyph_names[glyph_index]}')
        for bitmap_row in font.bitmaps[glyph_index]:
            print(''.join(map(str, bitmap_row)).replace('0', '__').replace('1', '**'))
        print()
    font.save(os.path.join(outputs_dir, 'unifont-15.1.05.pcf'))


if __name__ == '__main__':
    main()
```

## Test Fonts

- [GNU Unifont Glyphs](https://unifoundry.com/unifont/index.html)
- [bitmap-fonts](https://github.com/masaeedu/bitmap-fonts)

## References

- [FontForge - The X11 PCF bitmap font file format](https://fontforge.org/docs/techref/pcf-format.html)

## License

Under the [MIT license](LICENSE).
