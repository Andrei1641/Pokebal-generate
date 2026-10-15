# Tools
## TestTranslatorNumberOfBitsToRepresentNumber (count of bits in number)
| Testfallbeschreibung | Testdaten | Hypothese                                       | Testergebnis |
|----------------------|-----------|-------------------------------------------------|--------------|
| number is zero       | 0         | 0                                               | correct      |
| number is one        | 1         | 1                                               | correct      |
| positive number      | 50        | 6                                               | correct      |
| negative number      | -5        | ValueError("please write only positive number") | correct      |

## TestTranslatorFromIntToBytes
| Testfallbeschreibung                | Testdaten | Hypothese                                       | Testergebnis |
|-------------------------------------|-----------|-------------------------------------------------|--------------|
| number is zero                      | 0         | [0]                                             | correct      |
| positive number with multiple bytes | 300       | [1, 44]                                         | correct      |
| negative number                     | -300      | ValueError("please write only positive number") | correct      |

## TestTranslatorFromBytesToInt
| Testfallbeschreibung  | Testdaten | Hypothese  | Testergebnis |
|-----------------------|-----------|------------|--------------|
| byte is zero          | [0]       | 0          | correct      |
| multiple bytes        | [1, 44]   | 300        | correct      |
| byte part is negative | [1, -44]  | ValueError | correct      |

## TestTranslatorTranslateEndian
| Testfallbeschreibung | Testdaten | Hypothese | Testergebnis |
|----------------------|-----------|-----------|--------------|
| one byte             | [2]       | [2]       | correct      |
| multiple bytes       | [1, 44]   | [44, 1]   | correct      |

## TestTranslatorFillBytesBorder
| Testfallbeschreibung | Testdaten  | Hypothese     | Testergebnis |
|----------------------|------------|---------------|--------------|
| filled border        | [1, 44], 2 | [1, 44]       | correct      |
| fill empty           | [0], 2     | [0, 0]        | correct      |
| fill standard case   | [1, 44], 4 | [0, 0, 1, 44] | correct      |

## CreationProverIsOutOfBorder
| Testfallbeschreibung | Testdaten | Hypothese                      | Testergebnis |
|----------------------|-----------|--------------------------------|--------------|
| bigger               | 1, 256    | ValueError("false number 256") | correct      |
| negative number      | 1, -1     | ValueError("false number -1")  | correct      |
| inside               | 2, 256    | True                           | correct      |

# bitmap create
## file IO
### PictureCreator

expected_header_content = b'BMb\x01\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00,\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

header = WinHeader(
        354, 0, 54, 40, 10, 10, 1,
        24, 0,
        300, 0, 0, 0, 0
    )

expected_body_content = (b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00')


| Testfallbeschreibung | Testdaten                         | Hypothese               | Testergebnis |
|----------------------|-----------------------------------|-------------------------|--------------|
| write header         | header                            | expected_header_content | correct      |
| write body           | 10X10 white pixels(255, 255, 255) | expected_body_content   | correct      |

### PictureReaderFindPadding
| Testfallbeschreibung | Testdaten      | Hypothese | Testergebnis |
|----------------------|----------------|-----------|--------------|
| 24_depth             | 24, 10 ; 24, 4 | 2 ; 0     | correct      |
| 32_depth             | 32, 6          | 0         | correct      |

### ReadHeader
| Testfallbeschreibung    | Testdaten            | Hypothese                           | Testergebnis |
|-------------------------|----------------------|-------------------------------------|--------------|
| unexpected magic number | win_header, file.txt | TypeError                           | correct      |
| standard case           | win_header, file.bmp | readed_header is_subclass of Header | correct      |

### ReadWinHeader

win_header = WinHeader(
        354, 0, 54, 40, 10, 10, 1,
        24, 0,
        300, 0, 0, 0, 0
    )

| Testfallbeschreibung | Testdaten                                                     | Hypothese     | Testergebnis |
|----------------------|---------------------------------------------------------------|---------------|--------------|
| is data shifted      | win_header.bfOffbits ; win_header.bfSize ; win_header.biWidth | 54 ; 354 ; 10 | correct      |

### ReadRawBody

expected_raw_body = (b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00'
                            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00')


| Testfallbeschreibung | Testdaten                         | Hypothese         | Testergebnis |
|----------------------|-----------------------------------|-------------------|--------------|
| standard case        | 10X10 white pixels(255, 255, 255) | expected_raw_body | correct      |

### CreateCalculatePixels
| Testfallbeschreibung | Testdaten                         | Hypothese                                      | Testergebnis |
|----------------------|-----------------------------------|------------------------------------------------|--------------|
| unexpected header    | SomeHeader()                      | TypeError('unexpected header type SomeHeader') | correct      |
| standard case        | 10X10 white pixels(255, 255, 255) | pixel[9][9] is white                           | correct      |

## pixel
### 24Bit
| Testfallbeschreibung | Testdaten                                   | Hypothese     | Testergebnis |
|----------------------|---------------------------------------------|---------------|--------------|
| get color depth      | pixel is (blue = 255, green = 100, red = 0) | 24            | correct      |
| to bytes             | pixel is (blue = 255, green = 100, red = 0) | [255, 100, 0] | correct      |

## win body and head
### TranslateAttrInByteGetter
| Testfallbeschreibung | Testdaten | Hypothese | Testergebnis |
|----------------------|-----------|-----------|--------------|
| zero attr            | 0, 2      | [0, 0]    | correct      |
| attr multiple bytes  | 256, 3    | [0, 1, 0] | correct      |

### GetColorDepth
| Testfallbeschreibung | Testdaten            | Hypothese | Testergebnis |
|----------------------|----------------------|-----------|--------------|
| 24 bit               | pixel is (255, 0, 0) | 24        | correct      |

# bitmap calculate
## test frame
### FrameInit
| Testfallbeschreibung | Testdaten                     | Hypothese               | Testergebnis |
|----------------------|-------------------------------|-------------------------|--------------|
| standard case        | frame width = 10, height = 10 | width = 10, height = 10 | corerct      |

### FindNextPoint
| Testfallbeschreibung         | Testdaten                 | Hypothese | Testergebnis |
|------------------------------|---------------------------|-----------|--------------|
|                              | point on line             | 1         | correct      |
| positive slope line          | point left ; point right  | -1 ; 1    | correct      |
| negative slope line          | point left ; point right  | -1 ; 1    | correct      |
| vertical line (none slope)   | point left ; point right  | -1 ; 1    | correct      |
| horizontal lint (zero slope) | point below ; point upper | -1 ; 1    | correct      |

### DrawPoint
| Testfallbeschreibung | Testdaten                         | Hypothese           | Testergebnis |
|----------------------|-----------------------------------|---------------------|--------------|
| out of border        | frame 10X10, point(x = -5, y = 0) | no error            | correct      |
| standard case        | frame 10X10, point(x = 1, y = 1)  | pixel(x = 1, y = 1) | correct      |

### DrawLine
| Testfallbeschreibung | Testdaten                                    | Hypothese                                        | Testergebnis |
|----------------------|----------------------------------------------|--------------------------------------------------|--------------|
| out of border        | frame 10X10, line(point(-1, -1) point(9, 9)) | pixel(5, 5), pixel(0, 0), pixel(8, 8) are marked | correct      |
| standard case        | line(point(1, 1) point(9, 9))                | pixel(2, 2) is marked                            | correct      |

### DrawRectangle
| Testfallbeschreibung | Testdaten                                                               | Hypothese             | Testergebnis |
|----------------------|-------------------------------------------------------------------------|-----------------------|--------------|
| standard case        | rectangle(down left corner(0, 0), width = 5, height = 5)                | pixel(1, 1) is marked | correct      |
| out of border        | frame 10X10, rectangle(down left corner(-1, -1), width = 5, height = 5) | pixel(1, 1) is marked | correct      |

### MirrorPoint
| Testfallbeschreibung | Testdaten                               | Hypothese                                    | Testergebnis |
|----------------------|-----------------------------------------|----------------------------------------------|--------------|
| mirror_x             | point(0, 5), x=1 ; point(-5, 0), x=1    | point(-3, 0) ; point(7, 0)                   | correct      |
| mirror_y             | point(5, 0), y=1 ; point(0, -5), y=1    | point(0, -3) ; point(0, 7)                   | correct      |
| mirror_xy            | point(1, 1), x=0, y=0                   | point(-1, -1)                                | correct      |
| no value selected    | point(0, 0), no mirror line is selected | ValueError("select at least one of x and y") | correct      |

### DrawCircle
| Testfallbeschreibung | Testdaten                                   | Hypothese                                                                    | Testergebnis |
|----------------------|---------------------------------------------|------------------------------------------------------------------------------|--------------|
| standard case        | round(point(5, 5), radius = 5)              | pixel(5, 5), pixel(6, 6), pixel(0, 5) are marked                             | correct      |
| half                 | round(point(5, 5), radius = 5, half = True) | pixel(5, 5), pixel(6, 6), pixel(0, 5) are marked ; pixel(5, 4) is not marked | correct      |

### GetRenderPixels
| Testfallbeschreibung | Testdaten   | Hypothese                  | Testergebnis |
|----------------------|-------------|----------------------------|--------------|
| standard case        | frame 10X10 | 100 render pixels returned | correct      |

## figures
### Line
| Testfallbeschreibung  | Testdaten                                                                   | Hypothese                                         | Testergebnis |
|-----------------------|-----------------------------------------------------------------------------|---------------------------------------------------|--------------|
| init slope            | horizontal line ; positive slope line ; negative slope line ; constant line | slope = None ; slope > 0 ; slope < 0 ; slope == 0 | correct      |
| init shift            | line cross y on 0 ; line cross y on 1                                       | 0 ; 0                                             | correct      |
| set borders           | line(point(2, 0), point(1, 0)) ; line(point(0, 1), point(1, 0))             | (1, 2) ; (0, 1)                                   | correct      |
| calculate point side  |                                                                             |                                                   |              |
| horizontal line slope | left point ; right point ; point on line                                    | -1 ; 1 ; 1                                        | correct      |
| positive line slope   | left point ; right point ; point on line                                    | -1 ; 1 ; 1                                        | correct      |
| negative line slope   | left point ; right point ; point on line                                    | -1 ; 1 ; 1                                        | correct      |
| constant line slope   | left point ; right point ; point on line                                    | -1 ; 1 ; 1                                        | correct      |

### Round
| Testfallbeschreibung | Testdaten                                | Hypothese | Testergebnis |
|----------------------|------------------------------------------|-----------|--------------|
| get slope            | round                                    | 1         | correct      |
| calculate point side | point inside round ; point outside round | -1 ; 1    | correct      |

## pixels
### PixelXXBit
| Testfallbeschreibung | Testdaten                                                                     | Hypothese                               | Testergebnis |
|----------------------|-------------------------------------------------------------------------------|-----------------------------------------|--------------|
| set biggest number   | pixel(red = 50, green = 60, blue = 0) ; pixel(red = 100, green = 0, blue = 0) | 60 ; 100                                | correct      |
| mul                  | pixel * 5                                                                     | pixel are copies not links on one pixel | correct      |

### FindNeededDepth
| Testfallbeschreibung | Testdaten                                            | Hypothese                                                         | Testergebnis |
|----------------------|------------------------------------------------------|-------------------------------------------------------------------|--------------|
| unexpected bit depth | one of calculate pixels has red = 500(max - 255 now) | ValueError("there is no such bit-depth 500 to represent picture") | correct      |
| standard case        | calculate pixels -> 24Bit                            | no exeption                                                       | correct      |

### TranslateCalculateToRenderPixels
| Testfallbeschreibung | Testdaten            | Hypothese  | Testergebnis |
|----------------------|----------------------|------------|--------------|
| standard case        | pixel's colors < 255 | Pixel24Bit | correct      |

### NormalizePixels
| Testfallbeschreibung | Testdaten  | Hypothese                      | Testergebnis |
|----------------------|------------|--------------------------------|--------------|
| standard case        | 2X2 pixels | lengh of normalized pizels = 4 | correct      |
