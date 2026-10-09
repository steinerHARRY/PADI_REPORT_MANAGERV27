# created by H. Steiner, steinerh@telus.net
# all copyright reserved
# 24-08-2026 - V24.2 Specialty Worksheet save fix + visible PDF backdrop

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk, ImageOps
#from pdf2image import convert_from_path
import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DictionaryObject, NameObject, NumberObject, FloatObject,
    ArrayObject, DecodedStreamObject, TextStringObject, BooleanObject
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from reportlab.lib.utils import ImageReader
import re
import hashlib
import base64
from datetime import date

# Built-in cross-platform calendar support (no tkcalendar dependency).
import calendar as pycalendar

# ---------------- EMBEDDED APPLICATION LOGO ----------------
# Logo is stored directly in this source as Base64 PNG data.
EMBEDDED_LOGO_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAGcAAABmCAYAAADWHY9cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMA"
    "AA7DAcdvqGQAACH/SURBVHhe7Z13eBzVuf8/M9t3Je2qF6tastx7xTbYxjRjIDFJIJCEErg3hUsKNZQQSMIFfsnNTXJzUyAJIQkk"
    "hG6w6WCMbWxZ2LJs2eq9rbQqW7R9Z35/7GqtLbJXtrHFNZ/n2cfyObOzu/M95533vOc9ZwRZlmU+Y1IiRhd8xuRh0onjdDppaWmJ"
    "Lj4rmXTimM1mXn7xxejis5JJJ86Iw8Ghg4ewDg9HV511TDpxPG4PAwMD9Pb2RleddUwqcWRZxu1xY7NZMZvN0dVnHZNKHACr1YrD"
    "7sBisURXnXVMKnFkWaa/vx+/34/b5YquPuuYdOJ0tLfj8/lwfibO5BOnrq4ev9+Pz+uLrj7rmFTi+P1+mhoaCAQC+P2fiTOpxPH5"
    "fFgsFmRZxuV04fOd3QJNKnG8Hg8ejwdZlrHb7We9UzCpxHE5neG/Ozo66O/vj6g/25hU4gwND6NQKABoa2vD3NcXfchZxaQSx2q1"
    "IggCAObeXgZC95+zlUklTk93T1gcr9dL7ZFaRkZGog87a5hU4gxHRaJf3bz5rA6ATipx5i+YjyRJ4f93dXZS9fE+pEAg4rizBWEy"
    "5RAMDw+zZMHCiDKDwcCO3R+RnJwcUT5RJFlGkoJRCK9fwuuXUCtF1CoRAQFRBEEQCBrVyUFC4hw6eBCTyYRao0GlUqFUKsNeFYAk"
    "SQQCgdDI3k/A70cUFWTnZEec53j4/X5u+9732PralnCZLMt8+ZprePAnP0alUkUcfzwkSWZwxEvngJNddRZ21/VT12Nn2OHF7Qmg"
    "0yrJMWkpztSzuCyDpaVpFGcZSEvSoFaeeaOSkDj333sfh2tqMBqNZGZlkZaWil5vQBCCrc3lcuFwOLDb7AwODWGzWtHr9fzu8T9M"
    "qMXLsszbb73FN27+twjxAX7xq1+y8bLLYsrHY9DhZU+DhRd2d7C9xsygzYsggCgAgoAkRf5sWZZRKkXOnZnJpuUFzC9JoyBDT7JW"
    "RchHOe0kJI7dbuePjz/BKy+9RHt7OwgCSFLwX4ICjTL6tyiK3HPfvXzt+utRKpXh+uNRV1vHdV/9KgNR8zlpaWk88v8eY9355yOK"
    "x27V+5sHeXZnO8/ubMPu9KJSKijKNDAtL5ncVC0qhcig3UubZYT6bhvWkcgwkVatYE6RiWtXF/P55fkk6ybWY08VigcffPDB6MJo"
    "NBoN8+bPIzsnG0t/P5bQyF0QhJjXKLIs09TYSF5eHqVlZRF1x0KpVNLb08Ohgwcj3uN2u2mor6egqIjCwsK455NkmTcP9PLzlw7z"
    "6t5OvH6JDKOWa9eUcNMFpVy9uojLlkzh/Dk5rJ6VxZKydMpyk/H6JXqGXARCvckfkOkedDF9SgorpmegUSXWW081CYkDoFarmVpS"
    "wsxZs3E6R2hva8Pv90cfFsHIyAhNTU1kZ2dTXFx83BZPSByLxcI7b78dc/zQ0BBtra2UlpWRl5cXUScDb+zv4T+fP8SBtmFkGUx6"
    "FQ9fu4CvrClhdoERo16FUiGiEAV0agU5Jh2zC0wsLUtHEAQOtAwjhQzJjClGbr6wjLKc5DNm1hIWB0ChVJKVncXSpUtJy0jn48rK"
    "Y0aOZVlmaHCQQwcPkpGRQUlJyXHvGaIoIggC9XW1MWMcWZbp7+tjWvk05s2fHyHe7noLDzxzgIZue8gzk/nLrSu4eFEeyVrluF6Y"
    "QhRIT9awuDSdZIOKDw/3IctwwbwcvrKm+Iz1Gk5knCOKIhmZmdxw4428/OpmFixaGG5t8ZAkidaWVu65626e/POT+I8h5iizZs1i"
    "05VXYjQao6sIBAI4nS4CY8Y+vcMufvt6PfVdtvB3+caGaayfn5ew12XUq/iPS8r59oZyskxazpmZecbuNaNMqOeMRRAEUtPSuOzy"
    "y0lNTaWluRm32x0xiByL3+9nx4cfcrjmMLPnzMFgMIzrKAiCwIyZM7Fah6mvq4vonRqNhksu3cD8BQsAkGXYeaSfx16sCd+HNEqR"
    "f915bsLCjCIIArMKjAw6vFy9spAU/adUnFFUKhULFi5g5epVEAr7BwIBvF5v9KEIgkBLczNbt2xFFARMJhP6cURSKBQsXbYMr9eD"
    "dXgYp9OJ3+8nb0oel27cSMnUqQA43H6u+e8djLiP3v++cck0zp+bg3gCNwudRsHyaRmYktQoxIm//1Ry0uIQuugZGRmsXLWKhYsW"
    "kp+fj8lkIikpCZ/fj2vMpJkQGhdVVFRQXV2NFJDILyhAp9NFnJOQc7DinHNYvGQJgUCAg4cOYrPaMKWmsnDRQrRaLa9VdvLMB63h"
    "XiNJMg9dPY+CDEP06RJCEAQ0KsUZF4ZTJc4oCoWC7JwcFi5axHlr1rBw8SKmlZWRmpqKzWrF4XCEpwAkSaKnu4eq/ftZuGjhuO6x"
    "IAhkZmUyZ+5cGhsbaW1pobe3l0WLFpM3ZQpf+/Uu7K6jvUalVPD1C0rJNmojzvNpZGJGeQLo9XpmzpzJlV/8IrffeQcP/eQnXPH5"
    "z6MY42EJgoBSqUSlUsUVZizpGenccOMN5OTk0Gc28/gffk9bZx9t5sgphcJsA3pNrJn8NPKJiTPKqHd37przuOsHd/PYf/2cjIyM"
    "cH1JSQlZWVnHFUcURRYuWsRlV1yBJEns2rGTu//wJmKU+ZmSrkd7Bt3fU8knLs4ooiiSlZXFZZdfzp+e+gtlZWUAHDx0iN2798R1"
    "IKJJSkpi+YrlFBYWIvm97GiKTQDJN2rRqk7bz/pEOe2/QqlUMmvWLB77r59TXl6O1+3mpw89xMsvvnTMAe0oK845h2UrliNLASSF"
    "Prqa5gEnTu//jfmf0y4OoXvN3LlzufMHd1NYXITf7+e+e+7hpz/+CQ0NDcfsRTqdjvS0dJQqFQixX39vnYUBmye6+FPJKfXWJoIg"
    "CEyZMgWf18fB6mo8Hg8Hq6v5aNdOjKZUsrOz47rXgiDgdDrZV1mJJXUJshg5UJQkKMlOYklZ+gmNcyYTZ0wcQq53YWEBh6oP0tnZ"
    "GYzFDQ2xr7ISl8tJUVERKSkpMc6CqFCwfds2OhRTkVWRpk0QoKp1mJXTM5mSHmv2Pk3E2oXTTGZWFld+6YvoDUcHjQMDA/zj6ad5"
    "7NFHqa+ri0mPCs7KamE4/sJe64iXHz5zgJpOa3TVp4ozLo4gCKxdt47c3JyIcodjhHfeepsf3HU3FXv2RNQlJSWhVKnRdO8CIb7b"
    "/HHTIHf9ZR87aj+9WaNn1KyNolaryc7OYfMrr0RMA0iSRJ/ZzIcfbGfe/HlMyc+HkDlUKBRUbNuKLXftmDMdRRCge8jNnnoLAUmm"
    "fErKGQ3/nwgJTVOfDnw+H6uWr2BwcDC6CoDszHReem0LWdnBpJFAIMCG9edzZMSIe/YNIMePho+yvDyduzbNZuX0TJSKT4ejkJA4"
    "sgyNPTb8geikCMhJ05GWpI4oj0e/zc0b1b1YQ3Ewg1rB6vIMpuUeTQD5uLKSa66+GikQeaH9+mxGFnyLDKOO0vwsZGRAoKmrH8ug"
    "DUFjCs2FHhtZhiXT0vjyuSWsnJaOKUmNTq1Ar1FOikBnNAmLc+XPtlNRPxAxoyjJMt/aMI0ffnHumNL4PLerjQeeqabP6oZQaP47"
    "G2dw16ZZ4WN8Ph+3f//7bHn1tTEemox92heR8laEjztZZFlGr1VRmpvE0rJ0zpuVxawCI0UZhkklUkIOgSDAeTOy8HgDeHxHXz6/"
    "xJ5ayzFnQgF8fond9QMMO32IooAoCvj8Mp0DTkY8YyLKKhW3fuc7zJ4zJ8JDk7Lmhf8+FQiCgMvj51DrME++08Qtj+/l7r9V8ezO"
    "tnDjmQwkJA7AkrI0FHFsdUuf47g/aNDhpWtgBP8YcyXJMrVdNuq6bBHHlkydyj333ceGjZdiNBqRVMkIytjB6KnE6fazrbqX+54+"
    "wCMv1HC405qAkfzkSVicggwDpTlJ0cU43AF21R17z4CGHhtdg7FByuZeOw099ogypVLJsuXLuOfee/n+7beRPGNNzDhnFEEQkWUZ"
    "WQYZAUFQxLwQFAiiAgRh3POM4nD5eHZHG//1yhGaeiO/15kgYVdaluFIl42a9tiBXZZRy/p5keOUUQKSzJaPu3h1b3c4L2wUn19m"
    "frGJxaXpEbZeFEVSUlIom1bOW20quofip2Dp7PX864FNXLk8D5OrhcPvPo2qvxpl/4GIV6HQyc0bF3DRypmolSLNfSPj+g+SLNPa"
    "5wAZlk5LP6Pud8I9x6BVMr8oNeb+4pck6rtteP3xXVmnx0+HxYnbG3uBJVnmw9p+2i3x1+AoVBrsHmX86yiIiA1v8NTPfsDqmZls"
    "XDyFIlU/akt1xEtjqWbo8Da2PvEws7W9/OEbS3nnR+tZMDU9+oxhPD6J53d38N5BM8fpbJ8oCYujUoqU5iaRmqSJKJdl6Blyx5in"
    "UczDbpp67THxsVGqW4boHYo1eQCdFgce//hXR+my8MG2bdx849eZNXsWm67chBTwB8c8Y16SFKCzs5Pv3XILna1N9DdWcnFmO5pA"
    "5P1uLBarh/3Ngzjcx5/G+KRIWBwByE/TM6cgNpdswO5mX3Ps4FGWocnsYH/L+Ntz2V1+ugZdMWMogPdq+hiwxw//C/YOZCHoFlfs"
    "3s19P7gHu82GWj3+mMvhcHDbd7/Hv339Jn776I8QG7aOO3gVBNhVb6F7nIZzOkhYHIBMo5apOckxXd3hDtBidsRk7nv9Ei1mB0OO"
    "+BeY0fzmqp6YFuoLSFQ2DjDsjDe3I6Dqq4JAsC4QCLD9gw94/vnnj5siXF9fjyiKwfU4rgEEV2yjGqWm3Yp52B3frJ4GJiROik5F"
    "aU4SOk3kTdLjC9DWP8JQ1IV0uH0cbB0+7rzKriN9OMbknQFYR3xYR3zxG7YAKkcXgnT0PV6vd4L7FggIXjuCa/wV226PH5c3MK7z"
    "8EkzIXGUCoHyvGRyU2PHHc1mB409jogyi83Djtrxf/woQyM+mqNc10MdVtotzvhJ5B4r+I89tkoEQfIhhHpfPGRBoKmpicOHa6g+"
    "cICOjg6cp3EB8YTEASjLSWZKWqw43YPOCK9LBtosI3HHN9FIksxft7ce/b8sU90yGHRpYxBQDDUieGJd+okiKzVIUZN1YxFFBU/9"
    "+U/c8f3buOuOO7nlm9/koR89SF1t7XHHTKeCCYuTl6YjN00X06KtIz66LCP4Qi61LMvsa4yMxWnVCm7dWB5zzwLYWXN0Z0KPT8Ji"
    "9+D1xdo0QRCYX2gkK2X8G3/CqJJBO75LjeTD3NlOQ309jQ0NHK45zCsvv8yDD/yI6gMHPnGBJiyORqVgXnFqTJJ3QJKp6bDRH/Ku"
    "ApLMCxWdEcdMSdPxpVXFBKKizgAWu5cWc7Cn9FndtPaNxDQAgGS9khuvu5olS5bErN+ZELIMSi2yJtb7DOMaBH9kz/f7/VTs2cNd"
    "d9xJQ319RN2p5oR+3aKSNFINkeMdgEPtw+ExS9eAk+buyPvIJYunUJShpyA7Ngwky/CL1+oAqOuy8dE4IaFFJaksLUvn4Ucfoai4"
    "OLo6cQQxaNLE8bNDS5J9TCvMIis7O2JdkSAINDY08O1vfovaI0fGXVlxspyQOKU5SZgMscsjeoZcDNq9yDJsO9wX0fLVSpEL52aj"
    "Uyu5YV3J2LdBaFyxrboHj0+id9jN4Djjm6JMA0WZBkwmE7ffecdxF2ONh6Qy4E2bGV0cRhQFbrr6Yp7759/481+eZNW550bUC4JA"
    "a0sL/37zv7F3714Cx3HhT4QTEsdkUDOrwBgz9zHi9lPbZcXp8fPsh20RUYH8DD2ZRi2CAGtmZ8e114MOL1UtgzT22OJGFDQqBekp"
    "GpSK4Ne++JJLuPCii+Ke63jIWhOBtOnRxWE0shNbTyM+j4vpM2Zw1VVXxf2c7q4uHnrgR7z++uvU19XjHLPz1cmScOBzLKIg4PIG"
    "eLOqJyaYqVYpmFtk4tEXa8JlMnDpoilsWJQXnnV8Y38PwyORbqwsw5DLR1XrEJY4iYH5GXquXzeVqSGzKAgCs2bPYsurr0UsMzku"
    "goC78CIk43hmUUAYqKO/8iVaG2vp7Ojk5Rdforu7K/pACK1V3b9/P9UHDtDf10dJSQmGMdlEJ8oJ9RyAhVNTUcaZNTzSaWV3vYXA"
    "mHCMWimytCwNkyHoYaXoVFy6OC/Ga5NkmW3VZhqj7lWj5Jp0LCuL9K4KCgu5/c47SUlJiSg/Ft7kQnw5i0LNJg5+J+JwEz3NR9j8"
    "8iv85te/pqIiMgNoLJIk0dvTw0e7dvHHx5/g/ffeP26kIhFOWJz8dD1FY+b/R+kdcvOb1+sjsv8zUjTkpurCZlCtFFlQnBrXTDg9"
    "/rA7PhZBgGSdkuQoL1GhUHDF5z/HvfffR05uTtxzRiAocc+8FqIyRY8ioHT1o+6rgtCFt9vjN5Z4OBwOdn+065gpxYlywuKoFCKX"
    "L8yNLsYfkOiyRNrdeUUmSnOPemgKUaAg00B+VuJdX6tSsLg8I+6qaJ1Ox6YvfIFf/PKXzJw5/k1ekCXsC76BrE2LrgojBNwou3Yg"
    "esePWB+PqqoDeNyxZnminLA4AOvm5xA4jhupEAVmFxgpSI8UojjDwAVzEt8bJ1mn4pqVhdHFYRQKBcuWL+evT/+dNWvXxu6To1Dj"
    "mH0dUnJRZHkU4nAjGvM+gnH4E8NmtfLE44+zf9++iFXfE+WkxJmRlxIzvxONyaCmMDM2qyVZr6IkOynuQDMeBq0ibkwvmrT0dH79"
    "v7/hc1duorSslPTMLKSkXEamX40/Y07QPsZFQBzpxXDkHyclDEB6RgbX3XA9W159jb0VQTf7RMZCJ+StjaJSitR0WqntHN8ETM83"
    "ct26qTFrNEVRYMDuZXe9BceYNZ3jsWpmFpuWF0QXx0WtVrP+ggsom7sEiyKXQ/4y/KZpcZeMBBFQ2NrQH/4bos920uL4fT4uuXQD"
    "+QX5PPvPZ7Hb7djtdtLT0lAdY74pmpMSRwjFwV6t6Iw7LlGIAueUZ/DVNSXhsckoAqBRiVS3DtHU6xi/QYf4yTXzwy70sfD5JZr7"
    "HLxT3ctr1VY+bBewSuMHN0FGOdSAtmkzSqf5pIUhNH1hNpt59+13+LiyknfefpsDVQfQGwyUlpbGmtxxSCip8FjUd9tY+8N34npY"
    "eo2SWy+bzh1XxL9Ju70B7n/mAE+93xxdFYFKKdL0u8+hU0dGAyRZxuOTGLB76BpyUd9l41D7MPXdduq7bfQNH2daQfKh6j+ApuMD"
    "FE5zcKB1ipBlOarByuRNyecH997DpRs3jikfn5MWZ3jEy1f+eycVDQPRVeSl6njilhUsmxY/8ivL8LcPmnnkhZq4g85RFAqBL60s"
    "ihiVCMLohJwHh9vPiDuAzeVjeMQbt6FEk5UsYuj9CMuBNxB98aYmTj0yUFhQwLPPPxfO+T4WJy2Oxxfg568c4b83H4kxbYtL09h8"
    "z1rUx1hA29hr55u/q+BA61B0VQTRZpFQzxnNW0sEWYYkvYqbLijlxnUltNfX8LNHHuZgdXX0oZ8oX7r6Kh557LHo4hhif/EEUYUH"
    "lJHlggAz8o3HFIZQ0ogxgT1m/AEp5iVJxxZGCIWaFKJIaW4y9141h/0/38D9X5hNXqqO5csWs2bt2pObejgBbLbxHaixnHTPAahq"
    "HeKG3+ymd8AZvp+KgsA/b1/NebOyog+P4eebj/C/W+uC8/UnwOgGqkpRRK0U0ahEtCoF2Wk6lpels25uDgtLUlEJAYaGhmhtbWVf"
    "ZSWtLS0cOXyE2tM0s0loY6XH//RHVq1eHV0VwykRx2Lz8PSHrRzutIbFUStEfva1hWijbuLxaDbb+e2bDdijkjwSRSGKJGmVmPRq"
    "clO1FGcbmJaTTLYxuGWkz+ejs6ODXbt28drmzVTurQyPO6JN8SeJKIp87frrue+H9yfUW0+JOITseXQgcSI/PN77E8Xn99PR1o7Z"
    "3IvBYCArKwuj0YhSpWJoaIiPdu7ilZdfpmLPHjye8R2PE0WpVFIydSo6nY7W1lZs1vj5DWq1mn+9+AJz5syJrorLKRPnTOJyuXjr"
    "zTd54bnncDpdZGZlYTSmoNFoGbBYqKqqorenJ/ptYWRZRhSDSfETIdieZAoKCvjxwz8lOTmZXbt28fen/oogCOROyaO1uQWbzUZO"
    "bg7nrVnLrd+5lZzc2JhkPD614sihbY7r6+pQKJT09/fx3rvv0dnRET5GEAQkSQr34NG/ZVkmKSmJ7JwciouLKCubRvmM6bz5+hu8"
    "/dZbCfV4WZZZsXIl69atY8bMGaxctQpRFOnr6+PWb9/C166/jtKyMjo7OjCbzUydOpXy8nLS0tMTMml8msXx+Xx8/frr2b9/P0pF"
    "MA/A7Xbj8/mQZZn8/Hw2bLyUjIxM3G43IGNKTUWn05Gbm4spNRVjSgoarRatVotOp2NocIirv/Ql+szmcMhfFEX0ej2GJAM5ObkY"
    "jUZ0Wi11dfU8+JOHWLR4MWq1OnzBt27Zwt6Kvdx2+20kp6SEN0NPZGesaD614hAS40BVFW9sfZ19oQjwOeecw4UXX8S8+fPHvSBC"
    "1DbLY3G7XLg9noj5GL1ej1KpRKkIrvORJIn7772Xm266ieljpigcDgePPPwwF118Meeed17CPWQ8PtXijCU4GA3eOz5pZFnmxw8+"
    "yFevu47S0lII5Wu/unkzPT09XHPttZhMpui3TZhP/pecJgRBOC3CEPosgyGJEYcDSZJwuVx8XFlJR3sH69atOyXC8H+p55xuKioq"
    "aG1uwWQyMTQ8xODAAIuXLGHJ0qWnrJF8Js4JIssylZWVNNY3oFQqWbJ0CcUlJePey06Ez8Q5SUYv36kUZZSExdnfaCEvJ4Xs0G4d"
    "h1uHGHQHWD0juF+nw+WjuW+E/HQ91c2DLJ+ZhSjLNPbYyUrXkxm1y4ckybT0OdhZa8GgU7F+bjamMQFQSZKpbhumosFCTrqBSxbk"
    "og4ttR8YdlLb52RxSVp4y8hBu4chp4+CDEP4OELLHncc6Q9PghZkJ7OkyBi+mPXdNpRKkVStku11A1yxZErExJ950Emnw8e8Kcns"
    "PNLPqplZdPQ7cPplynOTUIei5QNWN73Dbqblp0SUvVvTh8sbYFl5BtNykuKmk41Hwsbx/epe3q8J7sAkSzK/2lrH/c8eDNe39tp5"
    "p8bMoNPHr16tZcgrYXd6eWNvJw39kQl/sixTUd/PN39fwZZ9Xfz9/SY+9+h2PKFcN68vwJ/ebuC7T37M+zV9/H5rLVc8sh3LSDD2"
    "1tQ1zAN//Zhe69FQTFufnQ+O9OHwRs7l1Hfb+Olzh3jirUb++HYTN/9qF9f8z57wMsdt1b3srB1ArRK588+V2DyRwdffv9VAs8WF"
    "2xPgt1vqcfoC7Krt5zt/+pjm/qNZRs1mB1v3deMKff72Q2Yu+vH7/GtXO1sqO/nm7/bw6r4e/FFJmMciYXFK85JpCiX72Uc8SChQ"
    "BAIMuYNfpmPAiUalJDNFg8cnIcnBeJkvIMWswPZ4A+xrtPCV9eU8e9tqXrz7PC6cmcp/bm1ClmF7jZkddQP8z81L+cf3V7Hl/nWs"
    "n5XO957YiywHe5U/IHHvv2rC0ThJlmOyTwlNNayfm82r965l6/1r2f3oRYxYnfzuw3YILW/0BySUKiVT0rTUjdkKWZZlajttzM5J"
    "QpZlPL7gKjd/QKbLbOONA2ZGPzIgBR83JgM2u5s7nvyYH1+/mOfuWM2zt6/mh1+YyXsHzfQdY1IxmoTFKcww0DPkQpKDu3aU5RtZ"
    "X57K3nYrgYBEv92LRiGQlEAU2heQGRj2UpqbTEAKTufedNF0tH4/Hp+ftj4Hy8ozmFcYXJ4hCALXnV+KIMjUWVwgw1Vryqip66XW"
    "PLHcZJ1GyZP/sZwX3mnAG85KDf5756XT+Mv29rDgnWYb6RnJZKdEZhhJksS1a0t4cWcrnXGmwv/5YSvnLy9m47wshND3Xzc3h6lZ"
    "enxxFiaPR8LipCZrUQsyVk+Ahi4b0wtNLJmRxTv7unH7AvgCEmlJmoROqFGLFOca+Pu7DbxR1cPhLhspSVru2TQDh9OH2eqhrDAy"
    "8c+oV3FeeSrvHwouslLptdz3hZl8+w978cXpMcdCp9egVoAtaoriwqUF7D/UHd5d9+2DfSyemkaSNrbBFWYls2FOJr99ozHGVB1s"
    "G2b93Mh5LFGh4LuXllOUfvz0rlESuZYQ2iQiL1VD+4CT+j4neSkq5hencqhlEIfLjz8gk5fg8wPUSgVr5+VRYNLw9ActPPxCDb98"
    "rY4+hw+3T8Lm8ZOdGplKpRRF0gxqLKPLGGWZi5cWka6UeG2/eUKzDQKgUIg4QiZ5FJVaxfRcA039LqSARFu/i8K04JxQNLIMN64v"
    "ZVtVF9WdR9N1ZVnG6vJj1AcdoBG3n3eqenjy3SaefLeJtoHEE+5jP3UcdGoFGSlaatuG8UrB/dIyTXpUcoCOYTf+gERJgum1MpCd"
    "quO7V8zkrs/P5PJFubT0WHn0xcOIIqhEAXfUkkNZlvEFJDRhsymjEAUe+PJcfv96HQ6fNDoplBCSJKNRxXpOX1yRz1sHzfQMOklJ"
    "0TAlXR98CF8MAsZkHXdsnMZvttbh8gc/XwBUCiGcCesPSPQMumjosfPMBy009CVuhhMWR6tWkJWioaplkBSDmmSdClEpsrgohb3t"
    "NqxuP+n68VeJjWXA6uJnLx9Br1GxoCSNq1YVcfemWbz8URtJWhVZyWoaOiI3lnB6A1R32Zk1NdLczSpK49wyI//Y1YEqzq5W8ZAC"
    "wZSqlDjmak5xGjWNFnY3DpKkUZAb1YOjuXxFIR6Xh48aBoPuuSCQm6qjqTeY0ZOsU3HF8ny+f/kM5hUaj5ufN5aExVGKIil6NR19"
    "drJM2vByjvlT06iotWDQqMb14WNKBYHGHisHQtt5iYKAUa9CFEQMWhWZRh1VzYMMj8kEbTfbONzhYM201DEnCmblXLw4n3f3d9Mx"
    "nFhm//M7mpk+NR1dnE2HDDoVBSY19T0j6DVKkqL2XIhGo1byrQtLeWZbEwOhpyZeuSKfP7/dyMBIcH85o0FNql5FIPS4skRJWByE"
    "4APqrCNeRIHwl56el0JlbR8l+fGDfdYRD29UdvHke808+X4z/9jRjsmg5sI52dz+x0qe2t7K5souvvqLnfzHlXNQKATWzcnGM+Lm"
    "rr9Vsbmymyffb+KqX37EDRumkxzHG5ydb+TfzyscZyd2gYYeO3/7oIWntrVwx18+5ofP1vDTL8+Na65SDSoWFqWwv8PKjKJUFAk0"
    "9RmFqczOS8YZ2thvUXkWa6emsOGn2/j7jjZerujkW3+o4GCnnYLj9MSxTDgd1ycJzC4wURDyOpRKkV6rm8uW5WPSKkGGmrZhzp2b"
    "g1qQOdI2TFXrMA09dhq67XQNu9m0LJ/i7CT0Snhpdwd7Gge5fGUR37kw+DSpJJ2KecWptPba+dfOVnqsXn50zQIumRP0gKwjHvyi"
    "grIsAyqFgEqlQFYq8MsCC4pT0SiPXlCby8eOw/009Nip77FhNGj47S0ryTcG3eOeIRemJC2l2UkoxGBk2xsQEGSZ9XOz0YQeLRaQ"
    "ZOq77Jw3J5shu4ckvZqp2QaUoScnFqTpCciwqDQNtVLkvLk5pGoVvLS7g521FmYWp/HAVXMpm0DyfsLhm884/SRu1j7jtPOZOJOY"
    "z8SZxHwmziTmM3EmMf8fxDefoDmkaREAAAAASUVORK5CYII="
)


editing_active = False
current_inline_entry = None

reopened_exported_pdf = False
loaded_pdf_values = {}
pdf_field_mapping = {}
pdf_field_rects = {}
tooltip_window = None
# ---------------- APPLICATION / RESOURCE PATHS ----------------

import sys
import os

# Platform flags used by Tk event bindings and diagnostics.
IS_MACOS = (sys.platform == "darwin")

# ---------------- STABLE CROSS-PLATFORM DATE PICKER ----------------
class StableDatePicker(ttk.Frame):
    """Small calendar picker implemented only with Tk/ttk.

    This replaces tkcalendar.DateEntry and avoids dropdown/grab behavior
    that can be unreliable in Aqua Tk inside a frozen macOS application.
    """
    def __init__(self, master, width=12, date_pattern="yyyy-mm-dd", **kwargs):
        for key in ("background", "foreground", "borderwidth", "selectbackground", "selectforeground"):
            kwargs.pop(key, None)
        super().__init__(master, **kwargs)
        self._selected_date = date.today()
        self._display_var = tk.StringVar()
        self._popup = None
        self._view_year = self._selected_date.year
        self._view_month = self._selected_date.month

        self._entry = ttk.Entry(self, width=width, textvariable=self._display_var, state="readonly")
        self._entry.pack(side="left", fill="x")
        self._button = ttk.Button(self, text="▼", width=2, command=self._open_calendar)
        self._button.pack(side="left", padx=(2, 0))
        self._entry.bind("<Button-1>", lambda e: self._open_calendar())
        self._refresh_display()

    def _refresh_display(self):
        self._display_var.set(self._selected_date.strftime("%Y-%m-%d"))

    def get_date(self):
        return self._selected_date

    def set_date(self, value):
        if isinstance(value, date):
            new_date = value
        elif isinstance(value, str):
            value = value.strip()
            parsed = None
            from datetime import datetime
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
                try:
                    parsed = datetime.strptime(value, fmt).date()
                    break
                except ValueError:
                    pass
            if parsed is None:
                raise ValueError(f"Unsupported date format: {value}")
            new_date = parsed
        else:
            new_date = date(int(value.year), int(value.month), int(value.day))
        self._selected_date = new_date
        self._view_year = new_date.year
        self._view_month = new_date.month
        self._refresh_display()

    def _close_calendar(self):
        popup = self._popup
        self._popup = None
        if popup is not None:
            try:
                if popup.winfo_exists():
                    popup.destroy()
            except tk.TclError:
                pass

    def _open_calendar(self):
        if self._popup is not None:
            try:
                if self._popup.winfo_exists():
                    self._popup.lift()
                    self._popup.focus_force()
                    return
            except tk.TclError:
                self._popup = None

        self._view_year = self._selected_date.year
        self._view_month = self._selected_date.month
        popup = tk.Toplevel(self)
        self._popup = popup
        popup.title("Select Date")
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())
        popup.protocol("WM_DELETE_WINDOW", self._close_calendar)
        popup.bind("<Escape>", lambda e: self._close_calendar())

        # Deliberately do not use grab_set() on macOS/Aqua Tk.
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 3
        popup.geometry(f"+{x}+{y}")

        self._calendar_body = ttk.Frame(popup, padding=6)
        self._calendar_body.pack(fill="both", expand=True)
        self._render_calendar()
        popup.after(25, lambda: self._safe_focus_popup(popup))

    def _safe_focus_popup(self, popup):
        try:
            if popup.winfo_exists():
                popup.lift()
                popup.focus_set()
        except tk.TclError:
            pass

    def _change_month(self, amount):
        month = self._view_month + amount
        year = self._view_year
        while month < 1:
            month += 12
            year -= 1
        while month > 12:
            month -= 12
            year += 1
        self._view_year = year
        self._view_month = month
        self._render_calendar()

    def _choose_day(self, day):
        chosen = date(self._view_year, self._view_month, int(day))
        self._selected_date = chosen
        self._refresh_display()
        self._close_calendar()
        self.event_generate("<<DateEntrySelected>>", when="tail")

    def _render_calendar(self):
        body = self._calendar_body
        for child in body.winfo_children():
            child.destroy()

        header = ttk.Frame(body)
        header.grid(row=0, column=0, columnspan=7, sticky="ew", pady=(0, 5))
        ttk.Button(header, text="◀", width=3, command=lambda: self._change_month(-1)).pack(side="left")
        ttk.Label(header, text=f"{pycalendar.month_name[self._view_month]} {self._view_year}", anchor="center", width=20).pack(side="left", padx=4)
        ttk.Button(header, text="▶", width=3, command=lambda: self._change_month(1)).pack(side="left")

        for col, name in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
            ttk.Label(body, text=name, anchor="center", width=4).grid(row=1, column=col, padx=1, pady=(0, 2))

        weeks = pycalendar.monthcalendar(self._view_year, self._view_month)
        for row_index, week in enumerate(weeks, start=2):
            for col, day_num in enumerate(week):
                if day_num == 0:
                    ttk.Label(body, text="", width=4).grid(row=row_index, column=col, padx=1, pady=1)
                else:
                    ttk.Button(body, text=str(day_num), width=3, command=lambda d=day_num: self._choose_day(d)).grid(row=row_index, column=col, padx=1, pady=1)

        ttk.Button(body, text="Today", command=self._select_today).grid(row=2 + len(weeks), column=0, columnspan=7, pady=(5, 0))

    def _select_today(self):
        today = date.today()
        self._view_year = today.year
        self._view_month = today.month
        self._choose_day(today.day)

import copy
import tempfile
import traceback
import shutil

APP_NAME = "PADI Manager"
APP_VERSION = "V27"

# ---------------- SINGLE-INSTANCE APPLICATION GUARD ----------------
# Keep this handle/file descriptor alive for the lifetime of the process.
# The operating system automatically releases it if the program crashes.
_SINGLE_INSTANCE_HANDLE = None


def _ensure_single_instance():
    global _SINGLE_INSTANCE_HANDLE
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateMutexW.argtypes = (ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR)
        kernel32.CreateMutexW.restype = wintypes.HANDLE
        # Local namespace: one instance per Windows logon session.
        handle = kernel32.CreateMutexW(None, False, "Local\\PADI_Manager_HSteiner_SingleInstance")
        if not handle:
            raise OSError(ctypes.get_last_error(), "Unable to create application mutex")
        error = ctypes.get_last_error()
        if error == 183:  # ERROR_ALREADY_EXISTS
            kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
            kernel32.CloseHandle(handle)
            return False
        _SINGLE_INSTANCE_HANDLE = handle
        return True

    # macOS / Linux: an advisory OS file lock, released on process termination.
    import fcntl
    import tempfile
    lock_path = Path(tempfile.gettempdir()) / f"padi_manager_{os.getuid()}_single_instance.lock"
    lock_file = open(lock_path, "a+b")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (BlockingIOError, OSError):
        lock_file.close()
        return False
    _SINGLE_INSTANCE_HANDLE = lock_file
    return True


def _show_already_running_message():
    message = "PADI Manager is already running.\n\nPlease use the existing window."
    if os.name == "nt":
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, message, "PADI Manager", 0x40)
    else:
        # Only create a short-lived dialog; do not start the main application.
        try:
            dialog_root = tk.Tk()
            dialog_root.withdraw()
            messagebox.showinfo("PADI Manager", message, parent=dialog_root)
            dialog_root.destroy()
        except Exception:
            print(message, file=sys.stderr)


if not _ensure_single_instance():
    _show_already_running_message()
    sys.exit(0)


def _get_resource_dir():
    """Return the directory containing read-only bundled application resources."""
    if not getattr(sys, "frozen", False):
        return Path(__file__).resolve().parent

    candidates = []

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass))

    executable = Path(sys.executable).resolve()
    candidates.append(executable.parent)

    if sys.platform == "darwin":
        # Typical .app layout:
        # App.app/Contents/MacOS/App
        candidates.append(executable.parent.parent / "Resources")
        candidates.append(executable.parent.parent)

    # Prefer a candidate containing the bundled logo or other known resource.
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0] if candidates else Path.cwd()


def _get_user_data_dir():
    """Return a writable per-user data directory.

    The application bundle/install directory is never used for mutable data.
    This is important on macOS, where an installed .app is commonly read-only.
    """
    if sys.platform == "darwin":
        data_dir = Path.home() / "Library" / "Application Support" / APP_NAME
    elif os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        data_dir = Path(root) / APP_NAME if root else Path.home() / APP_NAME
    else:
        data_dir = Path.home() / ".padi_manager"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


RESOURCE_DIR = _get_resource_dir()
DATA_DIR = _get_user_data_dir()

# BASE_DIR is retained as the resource directory for existing resource paths.
BASE_DIR = RESOURCE_DIR

# Mutable application data belongs in the user's writable data directory.
DB_FILE = DATA_DIR / "instructors.json"
SIGNATURE_DIR = DATA_DIR / "signatures"
STATE_FILE = DATA_DIR / "state_padi.json"
COMMENTS_FILE = DATA_DIR / "comments.json"
SIGNATURE_DIR.mkdir(parents=True, exist_ok=True)

# Clean source PDFs are cached here. Exported PDFs contain a flattened/static
# appearance layer, so re-exporting an exported PDF directly would stack the
# old appearance under the new one. Keeping a clean source prevents that.
TEMPLATE_CACHE_DIR = DATA_DIR / "template_cache"
TEMPLATE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

current_base_pdf_path = None
current_base_id = None

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _cache_clean_template(path):
    """Cache a pristine PDF and return (base_id, cached_path)."""
    path = Path(path).expanduser().resolve()
    base_id = _sha256_file(path)
    cached = TEMPLATE_CACHE_DIR / f"{base_id}.pdf"
    if not cached.exists():
        shutil.copy2(path, cached)
        print("CACHED CLEAN TEMPLATE =", cached)
    return base_id, cached

def _base_id_from_pdf(path):
    """Read PADI Manager's clean-template ID from an exported PDF."""
    try:
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        value = metadata.get("/PADIManagerBaseID")
        return str(value) if value else None
    except Exception as e:
        print("BASE ID READ WARNING:", e)
        return None

def _cached_base_for_id(base_id):
    if not base_id:
        return None
    candidate = TEMPLATE_CACHE_DIR / f"{base_id}.pdf"
    return candidate if candidate.exists() else None

def _single_cached_template():
    """Compatibility fallback for legacy exports made before base IDs existed."""
    candidates = sorted(TEMPLATE_CACHE_DIR.glob("*.pdf"))
    return candidates[0] if len(candidates) == 1 else None


def resolve_signature_path(value):
    """Resolve a saved signature path across Windows/macOS/Linux."""
    if not value:
        return None

    text = str(value)
    candidate = Path(text).expanduser()

    if candidate.exists():
        return candidate

    # A state file created on Windows can contain backslashes. On macOS/Linux
    # those are not path separators, so normalize them before taking basename.
    portable_name = Path(text.replace("\\", "/")).name
    if portable_name:
        candidate = SIGNATURE_DIR / portable_name
        if candidate.exists():
            return candidate

    return Path(text)


def _migrate_legacy_user_data():
    """Migrate old writable files from the application directory once.

    The master mask is deliberately excluded. Existing user databases and
    signatures are moved/copied into the platform-appropriate user-data
    directory so an installed macOS .app never needs write access to itself.
    """
    legacy_files = ("instructors.json", "state_padi.json", "comments.json")

    for filename in legacy_files:
        source = RESOURCE_DIR / filename
        target = DATA_DIR / filename
        if source.exists() and not target.exists():
            try:
                shutil.copy2(source, target)
                print("MIGRATED:", source, "->", target)
            except Exception as e:
                print("LEGACY DATA MIGRATION WARNING:", source, e)

    legacy_signatures = RESOURCE_DIR / "signatures"
    if legacy_signatures.exists() and legacy_signatures.is_dir():
        try:
            for source in legacy_signatures.iterdir():
                target = SIGNATURE_DIR / source.name
                if source.is_file() and not target.exists():
                    shutil.copy2(source, target)
                    print("MIGRATED SIGNATURE:", source, "->", target)
        except Exception as e:
            print("SIGNATURE MIGRATION WARNING:", e)


_migrate_legacy_user_data()


def _atomic_json_write(path, data):
    """Write JSON atomically in the writable user-data directory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.stem}_",
        suffix=".tmp",
        dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        Path(temp_name).replace(path)
        return True
    except Exception:
        try:
            Path(temp_name).unlink(missing_ok=True)
        except Exception:
            pass
        raise


print("RESOURCE_DIR =", RESOURCE_DIR)
print("DATA_DIR =", DATA_DIR)
print("COMMENTS_FILE =", COMMENTS_FILE)
# ---------------- ZOOM SETTINGS ----------------

zoom_level_def = 0.50
ZOOM_STEP =0.1
MIN_ZOOM = 0.3
MAX_ZOOM = 3.0
zoom_level = zoom_level_def

# ---------------- Instructor Database ----------------

def load_instructors():
    if not DB_FILE.exists():
        return {"instructors": []}
    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return {"instructors": []}
    if "instructors" not in data:
        data["instructors"] = []
    return data

def save_instructors(data):
    try:
        _atomic_json_write(DB_FILE, data)
        return True
    except Exception as e:
        messagebox.showerror("Instructor Error", f"Failed to save instructor data:\n{e}")
        return False

db = load_instructors()
instructor_list = db["instructors"]

# ---------------- PDF Comments (embedded in the PDF) ----------------
# Legacy comments.json is read only for migration; new comments are never
# written to a separate JSON database.
PDF_COMMENT_KEY = "/PADIManagerComment"

def load_comments_db():
    if not COMMENTS_FILE.exists():
        return {}
    try:
        with COMMENTS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print("LEGACY COMMENT LOAD WARNING:", e)
        return {}

comments_db = {}

def _comment_identity(pdf_file):
    path = str(Path(pdf_file).resolve()) if pdf_file else ""
    filename = Path(pdf_file).name if pdf_file else ""
    path_key = hashlib.sha256(path.encode("utf-8")).hexdigest() if path else ""
    student = str(state.get("Student Name", "")).strip() if "state" in globals() else ""
    return path_key, filename, student

def _legacy_comment(pdf_file):
    path_key, filename, student = _comment_identity(pdf_file)
    record = comments_db.get(path_key)
    if isinstance(record, dict):
        return str(record.get("comment", ""))
    for record in comments_db.values():
        if (isinstance(record, dict) and record.get("filename") == filename
                and student and record.get("student_name") == student):
            return str(record.get("comment", ""))
    return ""

def get_saved_comment(pdf_file):
    """Prefer the PDF's own metadata, falling back to legacy comments.json."""
    if not pdf_file or not Path(pdf_file).is_file():
        return ""
    try:
        metadata = PdfReader(str(pdf_file)).metadata
        if metadata is not None and PDF_COMMENT_KEY in metadata:
            return str(metadata.get(PDF_COMMENT_KEY) or "")
    except Exception as e:
        print("PDF COMMENT READ WARNING:", e)
    return _legacy_comment(pdf_file)

def _metadata_with_comment(reader, comment):
    metadata = {}
    try:
        for key, value in (reader.metadata or {}).items():
            if isinstance(key, str) and isinstance(value, str):
                metadata[key] = value
    except Exception:
        pass
    metadata[PDF_COMMENT_KEY] = str(comment or "")
    return metadata

def _write_comment_into_existing_pdf(pdf_file, comment):
    """Rewrite PDF atomically to embed a comment without losing form fields."""
    target = Path(pdf_file).expanduser().resolve()
    if not target.is_file():
        raise FileNotFoundError(target)
    reader = PdfReader(str(target))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.add_metadata(_metadata_with_comment(reader, comment))
    temp = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=".padi_comment_", suffix=".pdf",
            dir=str(target.parent), delete=False
        ) as f:
            temp = Path(f.name)
            writer.write(f)
        temp.replace(target)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()

def save_comment_for_pdf(pdf_file, comment):
    if not pdf_file:
        messagebox.showerror("Comment", "Load a PDF before saving a comment.")
        return False
    try:
        _write_comment_into_existing_pdf(pdf_file, comment)
        return True
    except Exception as e:
        messagebox.showerror("Comment", f"Could not embed note in PDF:\\n{e}")
        return False

def display_comment(pdf_file):
    """Restore the PDF-embedded comment into the existing Comments box."""
    if "comment_text" not in globals():
        return
    comment_text.delete("1.0", "end")
    if pdf_file:
        saved = get_saved_comment(pdf_file)
        if saved:
            comment_text.insert("1.0", saved)
    update_comment_box_color()
    comment_text.see("1.0")

def save_current_comment(pdf_file=None):
    target = pdf_file or globals().get("pdf_path")
    if not target or "comment_text" not in globals():
        return False
    comment = comment_text.get("1.0", "end-1c").strip()
    return save_comment_for_pdf(target, comment)


# PDF converter  
def convert_from_path(pdf_path, dpi=200):
    """Render a PDF with PDFium while releasing native objects promptly.

    Explicit cleanup is important in a long-running frozen macOS app because
    PDFium bitmaps can otherwise retain substantial native memory.
    """
    pdf = pdfium.PdfDocument(str(pdf_path))
    rendered_pages = []
    scale = dpi / 72.0

    try:
        for page_index in range(len(pdf)):
            page = None
            bitmap = None
            try:
                page = pdf[page_index]
                bitmap = page.render(scale=scale)
                image = bitmap.to_pil().convert("RGB")
                # Detach PIL image data from the PDFium bitmap before closing it.
                image.load()
                rendered_pages.append(image.copy())
                image.close()
            finally:
                if bitmap is not None:
                    try:
                        bitmap.close()
                    except Exception:
                        pass
                if page is not None:
                    try:
                        page.close()
                    except Exception:
                        pass
    finally:
        try:
            pdf.close()
        except Exception:
            pass

    return rendered_pages
# ---------------- Field Map + State ----------------

# ---------------- EMBEDDED MASTER MASK ----------------
# The master 10056 OW Records mask is embedded directly in this source.
# No external mask JSON file is required or consulted at runtime.
HARDCODED_MASK = {
    "fields": [
        {
            "name": "Student Name",
            "type": "text",
            "page": 0,
            "x1": 204,
            "y1": 177,
            "x2": 625,
            "y2": 206
        },
        {
            "name": "Birth Date",
            "type": "text",
            "page": 0,
            "x1": 160,
            "y1": 223,
            "x2": 222,
            "y2": 252
        },
        {
            "name": "undefined",
            "type": "text",
            "page": 0,
            "x1": 242,
            "y1": 223,
            "x2": 304,
            "y2": 252
        },
        {
            "name": "undefined_2",
            "type": "text",
            "page": 0,
            "x1": 324,
            "y1": 223,
            "x2": 386,
            "y2": 252
        },
        {
            "name": "Mailing address 1",
            "type": "text",
            "page": 0,
            "x1": 215,
            "y1": 284,
            "x2": 625,
            "y2": 314
        },
        {
            "name": "Mailing address 2",
            "type": "text",
            "page": 0,
            "x1": 75,
            "y1": 340,
            "x2": 315,
            "y2": 369
        },
        {
            "name": "Mailing address 3",
            "type": "text",
            "page": 0,
            "x1": 325,
            "y1": 340,
            "x2": 427,
            "y2": 369
        },
        {
            "name": "Mailing address 4",
            "type": "text",
            "page": 0,
            "x1": 436,
            "y1": 340,
            "x2": 502,
            "y2": 369
        },
        {
            "name": "Mailing address 5",
            "type": "text",
            "page": 0,
            "x1": 512,
            "y1": 340,
            "x2": 625,
            "y2": 369
        },
        {
            "name": "undefined_3",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 419,
            "x2": 337,
            "y2": 448
        },
        {
            "name": "undefined_4",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 419,
            "x2": 625,
            "y2": 448
        },
        {
            "name": "undefined_5",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 459,
            "x2": 337,
            "y2": 489
        },
        {
            "name": "undefined_6",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 459,
            "x2": 625,
            "y2": 489
        },
        {
            "name": "undefined_7",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 500,
            "x2": 337,
            "y2": 529
        },
        {
            "name": "undefined_8",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 500,
            "x2": 625,
            "y2": 529
        },
        {
            "name": "Email",
            "type": "text",
            "page": 0,
            "x1": 125,
            "y1": 540,
            "x2": 625,
            "y2": 569
        },
        {
            "name": "init_padi_instructor_1",
            "type": "text",
            "page": 0,
            "x1": 204,
            "y1": 691,
            "x2": 625,
            "y2": 720
        },
        {
            "name": "Init_Instructor_Signature_1",
            "type": "signature",
            "page": 0,
            "x1": 165,
            "y1": 731,
            "x2": 625,
            "y2": 760
        },
        {
            "name": "Init_PADI_no_1",
            "type": "text",
            "page": 0,
            "x1": 155,
            "y1": 772,
            "x2": 275,
            "y2": 801
        },
        {
            "name": "Init_Dive_Resort_No_1",
            "type": "text",
            "page": 0,
            "x1": 494,
            "y1": 772,
            "x2": 625,
            "y2": 801
        },
        {
            "name": "Init_day_1",
            "type": "text",
            "page": 0,
            "x1": 114,
            "y1": 817,
            "x2": 177,
            "y2": 846
        },
        {
            "name": "Init_month_1",
            "type": "text",
            "page": 0,
            "x1": 197,
            "y1": 817,
            "x2": 259,
            "y2": 846
        },
        {
            "name": "Init_year_1",
            "type": "text",
            "page": 0,
            "x1": 279,
            "y1": 817,
            "x2": 341,
            "y2": 846
        },
        {
            "name": "undefined_11",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 889,
            "x2": 337,
            "y2": 919
        },
        {
            "name": "Init_Phone_1",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 889,
            "x2": 625,
            "y2": 919
        },
        {
            "name": "undefined_13",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 930,
            "x2": 337,
            "y2": 959
        },
        {
            "name": "undefined_14",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 930,
            "x2": 625,
            "y2": 959
        },
        {
            "name": "Init_Email_1",
            "type": "text",
            "page": 0,
            "x1": 125,
            "y1": 970,
            "x2": 625,
            "y2": 1000
        },
        {
            "name": "Init_padi_instructor_2",
            "type": "text",
            "page": 0,
            "x1": 204,
            "y1": 1035,
            "x2": 625,
            "y2": 1065
        },
        {
            "name": "Init_Instructor_Signature_2",
            "type": "signature",
            "page": 0,
            "x1": 165,
            "y1": 1076,
            "x2": 625,
            "y2": 1105
        },
        {
            "name": "Init_PADI_no_2",
            "type": "text",
            "page": 0,
            "x1": 155,
            "y1": 1116,
            "x2": 275,
            "y2": 1145
        },
        {
            "name": "Init_Dive_Resort_No_2",
            "type": "text",
            "page": 0,
            "x1": 494,
            "y1": 1116,
            "x2": 625,
            "y2": 1145
        },
        {
            "name": "Init_day_2",
            "type": "text",
            "page": 0,
            "x1": 114,
            "y1": 1162,
            "x2": 177,
            "y2": 1191
        },
        {
            "name": "Init_month_2",
            "type": "text",
            "page": 0,
            "x1": 197,
            "y1": 1162,
            "x2": 259,
            "y2": 1191
        },
        {
            "name": "Init_year_2",
            "type": "text",
            "page": 0,
            "x1": 279,
            "y1": 1162,
            "x2": 341,
            "y2": 1191
        },
        {
            "name": "undefined_17",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 1229,
            "x2": 337,
            "y2": 1258
        },
        {
            "name": "Init_Phone_2",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 1229,
            "x2": 625,
            "y2": 1258
        },
        {
            "name": "undefined_19",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 1269,
            "x2": 337,
            "y2": 1298
        },
        {
            "name": "undefined_20",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 1269,
            "x2": 625,
            "y2": 1298
        },
        {
            "name": "Init_Email_2",
            "type": "text",
            "page": 0,
            "x1": 125,
            "y1": 1309,
            "x2": 625,
            "y2": 1338
        },
        {
            "name": "CW2_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 244,
            "x2": 803,
            "y2": 273
        },
        {
            "name": "CW2_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 244,
            "x2": 893,
            "y2": 273
        },
        {
            "name": "CW2_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 244,
            "x2": 985,
            "y2": 273
        },
        {
            "name": "CW3_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 277,
            "x2": 803,
            "y2": 306
        },
        {
            "name": "CW3_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 277,
            "x2": 893,
            "y2": 306
        },
        {
            "name": "CW3_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 277,
            "x2": 985,
            "y2": 306
        },
        {
            "name": "CW4_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 310,
            "x2": 803,
            "y2": 339
        },
        {
            "name": "CW4_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 310,
            "x2": 893,
            "y2": 339
        },
        {
            "name": "CW4_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 310,
            "x2": 985,
            "y2": 339
        },
        {
            "name": "CW1_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 210,
            "x2": 1086,
            "y2": 239
        },
        {
            "name": "CW2_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 244,
            "x2": 1086,
            "y2": 273
        },
        {
            "name": "CW3_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 277,
            "x2": 1086,
            "y2": 306
        },
        {
            "name": "CW4_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 310,
            "x2": 1086,
            "y2": 339
        },
        {
            "name": "CW1_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 210,
            "x2": 803,
            "y2": 239
        },
        {
            "name": "CW1_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 210,
            "x2": 893,
            "y2": 239
        },
        {
            "name": "CW1_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 210,
            "x2": 985,
            "y2": 239
        },
        {
            "name": "CW1_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 210,
            "x2": 1192,
            "y2": 239
        },
        {
            "name": "CW15_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 211,
            "x2": 1407,
            "y2": 239
        },
        {
            "name": "CW15_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 211,
            "x2": 1498,
            "y2": 239
        },
        {
            "name": "CW15_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 211,
            "x2": 1588,
            "y2": 239
        },
        {
            "name": "undefined_32",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 211,
            "x2": 1761,
            "y2": 239
        },
        {
            "name": "CW15_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 211,
            "x2": 1983,
            "y2": 239
        },
        {
            "name": "CW15_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 211,
            "x2": 2117,
            "y2": 239
        },
        {
            "name": "CW2_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 244,
            "x2": 1192,
            "y2": 273
        },
        {
            "name": "CW16_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 240,
            "x2": 1407,
            "y2": 270
        },
        {
            "name": "CW16_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 240,
            "x2": 1498,
            "y2": 270
        },
        {
            "name": "CW16_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 240,
            "x2": 1588,
            "y2": 270
        },
        {
            "name": "undefined_38",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 240,
            "x2": 1761,
            "y2": 270
        },
        {
            "name": "CW16_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 240,
            "x2": 1983,
            "y2": 270
        },
        {
            "name": "CW16_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 240,
            "x2": 2117,
            "y2": 270
        },
        {
            "name": "CW3_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 277,
            "x2": 1192,
            "y2": 306
        },
        {
            "name": "CW17_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 271,
            "x2": 1407,
            "y2": 300
        },
        {
            "name": "CW17_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 271,
            "x2": 1498,
            "y2": 300
        },
        {
            "name": "CW17_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 271,
            "x2": 1588,
            "y2": 300
        },
        {
            "name": "undefined_44",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 271,
            "x2": 1761,
            "y2": 300
        },
        {
            "name": "CW17_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 271,
            "x2": 1983,
            "y2": 300
        },
        {
            "name": "CW17_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 271,
            "x2": 2117,
            "y2": 300
        },
        {
            "name": "CW4_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 310,
            "x2": 1192,
            "y2": 339
        },
        {
            "name": "CW18_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 302,
            "x2": 1407,
            "y2": 331
        },
        {
            "name": "CW18_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 302,
            "x2": 1498,
            "y2": 331
        },
        {
            "name": "CW18_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 302,
            "x2": 1588,
            "y2": 331
        },
        {
            "name": "undefined_50",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 302,
            "x2": 1761,
            "y2": 331
        },
        {
            "name": "CW18_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 302,
            "x2": 1983,
            "y2": 331
        },
        {
            "name": "CW18_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 302,
            "x2": 2117,
            "y2": 331
        },
        {
            "name": "CW5_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 343,
            "x2": 803,
            "y2": 373
        },
        {
            "name": "CW5_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 343,
            "x2": 893,
            "y2": 373
        },
        {
            "name": "CW5_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 343,
            "x2": 985,
            "y2": 373
        },
        {
            "name": "CW5_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 343,
            "x2": 1086,
            "y2": 373
        },
        {
            "name": "CW5_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 343,
            "x2": 1192,
            "y2": 373
        },
        {
            "name": "CW19_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 332,
            "x2": 1407,
            "y2": 361
        },
        {
            "name": "CW19_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 332,
            "x2": 1498,
            "y2": 361
        },
        {
            "name": "CW19_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 332,
            "x2": 1588,
            "y2": 361
        },
        {
            "name": "undefined_58",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 332,
            "x2": 1761,
            "y2": 361
        },
        {
            "name": "CW19_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 332,
            "x2": 1983,
            "y2": 361
        },
        {
            "name": "CW19_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 332,
            "x2": 2117,
            "y2": 361
        },
        {
            "name": "CW20_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 375,
            "x2": 1407,
            "y2": 404
        },
        {
            "name": "CW20_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 375,
            "x2": 1498,
            "y2": 404
        },
        {
            "name": "CW20_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 375,
            "x2": 1588,
            "y2": 404
        },
        {
            "name": "CW20_quizz",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 375,
            "x2": 1761,
            "y2": 404
        },
        {
            "name": "CW20_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 375,
            "x2": 1983,
            "y2": 404
        },
        {
            "name": "CW20_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 375,
            "x2": 2117,
            "y2": 404
        },
        {
            "name": "CW6_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 486,
            "x2": 1086,
            "y2": 516
        },
        {
            "name": "CW6_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 486,
            "x2": 803,
            "y2": 516
        },
        {
            "name": "CW6_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 486,
            "x2": 893,
            "y2": 516
        },
        {
            "name": "CW6_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 486,
            "x2": 985,
            "y2": 516
        },
        {
            "name": "CW6_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 486,
            "x2": 1192,
            "y2": 516
        },
        {
            "name": "Instructor_signature_4",
            "type": "signature",
            "page": 0,
            "x1": 1379,
            "y1": 480,
            "x2": 1690,
            "y2": 509
        },
        {
            "name": "PADI_no_4",
            "type": "text",
            "page": 0,
            "x1": 1717,
            "y1": 480,
            "x2": 1832,
            "y2": 509
        },
        {
            "name": "day_4",
            "type": "text",
            "page": 0,
            "x1": 1888,
            "y1": 480,
            "x2": 1970,
            "y2": 509
        },
        {
            "name": "month_4",
            "type": "text",
            "page": 0,
            "x1": 1990,
            "y1": 480,
            "x2": 2043,
            "y2": 509
        },
        {
            "name": "year_4",
            "type": "text",
            "page": 0,
            "x1": 2063,
            "y1": 480,
            "x2": 2117,
            "y2": 509
        },
        {
            "name": "CW7_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 559,
            "x2": 985,
            "y2": 589
        },
        {
            "name": "CW7_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 559,
            "x2": 1086,
            "y2": 589
        },
        {
            "name": "CW7_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 559,
            "x2": 1192,
            "y2": 589
        },
        {
            "name": "CW7_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 559,
            "x2": 803,
            "y2": 589
        },
        {
            "name": "CW7_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 559,
            "x2": 893,
            "y2": 589
        },
        {
            "name": "CW8_initials",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 676,
            "x2": 1086,
            "y2": 705
        },
        {
            "name": "CW8_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 676,
            "x2": 1192,
            "y2": 705
        },
        {
            "name": "CW22_day",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 641,
            "x2": 1328,
            "y2": 671
        },
        {
            "name": "CW22_month",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 641,
            "x2": 1402,
            "y2": 671
        },
        {
            "name": "CW22_year",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 641,
            "x2": 1475,
            "y2": 671
        },
        {
            "name": "CW21_initials",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 612,
            "x2": 1547,
            "y2": 637
        },
        {
            "name": "CW22_initials",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 641,
            "x2": 1547,
            "y2": 671
        },
        {
            "name": "CW22_padi",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 641,
            "x2": 1654,
            "y2": 671
        },
        {
            "name": "CW24_day",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 641,
            "x2": 1781,
            "y2": 671
        },
        {
            "name": "CW24_month",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 641,
            "x2": 1854,
            "y2": 671
        },
        {
            "name": "CW24_year",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 641,
            "x2": 1928,
            "y2": 671
        },
        {
            "name": "CW23_initials",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 612,
            "x2": 2010,
            "y2": 637
        },
        {
            "name": "CW24_initials",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 641,
            "x2": 2010,
            "y2": 671
        },
        {
            "name": "CW21_day",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 612,
            "x2": 1328,
            "y2": 637
        },
        {
            "name": "CW21_month",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 612,
            "x2": 1401,
            "y2": 637
        },
        {
            "name": "CW21_year",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 612,
            "x2": 1475,
            "y2": 637
        },
        {
            "name": "CW21_padi",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 612,
            "x2": 1654,
            "y2": 637
        },
        {
            "name": "CW23_day",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 612,
            "x2": 1781,
            "y2": 637
        },
        {
            "name": "CW23_month",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 612,
            "x2": 1854,
            "y2": 637
        },
        {
            "name": "CW23_year",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 612,
            "x2": 1928,
            "y2": 637
        },
        {
            "name": "CW23_padi",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 612,
            "x2": 2117,
            "y2": 637
        },
        {
            "name": "CW24_padi",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 641,
            "x2": 2117,
            "y2": 671
        },
        {
            "name": "CW8_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 676,
            "x2": 803,
            "y2": 705
        },
        {
            "name": "CW8_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 676,
            "x2": 893,
            "y2": 705
        },
        {
            "name": "CW8_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 676,
            "x2": 985,
            "y2": 705
        },
        {
            "name": "CW9_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 756,
            "x2": 1086,
            "y2": 785
        },
        {
            "name": "CW9_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 756,
            "x2": 1192,
            "y2": 785
        },
        {
            "name": "CW9_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 756,
            "x2": 803,
            "y2": 785
        },
        {
            "name": "CW9_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 756,
            "x2": 893,
            "y2": 785
        },
        {
            "name": "CW9_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 756,
            "x2": 985,
            "y2": 785
        },
        {
            "name": "Dive_2",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 773,
            "x2": 1779,
            "y2": 803
        },
        {
            "name": "CW10_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 835,
            "x2": 803,
            "y2": 864
        },
        {
            "name": "CW10_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 835,
            "x2": 985,
            "y2": 864
        },
        {
            "name": "CW10_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 835,
            "x2": 1086,
            "y2": 864
        },
        {
            "name": "CW10_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 835,
            "x2": 1192,
            "y2": 864
        },
        {
            "name": "Dive_3",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 804,
            "x2": 1779,
            "y2": 833
        },
        {
            "name": "CW10_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 835,
            "x2": 893,
            "y2": 864
        },
        {
            "name": "Dive_4",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 835,
            "x2": 1779,
            "y2": 864
        },
        {
            "name": "CW11_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 915,
            "x2": 1192,
            "y2": 944
        },
        {
            "name": "Dive_5",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 865,
            "x2": 1779,
            "y2": 894
        },
        {
            "name": "CW11_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 915,
            "x2": 803,
            "y2": 944
        },
        {
            "name": "Dive_6",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 896,
            "x2": 1779,
            "y2": 925
        },
        {
            "name": "CW11_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 915,
            "x2": 893,
            "y2": 944
        },
        {
            "name": "CW11_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 915,
            "x2": 985,
            "y2": 944
        },
        {
            "name": "CW11_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 915,
            "x2": 1086,
            "y2": 944
        },
        {
            "name": "Dive_7",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 926,
            "x2": 1779,
            "y2": 956
        },
        {
            "name": "CW12_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 994,
            "x2": 1086,
            "y2": 1024
        },
        {
            "name": "CW12_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 994,
            "x2": 1192,
            "y2": 1024
        },
        {
            "name": "Dive_8",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 957,
            "x2": 1779,
            "y2": 986
        },
        {
            "name": "CW12_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 994,
            "x2": 803,
            "y2": 1024
        },
        {
            "name": "CW12_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 994,
            "x2": 893,
            "y2": 1024
        },
        {
            "name": "CW12_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 994,
            "x2": 985,
            "y2": 1024
        },
        {
            "name": "Dive_9",
            "type": "text",
            "page": 0,
            "x1": 1698,
            "y1": 988,
            "x2": 1778,
            "y2": 1017
        },
        {
            "name": "Dive_initials_1",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 744,
            "x2": 1912,
            "y2": 772
        },
        {
            "name": "Dive_initials_2",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 773,
            "x2": 1912,
            "y2": 803
        },
        {
            "name": "Dive_initials_3",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 804,
            "x2": 1912,
            "y2": 833
        },
        {
            "name": "Dive_initials_4",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 835,
            "x2": 1912,
            "y2": 864
        },
        {
            "name": "Dive_initials_5",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 865,
            "x2": 1912,
            "y2": 894
        },
        {
            "name": "Dive_initials_6",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 896,
            "x2": 1912,
            "y2": 925
        },
        {
            "name": "Dive_initials_7",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 926,
            "x2": 1912,
            "y2": 956
        },
        {
            "name": "Dive_initials_8",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 957,
            "x2": 1912,
            "y2": 986
        },
        {
            "name": "Dive_1",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 744,
            "x2": 1779,
            "y2": 772
        },
        {
            "name": "Dive_padi_1",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 744,
            "x2": 2081,
            "y2": 772
        },
        {
            "name": "Dive_padi_2",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 773,
            "x2": 2081,
            "y2": 803
        },
        {
            "name": "Dive_padi_3",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 804,
            "x2": 2081,
            "y2": 833
        },
        {
            "name": "Dive_padi_4",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 835,
            "x2": 2081,
            "y2": 864
        },
        {
            "name": "Dive_padi_5",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 865,
            "x2": 2081,
            "y2": 894
        },
        {
            "name": "Dive_padi_6",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 896,
            "x2": 2081,
            "y2": 925
        },
        {
            "name": "Dive_padi_7",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 926,
            "x2": 2081,
            "y2": 956
        },
        {
            "name": "Dive_padi_8",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 957,
            "x2": 2081,
            "y2": 986
        },
        {
            "name": "Dive_padi_9",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 988,
            "x2": 2081,
            "y2": 1017
        },
        {
            "name": "CW13_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1083,
            "x2": 985,
            "y2": 1113
        },
        {
            "name": "CW13_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 1083,
            "x2": 1086,
            "y2": 1113
        },
        {
            "name": "CW13_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1083,
            "x2": 1192,
            "y2": 1113
        },
        {
            "name": "Dive_10",
            "type": "text",
            "page": 0,
            "x1": 1698,
            "y1": 1018,
            "x2": 1778,
            "y2": 1047
        },
        {
            "name": "Dive_padi_10",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 1018,
            "x2": 2081,
            "y2": 1047
        },
        {
            "name": "CW13_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1083,
            "x2": 803,
            "y2": 1113
        },
        {
            "name": "CW13_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1083,
            "x2": 893,
            "y2": 1113
        },
        {
            "name": "CW14_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1172,
            "x2": 985,
            "y2": 1202
        },
        {
            "name": "CW14_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 1172,
            "x2": 1086,
            "y2": 1202
        },
        {
            "name": "CW14_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1172,
            "x2": 1192,
            "y2": 1202
        },
        {
            "name": "Instructor_signature_5",
            "type": "signature",
            "page": 0,
            "x1": 1379,
            "y1": 1128,
            "x2": 1690,
            "y2": 1158
        },
        {
            "name": "PADI_no_5",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1128,
            "x2": 1814,
            "y2": 1158
        },
        {
            "name": "day_5",
            "type": "text",
            "page": 0,
            "x1": 1863,
            "y1": 1128,
            "x2": 1935,
            "y2": 1158
        },
        {
            "name": "month_5",
            "type": "text",
            "page": 0,
            "x1": 1954,
            "y1": 1128,
            "x2": 2026,
            "y2": 1158
        },
        {
            "name": "year_5",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 1128,
            "x2": 2117,
            "y2": 1158
        },
        {
            "name": "CW14_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1172,
            "x2": 803,
            "y2": 1202
        },
        {
            "name": "CW14_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1172,
            "x2": 893,
            "y2": 1202
        },
        {
            "name": "student_signature",
            "type": "signature",
            "page": 0,
            "x1": 1370,
            "y1": 1316,
            "x2": 1814,
            "y2": 1345
        },
        {
            "name": "Stu_day",
            "type": "text",
            "page": 0,
            "x1": 1869,
            "y1": 1316,
            "x2": 1940,
            "y2": 1345
        },
        {
            "name": "Stu_month",
            "type": "text",
            "page": 0,
            "x1": 1960,
            "y1": 1316,
            "x2": 2030,
            "y2": 1345
        },
        {
            "name": "Stu_year",
            "type": "text",
            "page": 0,
            "x1": 2051,
            "y1": 1316,
            "x2": 2122,
            "y2": 1345
        },
        {
            "name": "Instructor_signature_3",
            "type": "signature",
            "page": 0,
            "x1": 819,
            "y1": 1353,
            "x2": 1192,
            "y2": 1383
        },
        {
            "name": "PADI_no_3",
            "type": "text",
            "page": 0,
            "x1": 721,
            "y1": 1409,
            "x2": 890,
            "y2": 1438
        },
        {
            "name": "day_3",
            "type": "text",
            "page": 0,
            "x1": 940,
            "y1": 1409,
            "x2": 1011,
            "y2": 1438
        },
        {
            "name": "month_3",
            "type": "text",
            "page": 0,
            "x1": 1031,
            "y1": 1409,
            "x2": 1102,
            "y2": 1438
        },
        {
            "name": "year_3",
            "type": "text",
            "page": 0,
            "x1": 1122,
            "y1": 1409,
            "x2": 1193,
            "y2": 1438
        },
        {
            "name": "Instructor_signature_6",
            "type": "signature",
            "page": 0,
            "x1": 1387,
            "y1": 1459,
            "x2": 1690,
            "y2": 1488
        },
        {
            "name": "PADI_no_6",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1459,
            "x2": 1814,
            "y2": 1488
        },
        {
            "name": "day_6",
            "type": "text",
            "page": 0,
            "x1": 1863,
            "y1": 1459,
            "x2": 1935,
            "y2": 1488
        },
        {
            "name": "month_6",
            "type": "text",
            "page": 0,
            "x1": 1954,
            "y1": 1459,
            "x2": 2026,
            "y2": 1488
        },
        {
            "name": "year_6",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 1459,
            "x2": 2117,
            "y2": 1488
        },
        {
            "name": "Instructor_signature_7",
            "type": "signature",
            "page": 0,
            "x1": 1379,
            "y1": 1555,
            "x2": 1690,
            "y2": 1584
        },
        {
            "name": "PADI_no_7",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1555,
            "x2": 1814,
            "y2": 1584
        },
        {
            "name": "day_7",
            "type": "text",
            "page": 0,
            "x1": 1863,
            "y1": 1555,
            "x2": 1935,
            "y2": 1584
        },
        {
            "name": "month_7",
            "type": "text",
            "page": 0,
            "x1": 1954,
            "y1": 1555,
            "x2": 2026,
            "y2": 1584
        },
        {
            "name": "year_7",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 1555,
            "x2": 2117,
            "y2": 1584
        },
        {
            "name": "Dive_initials_9",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 988,
            "x2": 1912,
            "y2": 1017
        },
        {
            "name": "Dive_initials_10",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 1018,
            "x2": 1912,
            "y2": 1046
        },
        {
            "name": "Check Box20",
            "type": "checkbox",
            "page": 0,
            "x1": 542,
            "y1": 232,
            "x2": 556,
            "y2": 250
        },
        {
            "name": "Check Box21",
            "type": "checkbox",
            "page": 0,
            "x1": 594,
            "y1": 232,
            "x2": 608,
            "y2": 250
        },
        {
            "name": "Check Box22",
            "type": "checkbox",
            "page": 0,
            "x1": 1942,
            "y1": 135,
            "x2": 1957,
            "y2": 151
        },
        {
            "name": "Check Box23",
            "type": "checkbox",
            "page": 0,
            "x1": 1850,
            "y1": 135,
            "x2": 1864,
            "y2": 151
        },
        {
            "name": "Check Box24",
            "type": "checkbox",
            "page": 0,
            "x1": 1742,
            "y1": 135,
            "x2": 1756,
            "y2": 151
        },
        {
            "name": "Check Box25",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 221,
            "x2": 1637,
            "y2": 237
        },
        {
            "name": "Check Box26",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 221,
            "x2": 1840,
            "y2": 237
        },
        {
            "name": "Check Box27",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 251,
            "x2": 1637,
            "y2": 267
        },
        {
            "name": "Check Box28",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 251,
            "x2": 1840,
            "y2": 267
        },
        {
            "name": "Check Box29",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 282,
            "x2": 1637,
            "y2": 298
        },
        {
            "name": "Check Box30",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 282,
            "x2": 1840,
            "y2": 298
        },
        {
            "name": "Check Box31",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 312,
            "x2": 1637,
            "y2": 329
        },
        {
            "name": "Check Box32",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 312,
            "x2": 1840,
            "y2": 329
        },
        {
            "name": "Check Box33",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 343,
            "x2": 1637,
            "y2": 359
        },
        {
            "name": "Check Box34",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 343,
            "x2": 1840,
            "y2": 359
        },
        {
            "name": "Check Box35",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 385,
            "x2": 1637,
            "y2": 401
        },
        {
            "name": "Check Box36",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 385,
            "x2": 1840,
            "y2": 401
        },
        {
            "name": "CW 2",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 244,
            "x2": 803,
            "y2": 273
        },
        {
            "name": "undefined_21",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 244,
            "x2": 893,
            "y2": 273
        },
        {
            "name": "undefined_22",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 244,
            "x2": 985,
            "y2": 273
        },
        {
            "name": "CW 3",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 277,
            "x2": 803,
            "y2": 306
        },
        {
            "name": "undefined_23",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 277,
            "x2": 893,
            "y2": 306
        },
        {
            "name": "undefined_24",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 277,
            "x2": 985,
            "y2": 306
        },
        {
            "name": "CW 4",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 310,
            "x2": 803,
            "y2": 339
        },
        {
            "name": "undefined_25",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 310,
            "x2": 893,
            "y2": 339
        },
        {
            "name": "undefined_26",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 310,
            "x2": 985,
            "y2": 339
        },
        {
            "name": "Initials 1",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 210,
            "x2": 1085,
            "y2": 240
        },
        {
            "name": "Initials 2",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 244,
            "x2": 1085,
            "y2": 273
        },
        {
            "name": "Initials 3",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 277,
            "x2": 1085,
            "y2": 306
        },
        {
            "name": "Initials 4",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 310,
            "x2": 1085,
            "y2": 339
        },
        {
            "name": "CW 1",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 210,
            "x2": 803,
            "y2": 240
        },
        {
            "name": "undefined_27",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 210,
            "x2": 893,
            "y2": 240
        },
        {
            "name": "undefined_28",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 210,
            "x2": 985,
            "y2": 240
        },
        {
            "name": "undefined_29",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 210,
            "x2": 1192,
            "y2": 240
        },
        {
            "name": "Section 1",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 211,
            "x2": 1407,
            "y2": 239
        },
        {
            "name": "undefined_30",
            "type": "text",
            "page": 0,
            "x1": 1426,
            "y1": 211,
            "x2": 1498,
            "y2": 239
        },
        {
            "name": "undefined_31",
            "type": "text",
            "page": 0,
            "x1": 1517,
            "y1": 211,
            "x2": 1588,
            "y2": 239
        },
        {
            "name": "undefined_33",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 211,
            "x2": 1983,
            "y2": 239
        },
        {
            "name": "undefined_34",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 211,
            "x2": 2117,
            "y2": 239
        },
        {
            "name": "undefined_35",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 244,
            "x2": 1192,
            "y2": 273
        },
        {
            "name": "Section 2",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 240,
            "x2": 1407,
            "y2": 270
        },
        {
            "name": "undefined_41",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 277,
            "x2": 1192,
            "y2": 306
        },
        {
            "name": "undefined_47",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 310,
            "x2": 1192,
            "y2": 339
        },
        {
            "name": "CW 5",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 343,
            "x2": 803,
            "y2": 373
        },
        {
            "name": "undefined_53",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 343,
            "x2": 893,
            "y2": 373
        },
        {
            "name": "undefined_54",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 343,
            "x2": 985,
            "y2": 373
        },
        {
            "name": "DSD with all CW Dive 1 skills  Open Water Diver CW Dive 1",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 343,
            "x2": 1085,
            "y2": 373
        },
        {
            "name": "undefined_55",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 343,
            "x2": 1192,
            "y2": 373
        },
        {
            "name": "200 metreyard Swim OR 300 metreyard MaskSnorkelFin Swim",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 487,
            "x2": 1085,
            "y2": 516
        },
        {
            "name": "10 Minute Survival Float",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 487,
            "x2": 803,
            "y2": 516
        },
        {
            "name": "undefined_66",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 487,
            "x2": 893,
            "y2": 516
        },
        {
            "name": "undefined_67",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 487,
            "x2": 985,
            "y2": 516
        },
        {
            "name": "undefined_68",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 487,
            "x2": 1192,
            "y2": 516
        },
        {
            "name": "undefined_72",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 559,
            "x2": 985,
            "y2": 589
        },
        {
            "name": "undefined_73",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 559,
            "x2": 1085,
            "y2": 589
        },
        {
            "name": "undefined_74",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 559,
            "x2": 1192,
            "y2": 589
        },
        {
            "name": "undefined_75",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 559,
            "x2": 803,
            "y2": 589
        },
        {
            "name": "undefined_76",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 559,
            "x2": 893,
            "y2": 589
        },
        {
            "name": "undefined_77",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 676,
            "x2": 1085,
            "y2": 705
        },
        {
            "name": "undefined_78",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 676,
            "x2": 1192,
            "y2": 705
        },
        {
            "name": "Equipment Preparation and Care",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 676,
            "x2": 803,
            "y2": 705
        },
        {
            "name": "undefined_91",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 676,
            "x2": 893,
            "y2": 705
        },
        {
            "name": "undefined_92",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 676,
            "x2": 985,
            "y2": 705
        },
        {
            "name": "undefined_93",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 756,
            "x2": 1085,
            "y2": 785
        },
        {
            "name": "undefined_94",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 756,
            "x2": 1192,
            "y2": 785
        },
        {
            "name": "Disconnect Low Pressure Inflator Hose",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 756,
            "x2": 803,
            "y2": 785
        },
        {
            "name": "undefined_95",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 756,
            "x2": 893,
            "y2": 785
        },
        {
            "name": "undefined_96",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 756,
            "x2": 985,
            "y2": 785
        },
        {
            "name": "Loose Cylinder Band",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 835,
            "x2": 803,
            "y2": 864
        },
        {
            "name": "undefined_97",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 835,
            "x2": 985,
            "y2": 864
        },
        {
            "name": "undefined_98",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 835,
            "x2": 1085,
            "y2": 864
        },
        {
            "name": "undefined_99",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 835,
            "x2": 1192,
            "y2": 864
        },
        {
            "name": "undefined_100",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 835,
            "x2": 893,
            "y2": 864
        },
        {
            "name": "undefined_101",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 915,
            "x2": 1192,
            "y2": 944
        },
        {
            "name": "Weight System Removal and Replacement surface",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 915,
            "x2": 803,
            "y2": 944
        },
        {
            "name": "undefined_102",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 915,
            "x2": 893,
            "y2": 944
        },
        {
            "name": "undefined_103",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 915,
            "x2": 985,
            "y2": 944
        },
        {
            "name": "undefined_104",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 915,
            "x2": 1085,
            "y2": 944
        },
        {
            "name": "undefined_105",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 994,
            "x2": 1085,
            "y2": 1024
        },
        {
            "name": "undefined_106",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 994,
            "x2": 1192,
            "y2": 1024
        },
        {
            "name": "Emergency Weight Drop or in OW",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 994,
            "x2": 803,
            "y2": 1024
        },
        {
            "name": "undefined_107",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 994,
            "x2": 893,
            "y2": 1024
        },
        {
            "name": "undefined_108",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 994,
            "x2": 985,
            "y2": 1024
        },
        {
            "name": "undefined_118",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1083,
            "x2": 985,
            "y2": 1112
        },
        {
            "name": "undefined_119",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 1083,
            "x2": 1085,
            "y2": 1112
        },
        {
            "name": "undefined_120",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1083,
            "x2": 1192,
            "y2": 1112
        },
        {
            "name": "Skin Diving Skills",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1083,
            "x2": 803,
            "y2": 1112
        },
        {
            "name": "undefined_122",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1083,
            "x2": 893,
            "y2": 1112
        },
        {
            "name": "undefined_123",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1172,
            "x2": 985,
            "y2": 1202
        },
        {
            "name": "undefined_124",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 1172,
            "x2": 1085,
            "y2": 1202
        },
        {
            "name": "undefined_125",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1172,
            "x2": 1192,
            "y2": 1202
        },
        {
            "name": "Note If all Confined Water Dives Confined Water Dive Flexible Skills and Wa",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1172,
            "x2": 803,
            "y2": 1202
        },
        {
            "name": "undefined_129",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1172,
            "x2": 893,
            "y2": 1202
        },
        {
            "name": "undefined_36",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 240,
            "x2": 1498,
            "y2": 270
        },
        {
            "name": "undefined_37",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 240,
            "x2": 1588,
            "y2": 270
        },
        {
            "name": "undefined_39",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 240,
            "x2": 1983,
            "y2": 270
        },
        {
            "name": "undefined_40",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 240,
            "x2": 2117,
            "y2": 270
        },
        {
            "name": "Section 3",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 271,
            "x2": 1407,
            "y2": 300
        },
        {
            "name": "undefined_42",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 271,
            "x2": 1498,
            "y2": 300
        },
        {
            "name": "undefined_43",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 271,
            "x2": 1588,
            "y2": 300
        },
        {
            "name": "undefined_45",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 271,
            "x2": 1983,
            "y2": 300
        },
        {
            "name": "undefined_46",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 271,
            "x2": 2117,
            "y2": 300
        },
        {
            "name": "Section 4",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 302,
            "x2": 1407,
            "y2": 331
        },
        {
            "name": "undefined_48",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 302,
            "x2": 1498,
            "y2": 331
        },
        {
            "name": "undefined_49",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 302,
            "x2": 1588,
            "y2": 331
        },
        {
            "name": "undefined_51",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 302,
            "x2": 1983,
            "y2": 331
        },
        {
            "name": "undefined_52",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 302,
            "x2": 2117,
            "y2": 331
        },
        {
            "name": "Section 5",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 332,
            "x2": 1407,
            "y2": 361
        },
        {
            "name": "undefined_56",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 332,
            "x2": 1498,
            "y2": 361
        },
        {
            "name": "undefined_57",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 332,
            "x2": 1588,
            "y2": 361
        },
        {
            "name": "undefined_59",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 332,
            "x2": 1983,
            "y2": 361
        },
        {
            "name": "undefined_60",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 332,
            "x2": 2117,
            "y2": 361
        },
        {
            "name": "Quick Review",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 375,
            "x2": 1407,
            "y2": 404
        },
        {
            "name": "undefined_61",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 375,
            "x2": 1498,
            "y2": 404
        },
        {
            "name": "undefined_62",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 375,
            "x2": 1588,
            "y2": 404
        },
        {
            "name": "undefined_64",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 375,
            "x2": 1983,
            "y2": 404
        },
        {
            "name": "undefined_65",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 375,
            "x2": 2117,
            "y2": 404
        },
        {
            "name": "Dive 2",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 641,
            "x2": 1328,
            "y2": 671
        },
        {
            "name": "undefined_79",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 641,
            "x2": 1402,
            "y2": 671
        },
        {
            "name": "undefined_80",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 641,
            "x2": 1475,
            "y2": 671
        },
        {
            "name": "Initials 1_2",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 612,
            "x2": 1547,
            "y2": 637
        },
        {
            "name": "Initials 2_2",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 641,
            "x2": 1547,
            "y2": 671
        },
        {
            "name": "undefined_81",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 641,
            "x2": 1654,
            "y2": 671
        },
        {
            "name": "Dive 4",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 641,
            "x2": 1781,
            "y2": 671
        },
        {
            "name": "undefined_82",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 641,
            "x2": 1854,
            "y2": 671
        },
        {
            "name": "undefined_83",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 641,
            "x2": 1928,
            "y2": 671
        },
        {
            "name": "Initials 1_3",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 612,
            "x2": 2010,
            "y2": 637
        },
        {
            "name": "Initials 2_3",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 641,
            "x2": 2010,
            "y2": 671
        },
        {
            "name": "Dive 1",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 612,
            "x2": 1328,
            "y2": 637
        },
        {
            "name": "undefined_84",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 612,
            "x2": 1401,
            "y2": 637
        },
        {
            "name": "undefined_85",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 612,
            "x2": 1475,
            "y2": 637
        },
        {
            "name": "undefined_86",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 612,
            "x2": 1654,
            "y2": 637
        },
        {
            "name": "Dive 3",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 612,
            "x2": 1781,
            "y2": 637
        },
        {
            "name": "undefined_87",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 612,
            "x2": 1854,
            "y2": 637
        },
        {
            "name": "undefined_88",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 612,
            "x2": 1928,
            "y2": 637
        },
        {
            "name": "undefined_89",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 612,
            "x2": 2117,
            "y2": 637
        },
        {
            "name": "undefined_90",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 641,
            "x2": 2117,
            "y2": 671
        },
        {
            "name": "undefined_126",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1128,
            "x2": 1814,
            "y2": 1158
        }
    ]
}


def load_fields():
    """Return a fresh copy of the embedded master field mask.

    The external 10056_OW_Records_mask.json file is intentionally NOT read,
    created, checked, or required. The embedded Python definition is the
    single source of truth for the master mask.
    """
    return copy.deepcopy(HARDCODED_MASK.get("fields", []))


def save_fields(fields):
    """Compatibility hook for older field-edit code.

    Field edits remain in memory for the current session. The master mask is
    embedded in the application and is therefore never overwritten by the GUI.
    """
    return True

def load_state():
    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return {}

        # Current location-aware state format stores each value as
        # {"value": ..., "page": ..., "x1": ..., ...}.
        # Convert that back to the flat runtime state used by the GUI.
        normalized = {}
        wrapped = False

        for name, value in data.items():
            if isinstance(value, dict) and "value" in value:
                normalized[name] = value.get("value")
                wrapped = True
            else:
                normalized[name] = value

        return normalized if wrapped else data

    except Exception as e:
        print("STATE LOAD ERROR:", e)
        return {}

def save_state_with_locations():
    try:
        return _atomic_json_write(STATE_FILE, state)
    except Exception as e:
        messagebox.showerror("State Error", f"Failed to save application state:\n{e}")
        return False

fields = []
state = load_state()
comments_db = load_comments_db()

def show_program_fields():

    fields_used = """
PROGRAM FIELD LOGIC (OW 10056 document)

Student:(Left block)
-----------
Student Name
student_signature (Right block at the end)
Stu_day
Stu_month
Stu_year

Init Instructor Blocks: (Left  block)
(Instructors involved)
-----------------------
init_padi_instructor_1
init_padi_instructor_2

Init_Instructor_Signature_1 (All PADI Instructors #1 who initial this document ... )
Init_Instructor_Signature_2 (All PADI Instructors #1 who initial this document ... )

Init_PADI_no_1
Init_PADI_no_2

Init_Dive_Resort_No_1
Init_Dive_Resort_No_2

Init_day_1
Init_month_1
Init_year_1

Init_day_2
Init_month_2
Init_year_2

Init_Phone_1
Init_Phone_2

Init_Email_1
Init_Email_2

Instructor Signoffs:
--------------------
Instructor_signature_3  (All Confined have been completed)
Instructor_signature_4  (All Knowledge Development sessions listed above have been completed, Quizzes/Exams passed)
Instructor_signature_5  (All Open Water Dive Flexible Skills listed above have been completed.)
Instructor_signature_6  (All requirements for certification as a PADI Scuba Diver have been met)
Instructor_signature_7  (All requirements for certification as a PADI Open Water Diver have been met.)

PADI_no_3 to PADI_no_7
day_3 to day_7
month_3 to month_7
year_3 to year_7

CW Auto-Populate Pattern:
-------------------------
CW1_day ... CW24_day  (Starts at CW 1*)
CW1_month ... CW24_month
CW1_year ... CW24_year
CW1_initials ... CW24_initials
CW1_padi ... CW24_padi (ends at the year for the final signoff)

Dive Logic:
-----------
Dive_1 ... Dive_10
Dive_initials_1 ... Dive_initials_10
Dive_padi_1 ... Dive_padi_10

Special Logic:
--------------
CW12 auto-fills Dive_4
"""

    win = tk.Toplevel(root)
    win.title("Program Field Logic")
    win.geometry("700x700")

    txt = tk.Text(win, wrap="word")
    txt.pack(fill="both", expand=True)

    txt.insert("1.0", fields_used)
    txt.config(state="disabled")

# ---------------- Signature Drawing Window ----------------

def draw_student_signature_window(field_name):

    win = tk.Toplevel(root)
    win.title("Student Signature")
    win.geometry("620x320")

    width, height = 600, 120

    canvas_sig = tk.Canvas(
        win,
        bg="#E6E6E6",
        width=width,
        height=height
    )
    canvas_sig.pack(pady=10)

    img = Image.new("RGB", (width, height), "white")
    draw_obj = ImageDraw.Draw(img)

    last = {"x": None, "y": None}

    def start_draw(event):
        last["x"], last["y"] = event.x, event.y

    def draw_line(event):
        if last["x"] is not None:
            canvas_sig.create_line(
                last["x"], last["y"], event.x, event.y,
                fill="black", width=3
            )
            draw_obj.line(
                (last["x"], last["y"], event.x, event.y),
                fill="black", width=3
            )
        last["x"], last["y"] = event.x, event.y

    canvas_sig.bind("<Button-1>", start_draw)
    canvas_sig.bind("<B1-Motion>", draw_line)

    def clear_canvas():
        canvas_sig.delete("all")
        draw_obj.rectangle((0, 0, width, height), fill="white")

    def save_signature():

        filename = SIGNATURE_DIR / f"{field_name}_student.png"
        img.save(filename)

        state[field_name] = str(filename)

        d = date_picker.get_date()

        state["Stu_day"] = str(d.day)
        state["Stu_month"] = [
            "Jan","Feb","Mar","Apr","May","Jun",
            "Jul","Aug","Sep","Oct","Nov","Dec"
        ][d.month - 1]
        state["Stu_year"] = str(d.year)

        save_state_with_locations()

        redraw_all_text_fields()
        redraw_all_signatures()

        win.destroy()

    def delete_signature():
        if field_name in state:
            del state[field_name]
            save_state_with_locations()
            redraw_all_signatures()
        win.destroy()

    # Buttons
    tk.Button(
        win,
        text="Clear",
        command=clear_canvas
    ).pack(side="left", padx=20)

    tk.Button(
        win,
        text="Save Signature",
        command=save_signature
    ).pack(side="right", padx=20)

    tk.Button(
        win,
        text="Delete Signature",
        command=delete_signature
    ).pack(side="left", padx=20)

def draw_signature_window(name, padi_number, signature_var):

    win = tk.Toplevel(root)
    win.title(f"Draw Signature for {name}")
    win.geometry("620x320")

    width, height = 600, 120

    canvas_sig = tk.Canvas(
        win,
        bg="#E6E6E6",
        width=width,
        height=height
    )
    canvas_sig.pack(pady=10)

    img = Image.new("RGB", (width, height), "white")
    draw_obj = ImageDraw.Draw(img)

    last = {"x": None, "y": None}

    def start_draw(event):
        last["x"], last["y"] = event.x, event.y

    def draw_line(event):

        if last["x"] is not None:

            canvas_sig.create_line(
                last["x"],
                last["y"],
                event.x,
                event.y,
                fill="black",
                width=3
            )

            draw_obj.line(
                (last["x"], last["y"], event.x, event.y),
                fill="black",
                width=3
            )

        last["x"], last["y"] = event.x, event.y

    canvas_sig.bind("<Button-1>", start_draw)
    canvas_sig.bind("<B1-Motion>", draw_line)

    def clear_canvas():
        canvas_sig.delete("all")
        draw_obj.rectangle(
            (0, 0, width, height),
            fill="white"
        )

    def save_signature():

        safe_padi = re.sub(
            r"[^A-Za-z0-9_-]",
            "_",
            str(padi_number)
        )

        filename = SIGNATURE_DIR / f"{safe_padi}.png"

        img.save(filename)

        signature_var.set(str(filename))

        messagebox.showinfo(
            "Saved",
            f"Signature saved as:\n{filename}"
        )

        win.destroy()

        try:
            instructor_window.lift()
            instructor_window.focus_force()
        except:
            pass

    tk.Button(
        win,
        text="Clear",
        command=clear_canvas
    ).pack(side="left", padx=20, pady=5)

    tk.Button(
        win,
        text="Save Signature",
        command=save_signature
    ).pack(side="right", padx=20, pady=5)

# ---------------- PDF Viewer ----------------

pdf_path = None
pages = []
current_page = 0

def render_page():

    global zoom_level

    if not pages:
        print("RENDER PAGE ABORTED: pages list is empty")
        return

    if current_page < 0 or current_page >= len(pages):
        print("RENDER PAGE ABORTED: invalid page index", current_page)
        return

    try:
        print("RENDER_PAGE START: page", current_page + 1, "of", len(pages))

        # Clear canvas drawing objects only. Do not destroy Tk child widgets and
        # do not call root.update() from inside a drawing callback; both can
        # cause event-loop re-entry problems on macOS.
        canvas_pdf.delete("all")
        canvas_pdf.image = None

        if hasattr(canvas_pdf, "signature_images"):
            canvas_pdf.signature_images.clear()

        page = pages[current_page]
        w, h = page.size
        new_w = max(1, int(w * zoom_level))
        new_h = max(1, int(h * zoom_level))

        print("SOURCE PAGE SIZE =", (w, h), "DISPLAY SIZE =", (new_w, new_h))

        if new_w == w and new_h == h:
            display_image = page
        else:
            display_image = page.resize((new_w, new_h), Image.LANCZOS)

        print("CREATING TK PDF IMAGE")
        tk_img = ImageTk.PhotoImage(display_image, master=root)
        canvas_pdf.image = tk_img  # keep a strong reference

        image_id = canvas_pdf.create_image(
            0,
            0,
            anchor="nw",
            image=tk_img,
            tags=("pdf_backdrop",)
        )
        canvas_pdf.tag_lower("pdf_backdrop")
        canvas_pdf.config(scrollregion=(0, 0, new_w, new_h))

        print("PDF BACKDROP IMAGE ID =", image_id)

        print("DRAWING FIELD BOXES")
        draw_all_field_boxes()
        print("DRAWING TEXT FIELDS")
        redraw_all_text_fields()
        print("DRAWING SIGNATURES")
        redraw_all_signatures()
        print("DRAWING CHECKBOXES")
        redraw_all_checkboxes()

        canvas_pdf.tag_raise("text_drawn")
        canvas_pdf.tag_raise("signature_drawn")
        canvas_pdf.tag_raise("checkbox_drawn")
        canvas_pdf.tag_raise("field_box")

        print("RENDER_PAGE COMPLETE")

    except Exception as e:
        print("RENDER_PAGE ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Display Error",
            f"The PDF page could not be displayed:\n\n{e}"
        )


# ---------------- Advanced Field Detection ----------------

def detect_acroform_fields(pdf_path, pages):
    reader = PdfReader(pdf_path)
    root = reader.trailer.get("/Root", {})
    if "/AcroForm" not in root:
        return []

    form = root["/AcroForm"]
    fields_raw = form.get("/Fields", [])

    detected = []

    for field_ref in fields_raw:
        field = field_ref.get_object()

        ftype = field.get("/FT")
        rect = field.get("/Rect")
        page_ref = field.get("/P")

        if not rect or not page_ref:
            continue

        try:
            page_obj = page_ref.get_object()
        except:
            page_obj = page_ref

        page_index = None
        for i, p in enumerate(reader.pages):
            if p.indirect_reference.idnum == page_obj.indirect_reference.idnum:
                page_index = i
                break

        if page_index is None:
            print("WARNING: Could not resolve page for field:", field)
            continue

        x1_pdf, y1_pdf, x2_pdf, y2_pdf = rect

        pdf_page = reader.pages[page_index]
        pdf_w = float(pdf_page.mediabox.width)
        pdf_h = float(pdf_page.mediabox.height)

        img_w, img_h = pages[page_index].size

        scale_x = img_w / pdf_w
        scale_y = img_h / pdf_h

        x1_img = int(x1_pdf * scale_x)
        x2_img = int(x2_pdf * scale_x)
        y1_img = int((pdf_h - y2_pdf) * scale_y)
        y2_img = int((pdf_h - y1_pdf) * scale_y)

        if ftype == "/Sig":
            my_type = "signature"
        elif ftype == "/Tx":
            my_type = "text"
        elif ftype == "/Btn":
            my_type = "checkbox"
        else:
            my_type = "unknown"

        detected.append({
            "name": field.get("/T", f"{my_type}_field_{len(detected)+1}"),
            "type": my_type,
            "page": page_index,
            "x1": x1_img,
            "y1": y1_img,
            "x2": x2_img,
            "y2": y2_img
        })

    return detected
def build_pdf_field_mapping():
    """
    Map application/mask fields to the real AcroForm widgets.

    The mask coordinates are 200-DPI image coordinates, while the PDF stores
    widget rectangles in PDF points.  The PADI PDF also uses many generic
    field names (for example "CW 2", "PADI No", "undefined_9") while the
    application uses semantic names such as "CW2_day".

    Therefore mapping is based primarily on page + rectangle position.
    Exact names are preferred only when they occur at the same location.
    Each real PDF widget is claimed once so duplicate OCR/mask entries do
    not overwrite one another.
    """
    global pdf_field_mapping, pdf_field_rects

    pdf_field_mapping = {}
    pdf_field_rects = {}

    if not pdf_path:
        return

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print("Error reading PDF fields:", e)
        return

    render_sizes = {
        page_index: page_image.size
        for page_index, page_image in enumerate(pages)
    }

    actual_widgets = []

    for page_index, page in enumerate(reader.pages):
        pdf_w = float(page.mediabox.width)
        pdf_h = float(page.mediabox.height)

        if page_index in render_sizes:
            img_w, img_h = render_sizes[page_index]
            scale_x = img_w / pdf_w
            scale_y = img_h / pdf_h
        else:
            scale_x = 200.0 / 72.0
            scale_y = 200.0 / 72.0

        annots_ref = page.get("/Annots")
        if not annots_ref:
            continue

        try:
            annots = annots_ref.get_object()
        except Exception:
            annots = annots_ref

        for annot_ref in annots:
            try:
                annot = annot_ref.get_object()
            except Exception:
                annot = annot_ref

            if annot.get("/Subtype") != "/Widget":
                continue

            name_obj = annot.get("/T")
            rect = annot.get("/Rect")
            ftype = annot.get("/FT")

            if not name_obj or not rect:
                continue

            if not ftype and annot.get("/Parent"):
                try:
                    parent = annot["/Parent"].get_object()
                    ftype = parent.get("/FT")
                except Exception:
                    pass

            name = str(name_obj)

            x1_pdf, y1_pdf, x2_pdf, y2_pdf = [float(v) for v in rect]

            x1_img = x1_pdf * scale_x
            x2_img = x2_pdf * scale_x
            y1_img = (pdf_h - y2_pdf) * scale_y
            y2_img = (pdf_h - y1_pdf) * scale_y

            if ftype == "/Sig":
                widget_type = "signature"
            elif ftype == "/Tx":
                widget_type = "text"
            elif ftype == "/Btn":
                widget_type = "checkbox"
            else:
                widget_type = "unknown"

            actual_widgets.append({
                "name": name,
                "type": widget_type,
                "page": page_index,
                "x1": x1_img,
                "y1": y1_img,
                "x2": x2_img,
                "y2": y2_img,
            })

    claimed = set()

    def box_score(mask_field, widget):
        return (
            abs(float(mask_field["x1"]) - widget["x1"]) +
            abs(float(mask_field["y1"]) - widget["y1"]) +
            abs(float(mask_field["x2"]) - widget["x2"]) +
            abs(float(mask_field["y2"]) - widget["y2"])
        )

    for mask_field in fields:
        mask_name = mask_field["name"]
        page_index = mask_field["page"]

        candidates = [
            w for w in actual_widgets
            if w["page"] == page_index and w["name"] not in claimed
        ]

        if not candidates:
            pdf_field_mapping[mask_name] = None
            continue

        best = min(candidates, key=lambda w: box_score(mask_field, w))
        best_score = box_score(mask_field, best)

        if best_score > 10:
            pdf_field_mapping[mask_name] = None
            continue

        exact_candidates = [
            w for w in candidates
            if w["name"] == mask_name and box_score(mask_field, w) <= 10
        ]
        if exact_candidates:
            best = min(exact_candidates, key=lambda w: box_score(mask_field, w))

        claimed.add(best["name"])
        pdf_field_mapping[mask_name] = best["name"]

        pdf_field_rects[best["name"]] = (
            best["page"],
            best["x1"],
            best["y1"],
            best["x2"],
            best["y2"],
        )

    print("PDF FIELD MAPPING (coordinate based):")
    mapped_count = 0
    for app_name, pdf_name in pdf_field_mapping.items():
        if pdf_name:
            mapped_count += 1
            print(f"{app_name} -> {pdf_name}")

    print(
        f"Mapped {mapped_count} of {len(fields)} mask fields "
        f"to {len(claimed)} real PDF widgets."
    )

def heuristic_signature_boxes(page_image, page_index):
    w, h = page_image.size
    gray = ImageOps.grayscale(page_image)
    pixels = gray.load()

    candidates = []
    min_length = int(w * 0.2)
    threshold = 60

    for y in range(int(h * 0.2), int(h * 0.9)):
        dark_run = 0
        start_x = None
        for x in range(int(w * 0.05), int(w * 0.95)):
            if pixels[x, y] < threshold:
                if dark_run == 0:
                    start_x = x
                dark_run += 1
            else:
                if dark_run >= min_length:
                    candidates.append({
                        "name": f"signature_heuristic_{len(candidates)+1}",
                        "type": "signature",
                        "page": page_index,
                        "x1": start_x,
                        "y1": y - 10,
                        "x2": x,
                        "y2": y + 10
                    })
                dark_run = 0
                start_x = None

    return candidates

def save_state_with_locations():
    save_data = {}

    for f in fields:
        name = f["name"]

        if name not in state:
            continue

        save_data[name] = {
            "value": state[name],
            "page": f["page"],
            "x1": f["x1"],
            "y1": f["y1"],
            "x2": f["x2"],
            "y2": f["y2"],
            "type": f["type"]
        }

    try:
        return _atomic_json_write(STATE_FILE, save_data)
    except Exception as e:
        messagebox.showerror(
            "State Error",
            f"Failed to save application state:\n{e}"
        )
        return False

def clear_signature(field_name):
    if field_name in state:
        del state[field_name]
    save_state_with_locations()
    redraw_all_signatures()


def load_state_by_location():

    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            old_data = json.load(f)

    except Exception:
        return {}

    new_state = {}

    for current_field in fields:

        best_match = None
        best_score = 999999

        for old_name, old_info in old_data.items():

            if not isinstance(old_info, dict):
                continue

            #
            # FIRST TRY EXACT FIELD NAME MATCH
            #
            if old_name == current_field["name"]:

                print(
                    "NAME MATCH:",
                    current_field["name"],
                    "<--",
                    old_info.get("value")
                )

                new_state[current_field["name"]] = (
                    old_info.get("value")
                )

                best_match = None
                break

            #
            # OTHERWISE FALL BACK TO LOCATION MATCHING
            #
            if current_field["page"] != old_info.get("page"):
                continue

            score = (
                abs(current_field["x1"] - old_info["x1"]) +
                abs(current_field["y1"] - old_info["y1"]) +
                abs(current_field["x2"] - old_info["x2"]) +
                abs(current_field["y2"] - old_info["y2"])
            )

            if score < best_score:
                best_score = score
                best_match = old_info

        #
        # ONLY USE LOCATION MATCH IF
        # NAME MATCH DID NOT ALREADY HAPPEN
        #
        if (
            current_field["name"] not in new_state
            and best_match
            and best_score < 10
        ):

            print(
                "LOCATION MATCH:",
                current_field["name"],
                "<--",
                best_match.get("value"),
                "score=",
                best_score
            )

            new_state[current_field["name"]] = (
                best_match.get("value")
            )

    print("new_state =", new_state)
    print("LOADED STATE COUNT =", len(new_state))

    return new_state


# ---------------- PDF-EMBEDDED SIGNATURE RECOVERY ----------------
# Signatures in a reopened PDF must come from that PDF, never from the
# currently selected instructor or the global state_padi.json file.
PDF_SIGNATURE_CACHE_DIR = DATA_DIR / "pdf_signature_cache"
PDF_SIGNATURE_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _signature_field_lookup():
    """Return a case-insensitive lookup of application signature field names."""
    return {
        str(f.get("name", "")).strip().lower(): f.get("name")
        for f in fields
        if f.get("type") == "signature" and f.get("name")
    }


def _pdf_signature_cache_path(pdf_file, field_name, suffix="embedded"):
    """Create a deterministic local cache path for a signature recovered from a PDF."""
    try:
        pdf_id = _sha256_file(pdf_file)[:16]
    except Exception:
        pdf_id = hashlib.sha256(str(pdf_file).encode("utf-8")).hexdigest()[:16]

    safe_field = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(field_name)).strip("_") or "signature"
    folder = PDF_SIGNATURE_CACHE_DIR / pdf_id
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{safe_field}_{suffix}.png"


def _xobject_image_to_pil(image_obj):
    """Convert a PDF /Image XObject used by our signature stamps into a PIL image."""
    try:
        width = int(image_obj.get("/Width", 0))
        height = int(image_obj.get("/Height", 0))
        bits = int(image_obj.get("/BitsPerComponent", 8) or 8)
        color_space = image_obj.get("/ColorSpace")
        if hasattr(color_space, "get_object"):
            color_space = color_space.get_object()

        if width <= 0 or height <= 0 or bits != 8:
            return None

        # ReportLab signature PNGs normally become DeviceRGB image XObjects.
        # Handle the common grayscale/CMYK variants as well.
        cs_text = str(color_space)
        if "/DeviceRGB" in cs_text:
            mode = "RGB"
        elif "/DeviceGray" in cs_text:
            mode = "L"
        elif "/DeviceCMYK" in cs_text:
            mode = "CMYK"
        else:
            return None

        raw = image_obj.get_data()
        image = Image.frombytes(mode, (width, height), raw)

        # Restore transparency if the PDF image has a soft mask.
        smask = image_obj.get("/SMask")
        if smask is not None:
            smask = smask.get_object() if hasattr(smask, "get_object") else smask
            try:
                alpha_raw = smask.get_data()
                alpha = Image.frombytes("L", (width, height), alpha_raw)
                if image.mode != "RGBA":
                    image = image.convert("RGBA")
                image.putalpha(alpha)
            except Exception as e:
                print("SIGNATURE ALPHA MASK WARNING:", e)

        return image
    except Exception as e:
        print("SIGNATURE XOBJECT DECODE WARNING:", e)
        return None


def _find_first_image_xobject(resources):
    """Find the first image XObject in an appearance resource dictionary."""
    if resources is None:
        return None
    try:
        resources = resources.get_object() if hasattr(resources, "get_object") else resources
        xobjects = resources.get("/XObject")
        if not xobjects:
            return None
        xobjects = xobjects.get_object() if hasattr(xobjects, "get_object") else xobjects

        for _, ref in xobjects.items():
            obj = ref.get_object() if hasattr(ref, "get_object") else ref
            subtype = str(obj.get("/Subtype", ""))
            if subtype == "/Image":
                return obj
            if subtype == "/Form":
                nested = _find_first_image_xobject(obj.get("/Resources"))
                if nested is not None:
                    return nested
    except Exception as e:
        print("SIGNATURE XOBJECT SEARCH WARNING:", e)
    return None


def load_signature_stamps_from_pdf(pdf_file):
    """Recover V21 removable signature /Stamp annotations from an existing PDF.

    Returns {application_field_name: local_png_path}.  The /Contents value written
    by _add_signature_stamp_annotation() identifies which application field owns
    each stamp, so no instructor-dropdown state is involved.
    """
    recovered = {}
    field_lookup = _signature_field_lookup()

    try:
        reader = PdfReader(str(pdf_file))
        for page_index, page in enumerate(reader.pages):
            annotations = page.get("/Annots") or []
            for annot_ref in annotations:
                try:
                    annot = annot_ref.get_object() if hasattr(annot_ref, "get_object") else annot_ref
                    if str(annot.get("/Subtype", "")) != "/Stamp":
                        continue

                    contents = str(annot.get("/Contents", "")).strip()
                    app_name = field_lookup.get(contents.lower())
                    if not app_name:
                        continue

                    ap = annot.get("/AP")
                    if not ap:
                        continue
                    ap = ap.get_object() if hasattr(ap, "get_object") else ap
                    normal = ap.get("/N")
                    if not normal:
                        continue
                    normal = normal.get_object() if hasattr(normal, "get_object") else normal

                    image_obj = _find_first_image_xobject(normal.get("/Resources"))
                    if image_obj is None:
                        continue

                    image = _xobject_image_to_pil(image_obj)
                    if image is None:
                        continue

                    target = _pdf_signature_cache_path(pdf_file, app_name, f"stamp_p{page_index + 1}")
                    image.save(target, format="PNG")
                    image.close()
                    recovered[app_name] = str(target)
                    print("RECOVERED PDF SIGNATURE STAMP:", app_name, "->", target)
                except Exception as e:
                    print("SIGNATURE STAMP READ WARNING:", e)
    except Exception as e:
        print("SIGNATURE STAMP LOAD ERROR:", e)

    return recovered



def _render_pdf_pages_quiet(pdf_file, dpi=200):
    """Render a PDF specifically for signature recovery without changing GUI state."""
    doc = pdfium.PdfDocument(str(pdf_file))
    images = []
    scale = float(dpi) / 72.0
    try:
        for page_index in range(len(doc)):
            page = None
            bitmap = None
            try:
                page = doc[page_index]
                bitmap = page.render(scale=scale)
                image = bitmap.to_pil().convert("RGB")
                image.load()
                images.append(image.copy())
                image.close()
            finally:
                if bitmap is not None:
                    try:
                        bitmap.close()
                    except Exception:
                        pass
                if page is not None:
                    try:
                        page.close()
                    except Exception:
                        pass
    finally:
        try:
            doc.close()
        except Exception:
            pass
    return images


def _extract_flattened_signature_crop(actual_crop, base_crop=None):
    """Return a transparent signature image if handwriting is detected.

    Some PDF editors (notably macOS Preview/Quartz workflows) flatten a visible
    signature into the page artwork while leaving the AcroForm /Sig widget empty.
    This routine recovers that visible ink.  If a pristine base page is available,
    pixel differencing is used.  Otherwise long horizontal/vertical form lines are
    suppressed before the remaining ink is evaluated.
    """
    import numpy as _np

    actual = _np.asarray(actual_crop.convert("L"), dtype=_np.int16)
    h, w = actual.shape
    if h < 3 or w < 3:
        return None

    ink = None

    if base_crop is not None and base_crop.size == actual_crop.size:
        base = _np.asarray(base_crop.convert("L"), dtype=_np.int16)
        # Keep pixels that became materially darker than the pristine form.
        delta = base - actual
        ink = (delta > 22) & (actual < 225)

        # If the two pages are effectively identical, the chosen base was not
        # actually pristine. Fall back to line-suppression mode below.
        if int(ink.sum()) < max(10, int(w * h * 0.0007)):
            ink = None

    if ink is None:
        # Dark pixels are potential handwriting or printed form rules.
        ink = actual < 190

        # Remove long horizontal rules/underlines and their anti-aliased edges.
        row_counts = ink.sum(axis=1)
        line_rows = _np.where(row_counts > max(8, int(w * 0.38)))[0]
        for y in line_rows:
            y0 = max(0, int(y) - 2)
            y1 = min(h, int(y) + 3)
            ink[y0:y1, :] = False

        # Remove any long vertical widget/form borders.
        col_counts = ink.sum(axis=0)
        line_cols = _np.where(col_counts > max(8, int(h * 0.70)))[0]
        for x in line_cols:
            x0 = max(0, int(x) - 1)
            x1 = min(w, int(x) + 2)
            ink[:, x0:x1] = False

    # Ignore a narrow rim where field borders/anti-aliasing tend to occur.
    rim = max(1, min(3, h // 8))
    if h > rim * 2 and w > rim * 2:
        ink[:rim, :] = False
        ink[-rim:, :] = False
        ink[:, :rim] = False
        ink[:, -rim:] = False

    ink_count = int(ink.sum())
    # A real handwritten signature has substantially more remaining ink than
    # anti-aliasing noise after form-line suppression.
    threshold = max(24, int(w * h * 0.0030))
    if ink_count < threshold:
        return None

    ys, xs = _np.where(ink)
    if len(xs) == 0:
        return None

    # Reject tiny isolated blobs that cannot plausibly be a signature.
    span_w = int(xs.max() - xs.min() + 1)
    span_h = int(ys.max() - ys.min() + 1)
    if span_w < max(8, int(w * 0.08)) or span_h < 3:
        return None

    # Build a transparent black-ink PNG. Slightly expand the detected mask by one
    # pixel so anti-aliased handwriting remains visually continuous in the GUI.
    expanded = ink.copy()
    expanded[:-1, :] |= ink[1:, :]
    expanded[1:, :] |= ink[:-1, :]
    expanded[:, :-1] |= ink[:, 1:]
    expanded[:, 1:] |= ink[:, :-1]

    rgba = _np.zeros((h, w, 4), dtype=_np.uint8)
    rgba[:, :, 0:3] = 0
    rgba[:, :, 3] = _np.where(expanded, 255, 0).astype(_np.uint8)
    return Image.fromarray(rgba, mode="RGBA")


def load_flattened_signatures_from_pdf(pdf_file):
    """Recover visible signatures that were flattened into PDF page artwork.

    This is the final fallback after embedded PADI Manager metadata and removable
    /Stamp annotations. It uses the already-built application-to-AcroForm mapping
    so a recovered image is assigned to the correct signature field, never to the
    currently selected instructor dropdown entry.
    """
    recovered = {}
    actual_pages = []
    base_pages = []

    try:
        actual_pages = _render_pdf_pages_quiet(pdf_file, dpi=200)

        base_path = globals().get("current_base_pdf_path")
        if base_path:
            try:
                base_path = Path(base_path)
                if base_path.exists() and base_path.resolve() != Path(pdf_file).resolve():
                    base_pages = _render_pdf_pages_quiet(base_path, dpi=200)
            except Exception as e:
                print("FLATTENED SIGNATURE BASE RENDER WARNING:", e)
                base_pages = []

        for field in fields:
            if field.get("type") != "signature":
                continue

            app_name = field.get("name")
            pdf_name = pdf_field_mapping.get(app_name)
            rect_info = pdf_field_rects.get(pdf_name) if pdf_name else None

            # If automatic mapping did not provide an AcroForm rectangle, the
            # embedded master-mask coordinates are already in 200-dpi image space.
            if rect_info:
                page_index, x1, y1, x2, y2 = rect_info
            else:
                page_index = int(field.get("page", 0))
                x1, y1, x2, y2 = (
                    field.get("x1", 0), field.get("y1", 0),
                    field.get("x2", 0), field.get("y2", 0)
                )

            if page_index < 0 or page_index >= len(actual_pages):
                continue

            page_img = actual_pages[page_index]
            left = max(0, int(round(float(x1))))
            top = max(0, int(round(float(y1))))
            right = min(page_img.width, int(round(float(x2))))
            bottom = min(page_img.height, int(round(float(y2))))
            if right - left < 3 or bottom - top < 3:
                continue

            # Give handwriting a small margin because signatures frequently cross
            # the exact PDF widget rectangle by a few pixels.
            mx = max(2, int((right - left) * 0.02))
            my = max(2, int((bottom - top) * 0.12))
            left2 = max(0, left - mx)
            right2 = min(page_img.width, right + mx)
            top2 = max(0, top - my)
            bottom2 = min(page_img.height, bottom + my)

            actual_crop = page_img.crop((left2, top2, right2, bottom2))
            base_crop = None
            if page_index < len(base_pages):
                base_page = base_pages[page_index]
                if base_page.size == page_img.size:
                    base_crop = base_page.crop((left2, top2, right2, bottom2))

            extracted = _extract_flattened_signature_crop(actual_crop, base_crop)
            if extracted is None:
                continue

            target = _pdf_signature_cache_path(pdf_file, app_name, f"flattened_p{page_index + 1}")
            extracted.save(target, format="PNG")
            extracted.close()
            recovered[app_name] = str(target)
            print("RECOVERED FLATTENED PDF SIGNATURE:", app_name, "->", target)

    except Exception as e:
        print("FLATTENED SIGNATURE LOAD ERROR:", e)
        traceback.print_exc()
    finally:
        for img in actual_pages:
            try:
                img.close()
            except Exception:
                pass
        for img in base_pages:
            try:
                img.close()
            except Exception:
                pass

    return recovered

def load_embedded_signature_data(pdf_file):
    """Restore self-contained signature PNG data stored in PADI Manager metadata."""
    recovered = {}
    field_lookup = _signature_field_lookup()

    try:
        reader = PdfReader(str(pdf_file))
        metadata = reader.metadata or {}
        payload = metadata.get("/PADIManagerSignatureData")
        if not payload:
            return recovered

        data = json.loads(str(payload))
        if not isinstance(data, dict):
            return recovered

        for stored_name, encoded in data.items():
            app_name = field_lookup.get(str(stored_name).strip().lower())
            if not app_name or not encoded:
                continue
            try:
                raw = base64.b64decode(str(encoded), validate=True)
                # Validate that the payload is an actual image before caching it.
                with Image.open(io.BytesIO(raw)) as test_img:
                    test_img.verify()

                target = _pdf_signature_cache_path(pdf_file, app_name, "embedded")
                target.write_bytes(raw)
                recovered[app_name] = str(target)
                print("RECOVERED EMBEDDED PDF SIGNATURE:", app_name, "->", target)
            except Exception as e:
                print("EMBEDDED SIGNATURE READ WARNING:", app_name, e)
    except Exception as e:
        print("EMBEDDED SIGNATURE LOAD ERROR:", e)

    return recovered


def build_embedded_signature_payload(signature_state):
    """Return compact JSON containing the signature images currently used by this PDF."""
    payload = {}
    for f in fields:
        if f.get("type") != "signature":
            continue
        name = f.get("name")
        value = signature_state.get(name)
        if not value:
            continue
        resolved = resolve_signature_path(value)
        if not resolved or not resolved.exists():
            continue
        try:
            payload[name] = base64.b64encode(resolved.read_bytes()).decode("ascii")
        except Exception as e:
            print("SIGNATURE EMBED WARNING:", name, e)

    return json.dumps(payload, separators=(",", ":")) if payload else ""


def load_pdf_field_values(pdf_file):

    values = {}

    try:

        reader = PdfReader(pdf_file)

        pdf_fields = reader.get_fields()

        print("\n========================")
        print("ACTUAL PDF FIELD NAMES")
        print("========================")

        for name in sorted(pdf_fields.keys()):
            print(repr(name))

        print("========================\n")

        for name, info in pdf_fields.items():

            if info.get("/FT") == "/Btn":

                print("\nCHECKBOX FIELD:", name)

                for k, v in info.items():
                    print("   ", k, "=", v)

        print("================================")
        print("PDF FIELDS FROM EXPORTED FILE")
        print("================================")
        print(pdf_fields)

        if not pdf_fields:
            print("NO FIELDS FOUND")
            return values

        for field_name, info in pdf_fields.items():

            print("\n================================")
            print("FIELD:", field_name)
            print("================================")

            for k, v in info.items():
                print(k, "=", v)

            value = info.get("/V")

            print("VALUE =", value)
            print("FT    =", info.get("/FT"))

            if value is not None:
                values[field_name] = str(value)

        print("LOADED VALUES =", values)

    except Exception as e:

        print("FIELD LOAD ERROR:", e)

    return values


def pdf_values_to_state(pdf_values):
    """
    Convert raw PDF AcroForm values into the application's state dictionary.
    Signature fields in PDFs contain only metadata and must be ignored.
    """

    loaded_state = {}

    for app_name, pdf_name in pdf_field_mapping.items():

        # Skip if PDF field not present
        if pdf_name not in pdf_values:
            continue

        value = pdf_values[pdf_name]

        # Find field info from mask
        field_info = next((f for f in fields if f["name"] == app_name), None)
        if not field_info:
            continue

        # ⭐ SIGNATURE FIX ⭐
        # Ignore ALL signature fields from PDF
        if field_info["type"] == "signature":
            continue

        # Checkbox handling
        if field_info["type"] == "checkbox":
            loaded_state[app_name] = (
                str(value).lower() not in ("/off", "off", "", "false")
            )
            continue

        # Normal text fields
        loaded_state[app_name] = value

    return loaded_state


def load_pdf():

    global pdf_path
    global pages
    global current_page
    global zoom_level
    global state
    global reopened_exported_pdf
    global loaded_pdf_values
    global current_base_pdf_path
    global current_base_id

    pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")],
        title="Select a PADI PDF"
    )

    if not pdf_path:
        pdf_label.config(text="No PDF loaded")
        return

    #
    # INSPECT PDF
    #
    try:

        reader = PdfReader(pdf_path)

        pdf_fields = reader.get_fields()

        print("")
        print("================================")
        print("PDF FIELD TEST")
        print("================================")

        if pdf_fields:

            for name, info in pdf_fields.items():

                value = info.get("/V")

                print(
                    "FIELD:",
                    name,
                    "VALUE:",
                    value
                )

        else:

            print("NO ACROFORM FIELDS FOUND")

        print("================================")
        print("")

    except Exception as e:

        print("FIELD TEST ERROR:", e)

    pdf_label.config(
        text=f"Loaded: {Path(pdf_path).name}"
    )

    # Load the saved comment into the main-menu textbox.
    display_comment(pdf_path)

    #
    # DETECT WHETHER THIS IS A PREVIOUS PADI MANAGER EXPORT
    #
    # New exports carry /PADIManagerBaseID.  Older exports are detected from
    # meaningful AcroForm values.  /Off and false checkbox defaults do not count.
    current_base_id = _base_id_from_pdf(pdf_path)
    reopened_exported_pdf = bool(current_base_id)

    if not reopened_exported_pdf:
        try:
            reader = PdfReader(pdf_path)
            pdf_fields = reader.get_fields() or {}
            for field_name, info in pdf_fields.items():
                value = info.get("/V")
                if value not in (None, "", "/Off", "Off", False, 0):
                    reopened_exported_pdf = True
                    break
        except Exception as e:
            print("PDF DETECTION ERROR:", e)

    print("REOPENED EXPORTED PDF =", reopened_exported_pdf)
    print("PADI MANAGER BASE ID =", current_base_id)

    # Always start from the embedded master mask.
    fields.clear()
    fields.extend(load_fields())
    print("FIELDS FROM EMBEDDED MASTER MASK =", len(fields))

    # Resolve the pristine source PDF used as the viewer backdrop and export base.
    # This is the key fix for duplicate/stacked edits.
    current_base_pdf_path = None

    if current_base_id:
        current_base_pdf_path = _cached_base_for_id(current_base_id)
        if current_base_pdf_path:
            print("FOUND CACHED CLEAN BASE =", current_base_pdf_path)

    if current_base_pdf_path is None and not reopened_exported_pdf:
        # A blank/original form becomes the clean source for future updates.
        try:
            current_base_id, current_base_pdf_path = _cache_clean_template(pdf_path)
        except Exception as e:
            print("TEMPLATE CACHE WARNING:", e)
            current_base_pdf_path = Path(pdf_path)

    if current_base_pdf_path is None and reopened_exported_pdf:
        # Compatibility for exports created by an older PADI Manager version.
        fallback = _single_cached_template()
        if fallback is not None:
            current_base_pdf_path = fallback
            current_base_id = fallback.stem
            print("USING SINGLE CACHED TEMPLATE FOR LEGACY EXPORT =", fallback)
        else:
            # We can read/edit the file, but its previous static overlay cannot be
            # erased safely because merge_page permanently added it to page content.
            current_base_pdf_path = Path(pdf_path)
            print("WARNING: NO CLEAN BASE AVAILABLE FOR THIS LEGACY EXPORT")

    # Render the CLEAN BASE as the GUI backdrop.  Values are still read from
    # pdf_path below, so reopened edits remain editable without displaying the
    # old flattened/static text underneath the new Tk overlays.
    try:
        render_source = str(current_base_pdf_path or pdf_path)
        print("RENDERING CLEAN PDF BACKDROP =", render_source)
        pages = convert_from_path(render_source, dpi=200)
        print("PDF PAGES RENDERED =", len(pages))
        if not pages:
            raise RuntimeError("PDFium returned no rendered pages.")
        for page_no, page_image in enumerate(pages, start=1):
            print("PAGE", page_no, "SIZE =", page_image.size)
    except Exception as e:
        pages = []
        print("PDF RENDER ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Render Error",
            f"The PDF could not be rendered for display:\n\n{e}"
        )
        return

    #
    # Build field mapping only after rendered page dimensions are available.
    try:
        build_pdf_field_mapping()

        print("\n========= DUPLICATE TEST =========")
        seen = {}
        for app_field, pdf_field in pdf_field_mapping.items():
            print(app_field, "->", pdf_field)
            seen.setdefault(pdf_field, []).append(app_field)

        for pdf_field, apps in seen.items():
            if len(apps) > 1:
                print("DUPLICATE PDF FIELD:", pdf_field)
                print("USED BY:", apps)

        print("==================================")

        if reopened_exported_pdf:
            print("READING VALUES FROM EXPORTED PDF")
            pdf_values = load_pdf_field_values(pdf_path)
            print("PDF_VALUES =", pdf_values)
            state = pdf_values_to_state(pdf_values)

            # Signatures must be restored from THIS PDF only.  Never fall back
            # to state_padi.json or the selected instructor, because those are
            # global application state and can belong to another student/PDF.
            # Restore signatures from THIS PDF in priority order.  The sources
            # are merged rather than treated as all-or-nothing because a PDF can
            # contain a mixture of old flattened signatures and newer stamps.
            # Flattened-page recovery is lowest priority; explicit stamps override
            # it, and self-contained PADI Manager metadata is authoritative.
            pdf_signatures = load_flattened_signatures_from_pdf(pdf_path)
            pdf_signatures.update(load_signature_stamps_from_pdf(pdf_path))
            pdf_signatures.update(load_embedded_signature_data(pdf_path))

            state.update(pdf_signatures)
            print("SIGNATURES RESTORED FROM PDF =", pdf_signatures)

            print("Student Name in PDF =", pdf_values.get("Student Name"))
            print("Student Name mapping =", pdf_field_mapping.get("Student Name"))
            print("STATE LOADED FROM PDF =", state)
        else:
            print("BLANK TEMPLATE PDF")
            state = {}

        loaded_pdf_values = dict(state)
        print("STATE AFTER LOAD =", state)
        print("STUDENT NAME AFTER LOAD =", state.get("Student Name"))

    except Exception as e:
        print("PDF FIELD/MASK LOAD ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Load Error",
            f"Failed to prepare the PDF:\n{e}"
        )
        state = {}
        loaded_pdf_values = {}

    current_page = 0
    zoom_level = zoom_level_def

    root.update_idletasks()
    render_page()
    global _main_pdf_saved_snapshot
    _main_pdf_saved_snapshot = _main_pdf_snapshot()


def close_pdf():
    if _main_pdf_is_dirty() and not messagebox.askyesno(
        "Unsaved PDF Changes",
        "The Open Water PDF contains changes that have not been exported.\n\nClose it without saving?",
        parent=root
    ):
        return

    global pdf_path
    global pages
    global current_page
    global state
    global fields
    global loaded_pdf_values
    global pdf_field_mapping
    global reopened_exported_pdf
    global current_base_pdf_path
    global current_base_id

    pdf_path = None
    pages = []
    current_page = 0

    state = {}
    fields.clear()

    loaded_pdf_values = {}
    pdf_field_mapping = {}
    reopened_exported_pdf = False
    current_base_pdf_path = None
    current_base_id = None

    canvas_pdf.delete("all")

    canvas_pdf.config(
        scrollregion=(0, 0, 0, 0)
    )

    if hasattr(canvas_pdf, "signature_images"):
        canvas_pdf.signature_images.clear()

    pdf_label.config(
        text="No PDF loaded"
    )

    if "comment_text" in globals():
        comment_text.delete("1.0", "end")
        update_comment_box_color()

    status_label.config(
        text="PDF and Mask Closed"
    )


def next_page():
    global current_page
    if not pages:
        return
    if current_page < len(pages) - 1:
        current_page += 1
        render_page()

def prev_page():
    global current_page
    if not pages:
        return
    if current_page > 0:
        current_page -= 1
        render_page()

# ---------------- Zoom Controls ----------------

def zoom_in():
    global zoom_level
    if zoom_level < MAX_ZOOM:
        zoom_level += ZOOM_STEP
        render_page()

def zoom_out():
    global zoom_level
    if zoom_level > MIN_ZOOM:
        zoom_level -= ZOOM_STEP
        render_page()

def zoom_fit():
    global zoom_level
    if not pages:
        return

    page = pages[current_page]
    w, h = page.size

    canvas_w = canvas_pdf.winfo_width()
    canvas_h = canvas_pdf.winfo_height()

    zoom_w = canvas_w / w
    zoom_h = canvas_h / h

    zoom_level = min(zoom_w, zoom_h)
    render_page()

# ---------------- Field Detection ----------------

def find_field(x, y, page_index):
    for f in fields:
        if f.get("page", 0) != page_index:
            continue
        if f["x1"] <= x <= f["x2"] and f["y1"] <= y <= f["y2"]:
            return f
    return None


def action_field_info(field):
    """Return a short description for fields whose click triggers multiple updates."""
    if not field:
        return None

    name = str(field.get("name", "")).strip().lower()

    if re.fullmatch(r"cw\d+_day", name):
        prefix = name.rsplit("_", 1)[0].upper()
        return (
            f"{prefix} auto-fill\n"
            "Click to fill date, instructor initials and PADI number."
        )

    if re.fullmatch(r"init_padi_instructor_\d+", name):
        return (
            "Instructor auto-fill\n"
            "Click to fill instructor, PADI number, store, contact, signature and date."
        )

    if re.fullmatch(r"instructor_signature_\d+", name):
        return (
            "Instructor sign-off\n"
            "Click to add/remove the selected instructor signature, PADI number and date."
        )

    if re.fullmatch(r"dive_\d+", name):
        return (
            "Dive counter / auto-fill\n"
            "Click to cycle the dive count and update instructor initials/PADI number."
        )

    if name == "student_signature":
        return (
            "Student signature\n"
            "Click to add/replace the student signature and student signing date."
        )

    return None


def is_action_field(field):
    return action_field_info(field) is not None


def populate_cw_row(prefix):
    """Populate day, month, year, initials, and PADI# for a CW row."""

    # Date fields
    d = date_picker.get_date()

    state[f"{prefix}_day"] = str(d.day)
    state[f"{prefix}_month"] = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ][d.month - 1]

    state[f"{prefix}_year"] = str(d.year)

    # Instructor fields
    selected_name = instructor_var.get()

    instructor = next(
        (
            i for i in instructor_list
            if i["name"] == selected_name
        ),
        None
    )

    if instructor:

        state[f"{prefix}_initials"] = instructor.get(
            "initials",
            ""
        )

        state[f"{prefix}_padi"] = instructor.get(
            "padi_number",
            ""
        )

        # Auto-credit Confined Dive 4 when CW12 is completed
        if prefix == "CW12":

            state["Dive_4"] = "CONF"

            state["Dive_initials_4"] = instructor.get(
                "initials",
                ""
            )

            state["Dive_padi_4"] = instructor.get(
                "padi_number",
                ""
            )

    redraw_all_text_fields()
    redraw_all_signatures()

def redraw_all_text_fields():

    print(
        "ALL ITEMS BEFORE DELETE =",
        canvas_pdf.find_all()
    )

    print(
        "TEXT ITEMS BEFORE DELETE =",
        canvas_pdf.find_withtag("text_drawn")
    )

    canvas_pdf.delete("text_drawn")

    print(
        "TEXT ITEMS AFTER DELETE =",
        canvas_pdf.find_withtag("text_drawn")
    )

    canvas_pdf.delete("text_drawn") 

    if state is None:
        print("ERROR: state is None")
        return

    for f in fields:

        if f.get("page", 0) != current_page:
            continue

        if f["type"] not in ("day", "month", "year", "text"):
            continue

        if f["name"] == "Student Name":
            print(
                "DRAW STUDENT NAME:",
                repr(state.get(f["name"])),
                f["x1"],
                f["y1"]
            )

        value = state.get(f["name"])

        print(
            "DRAW:",
            repr(f["name"]),
            "=",
            repr(value)
        )

        if not value:
            continue

        x = int(f["x1"] * zoom_level)
        y = int(f["y1"] * zoom_level)

        print(
            "COORD:",
            f["name"],
            f["x1"],
            f["y1"]
        )
        item = canvas_pdf.create_text(
            x,
            y,
            anchor="nw",
            text=str(value),
            fill="black",
            font=("Helvetica", 10),
            tags="text_drawn"
        )


    # force text above image
    canvas_pdf.tag_raise("text_drawn")

    # keep boxes above text
    canvas_pdf.tag_raise("field_box")


def start_inline_edit(field):

    print("********************************")
    print("START_INLINE_EDIT CALLED")
    print("FIELD =", field["name"])
    print("STATE VALUE =", state.get(field["name"]))
    print("********************************")

    global editing_active
    global current_inline_entry

    if editing_active:
        return

    # Destroy any previous editor
    if current_inline_entry:
        try:
            current_inline_entry.destroy()
        except:
            pass

        current_inline_entry = None

    editing_active = True

    canvas_pdf.unbind("<Button-1>")

    current_value = state.get(field["name"], "")

    print("CURRENT VALUE =", repr(current_value))

    entry_var = tk.StringVar(value=current_value)

    entry = tk.Entry(
        canvas_pdf,
        textvariable=entry_var,
        width=20
    )

    current_inline_entry = entry
    globals()["_active_inline_field_name"] = field["name"]

    x = int(field["x1"] * zoom_level)
    y = int(field["y1"] * zoom_level)

    # hide existing drawn text while editing
    #canvas_pdf.delete("text_drawn")

    entry_window = canvas_pdf.create_window(
        x,
        y,
        anchor="nw",
        window=entry
    )

    def save_inline(event=None):

        global editing_active
        global current_inline_entry

        new_value = entry_var.get()

        print("ENTRY VALUE =", repr(new_value))

        state[field["name"]] = new_value

        print(
            "SAVED:",
            field["name"],
            "=",
            state[field["name"]]
        )

        canvas_pdf.delete(entry_window)

        if entry.winfo_exists():
            entry.destroy()

        current_inline_entry = None
        editing_active = False

        canvas_pdf.bind("<Button-1>", on_pdf_click)

        #redraw_all_text_fields()
        #save_state_with_locations()
        render_page()
        save_state_with_locations()

    def cancel_inline(event=None):

        global editing_active
        global current_inline_entry

        canvas_pdf.delete(entry_window)

        if entry.winfo_exists():
            entry.destroy()

        current_inline_entry = None
        editing_active = False

        canvas_pdf.bind("<Button-1>", on_pdf_click)

        #redraw_all_text_fields()
        render_page()

    entry.bind("<Return>", save_inline)
    entry.bind("<Escape>", cancel_inline)

    entry.focus_set()
    entry.select_range(0, tk.END)



def redraw_all_checkboxes():

    canvas_pdf.delete("checkbox_drawn")

    for f in fields:

        if f.get("page", 0) != current_page:
            continue

        if f["type"] != "checkbox":
            continue

        checked = bool(state.get(f["name"], False))

        if not checked:
            continue

        x1 = int(f["x1"] * zoom_level)
        y1 = int(f["y1"] * zoom_level)
        x2 = int(f["x2"] * zoom_level)
        y2 = int(f["y2"] * zoom_level)

        canvas_pdf.create_text(
            (x1 + x2) // 2,
            (y1 + y2) // 2,
            text="✓",
            fill="black",
            font=("Arial", 14, "bold"),
            tags="checkbox_drawn"
        )
   

def on_pdf_click(event):
    global editing_active

    if editing_active:
        return

    if not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)

    if not field:
        return

    global identify_mode, rename_mode

    print(
        "CLICKED:",
        field["name"],
        "rename_mode=",
        rename_mode
    )

    # ---------------------------
    # IDENTIFY MODE
    # ---------------------------

    if identify_mode:

        info = (
            f"Field Name: {field['name']}\n"
            f"Type: {field['type']}\n"
            f"Page: {field['page']}\n"
            f"Coordinates:\n"
            f"  x1={field['x1']}, y1={field['y1']}\n"
            f"  x2={field['x2']}, y2={field['y2']}"
        )

        messagebox.showinfo(
            "Field Info",
            info
        )

        print("FIELD JSON ENTRY:", field)

        return

    # ---------------------------
    # RENAME MODE
    # ---------------------------

    if rename_mode:

        new_name = simpledialog.askstring(
            "Rename Field",
            f"Enter new name for field '{field['name']}':",
            initialvalue=field["name"]
        )

        if new_name:

            field["name"] = new_name

            save_fields(fields)

            draw_all_field_boxes()
            redraw_all_text_fields()
            redraw_all_signatures()

            messagebox.showinfo(
                "Renamed",
                f"Field renamed to '{new_name}'"
            )

        return

    # ---------------------------
    # DIVE COUNTER
    # ---------------------------

    m = re.fullmatch(
        r"dive_(\d+)",
        field["name"].lower()
    )

    if m:

        dive_num = m.group(1)

        instructor = next(
            (
                i for i in instructor_list
                if i["name"] == instructor_var.get()
            ),
            None
        )

        current_value = state.get(
            field["name"],
            ""
        )

        if current_value == "":
            current_value = "1"
        elif current_value == "1":
            current_value = "2"
        elif current_value == "2":
            current_value = "3"
        elif current_value == "3":
            current_value = "4"
        else:
            current_value = ""

        state[field["name"]] = current_value

        if current_value == "":

            state[f"Dive_initials_{dive_num}"] = ""
            state[f"Dive_padi_{dive_num}"] = ""

        elif instructor:

            state[f"Dive_initials_{dive_num}"] = (
                instructor.get("initials", "")
            )

            state[f"Dive_padi_{dive_num}"] = (
                instructor.get("padi_number", "")
            )

        redraw_all_text_fields()
        save_state_with_locations()

        return

    # ---------------------------
    # CHECKBOX
    # ---------------------------

    if field["type"] == "checkbox":

        current_value = bool(
            state.get(field["name"], False)
        )

        state[field["name"]] = (
            not current_value
        )

        redraw_all_checkboxes()
        save_state_with_locations()

        return

    # ---------------------------
    # CW AUTO POPULATE
    # ---------------------------

    if field["name"].lower().endswith("_day"):

        name = field["name"].lower()

        m = re.search(
            r"(cw\d+)",
            name
        )

        if m:

            prefix = m.group(1).upper()

            populate_cw_row(prefix)

            return

    # ---------------------------
    # STUDENT SIGNATURE
    # ---------------------------

    if (
        field["name"]
        .strip()
        .lower()
        == "student_signature"
    ):

        existing_sig = state.get(
            field["name"]
        )

        if (
            existing_sig
            and resolve_signature_path(existing_sig).exists()
        ):

            answer = messagebox.askyesno(
                "Warning",
                "This student signature already exists.\n\n"
                "Replacing a signature may invalidate a previously "
                "signed training record.\n\n"
                "Do you want to continue?"
            )

            if not answer:
                return

        draw_student_signature_window(
            field["name"]
        )

        return

    # ---------------------------
    # INIT PADI INSTRUCTOR
    # ---------------------------

    m = re.fullmatch(
    r"init_padi_instructor_(\d+)",
    field["name"].strip().lower()
)

    if m:

        instructor_num = m.group(1)

        selected_name = instructor_var.get()

        if not selected_name:
            messagebox.showerror(
                "Error",
                "Select an instructor first."
            )
            return

        instructor = next(
            (i for i in instructor_list
            if i["name"] == selected_name),
            None
        )

        # Toggle OFF
        if state.get(field["name"]):

            state.pop(field["name"], None)

            state.pop(f"Init_PADI_no_{instructor_num}", None)
            state.pop(f"Init_Dive_Resort_No_{instructor_num}", None)
            state.pop(f"Init_Email_{instructor_num}", None)
            state.pop(f"Init_Phone_{instructor_num}", None)

            state.pop(
                f"Init_Instructor_Signature_{instructor_num}",
                None
            )

            state.pop(f"Init_day_{instructor_num}", None)
            state.pop(f"Init_month_{instructor_num}", None)
            state.pop(f"Init_year_{instructor_num}", None)

        # Toggle ON
        else:

            state[field["name"]] = selected_name

            if instructor:

                state[f"Init_PADI_no_{instructor_num}"] = \
                    instructor.get("padi_number", "")

                state[f"Init_Dive_Resort_No_{instructor_num}"] = \
                    instructor.get("store_number", "")

                state[f"Init_Email_{instructor_num}"] = \
                    instructor.get("email", "")

                state[f"Init_Phone_{instructor_num}"] = \
                    instructor.get("phone", "")

                sig_path = instructor.get("signature")

                if sig_path and resolve_signature_path(sig_path).exists():
                    state[
                        f"Init_Instructor_Signature_{instructor_num}"
                    ] = str(resolve_signature_path(sig_path))

            d = date_picker.get_date()

            state[f"Init_day_{instructor_num}"] = str(d.day)

            state[f"Init_month_{instructor_num}"] = [
                "Jan","Feb","Mar","Apr",
                "May","Jun","Jul","Aug",
                "Sep","Oct","Nov","Dec"
            ][d.month - 1]

            state[f"Init_year_{instructor_num}"] = str(d.year)

        redraw_all_text_fields()
        redraw_all_signatures()
        save_state_with_locations()

        return 

    # ---------------------------
    # INSTRUCTOR SIGNATURE
    # ---------------------------

    # ---------------------------
# INSTRUCTOR SIGNATURE
# ---------------------------

    m = re.fullmatch(
        r"instructor_signature_(\d+)",
        field["name"].strip().lower()
    )

    if m:

        selected_name = instructor_var.get()

        if not selected_name:
            messagebox.showerror(
                "Error",
                "Select an instructor first."
            )
            return

        instructor = next(
            (
                i for i in instructor_list
                if i["name"] == selected_name
            ),
            None
        )

        if not instructor:
            return

        signoff_num = m.group(1)

        # Toggle OFF
        if state.get(field["name"]):

            state.pop(field["name"], None)

            state.pop(f"PADI_no_{signoff_num}", None)
            state.pop(f"day_{signoff_num}", None)
            state.pop(f"month_{signoff_num}", None)
            state.pop(f"year_{signoff_num}", None)

        # Toggle ON
        else:

            sig_path = instructor.get("signature")

            if sig_path and resolve_signature_path(sig_path).exists():

                state[field["name"]] = sig_path

                state[f"PADI_no_{signoff_num}"] = (
                    instructor.get("padi_number", "")
                )

                d = date_picker.get_date()

                state[f"day_{signoff_num}"] = str(d.day)

                state[f"month_{signoff_num}"] = [
                    "Jan","Feb","Mar","Apr",
                    "May","Jun","Jul","Aug",
                    "Sep","Oct","Nov","Dec"
                ][d.month - 1]

                state[f"year_{signoff_num}"] = str(d.year)

        redraw_all_text_fields()
        redraw_all_signatures()
        save_state_with_locations()

        return

    # ---------------------------
    # NORMAL TEXT EDIT
    # ---------------------------

    start_inline_edit(field)


def on_pdf_right_click_normal(event):
    global editing_active
    if editing_active:
        return

    if not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)
    if not field:
        return

    if field["type"] in ("text", "day", "month", "year"):

        for child in canvas_pdf.place_slaves():
            child.destroy()

        entry_var = tk.StringVar(value=state.get(field["name"], ""))

        entry = tk.Entry(canvas_pdf, textvariable=entry_var, width=20)

        x = int(field["x1"] * zoom_level)
        y = int(field["y1"] * zoom_level)
        
        entry_window = canvas_pdf.create_window(
            x,
            y,
            anchor="nw",
            window=entry
        )

        
        
        def save_entry(event=None):
            state[field["name"]] = entry_var.get()
            save_state_with_locations()

            print("ENTRY EXISTS BEFORE =", entry.winfo_exists())
            entry.destroy()
            print("ENTRY EXISTS AFTER =", entry.winfo_exists())

            redraw_all_text_fields()
            
        entry.bind("<Return>", save_entry)
        entry.focus_set()




# ---------------- Hover Highlight ----------------

hover_field = None

def on_pdf_motion(event):
    global editing_active, zoom_level
    if editing_active:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    global hover_field
    new_field = find_field(scaled_x, scaled_y, current_page)

    #
    # SHOW TOOLTIP FOR ACTION / AUTO-FILL FIELDS
    #
    global tooltip_window

    action_tip = action_field_info(new_field)

    if action_tip:

        if tooltip_window is None:
            tooltip_window = tk.Toplevel(root)
            tooltip_window.overrideredirect(True)
            tooltip_window._label = tk.Label(
                tooltip_window,
                text=action_tip,
                bg="lightyellow",
                relief="solid",
                borderwidth=1,
                justify="left",
                padx=5,
                pady=3
            )
            tooltip_window._label.pack()
        else:
            try:
                tooltip_window._label.config(text=action_tip)
            except Exception:
                pass

        tooltip_window.geometry(
            f"+{event.x_root + 15}+{event.y_root + 15}"
        )

    else:

        if tooltip_window:
            tooltip_window.destroy()
            tooltip_window = None

    if new_field is hover_field:
        return

    hover_field = new_field

    draw_all_field_boxes()

    #if new_field:
   #  print("HOVER:", repr(new_field["name"]))

def on_pdf_leave(event):

    global tooltip_window

    if tooltip_window:
        tooltip_window.destroy()
        tooltip_window = None


def draw_all_field_boxes():

    global editing_active
    global zoom_level

    if editing_active:
        return

    canvas_pdf.delete("field_box")

    for f in fields:

        if f.get("page", 0) != current_page:
            continue

        x1 = int(f["x1"] * zoom_level)
        y1 = int(f["y1"] * zoom_level)
        x2 = int(f["x2"] * zoom_level)
        y2 = int(f["y2"] * zoom_level)

        outline_color = "blue"
        width = 1
        dash = None

        # Orange dashed boxes identify fields that perform an action and
        # populate/update several related fields when clicked.
        if is_action_field(f):
            outline_color = "darkorange"
            width = 2
            dash = (5, 3)

        if hover_field is f:
            outline_color = "red"
            width = 3
            dash = None

        canvas_pdf.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline=outline_color,
            width=width,
            dash=dash,
            tags="field_box"
        )

# ---------------- Mask Editor ----------------

mask_edit_mode = False
drag_start = None
identify_mode = False
rename_mode = False


def bind_mask_edit_events():
    canvas_pdf.bind("<ButtonPress-3>", on_pdf_button_press)
    canvas_pdf.bind("<ButtonRelease-3>", on_pdf_button_release)

def unbind_mask_edit_events():
    canvas_pdf.unbind("<ButtonPress-3>")
    canvas_pdf.unbind("<ButtonRelease-3>")
    canvas_pdf.unbind("<Button-3>")




def toggle_mask_edit():
    global mask_edit_mode, identify_mode, rename_mode

    mask_edit_mode = not mask_edit_mode

    if mask_edit_mode:
        identify_mode = False
        rename_mode = False

        bind_mask_edit_events()

        status_label.config(
            text="Mask Edit Mode: ON (left drag=create field, right click=delete field)"
        )

    else:
        unbind_mask_edit_events()

        # Restore normal handlers
        canvas_pdf.bind("<Button-1>", on_pdf_click)
        canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal)
        if IS_MACOS:
            canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal)

        status_label.config(text="Mask Edit Mode: OFF")
    update_button_colors()


def toggle_rename_mode():
    global rename_mode, identify_mode, mask_edit_mode

    rename_mode = not rename_mode
    print("RENAME MODE =", rename_mode)
    
    if rename_mode:
        # Disable other modes
        identify_mode = False
        mask_edit_mode = False
        unbind_mask_edit_events()

        # Restore left-click handler for rename mode
        canvas_pdf.bind("<Button-1>", on_pdf_click)

        # Remove right-click text entry
        canvas_pdf.unbind("<Button-3>")

        status_label.config(text="Rename Mode: Click a field to rename it")

    else:
        # Restore normal right-click behavior
        canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal, add="+")
        if IS_MACOS:
            canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal, add="+")
        status_label.config(text="Rename Mode: OFF")

    update_button_colors()



def on_pdf_button_press(event):
    global drag_start

    global editing_active
    if editing_active:
        return

    if not mask_edit_mode or not pages:
        return


    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    drag_start = (canvas_x, canvas_y)

def on_pdf_button_release(event):
    global editing_active
    if editing_active:
        return

    if not mask_edit_mode or not pages or drag_start is None:
        return


    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    x1_canvas, y1_canvas = drag_start
    x2_canvas, y2_canvas = canvas_x, canvas_y

    if abs(x2_canvas - x1_canvas) < 5 or abs(y2_canvas - y1_canvas) < 5:
        drag_start = None
        return

    x1 = int(min(x1_canvas, x2_canvas) / zoom_level)
    y1 = int(min(y1_canvas, y2_canvas) / zoom_level)
    x2 = int(max(x1_canvas, x2_canvas) / zoom_level)
    y2 = int(max(y1_canvas, y2_canvas) / zoom_level)

    new_field = {
        "name": f"field_{len(fields)+1}",
        "type": "signature",
        "page": current_page,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    }

    fields.append(new_field)
    messagebox.showinfo("Field Created", "Field added to the current session.")

    #save_fields(fields)  
    draw_all_field_boxes()

    messagebox.showinfo(
        "Field Created",
        f"New signature field created:\n{new_field['name']}\nPage {current_page}"
    )

    drag_start = None

def redraw_all_signatures():
    canvas_pdf.delete("signature_drawn")
    canvas_pdf.signature_images = []   # ⭐ REQUIRED FIX

    for f in fields:
        if f.get("page", 0) != current_page:
            continue
        if f["type"] != "signature":
            continue

        sig_path = state.get(f["name"])
        if not isinstance(sig_path, str):
            continue

        if not resolve_signature_path(sig_path).exists():
            continue


        img = Image.open(resolve_signature_path(sig_path))
        w = int((f["x2"] - f["x1"]) * zoom_level)
        h = int((f["y2"] - f["y1"]) * zoom_level)
        img = img.resize((w, h), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(img)
        canvas_pdf.signature_images.append(tk_img)

        x = int(f["x1"] * zoom_level)
        y = int(f["y1"] * zoom_level)

        canvas_pdf.create_image(x, y, anchor="nw", image=tk_img, tags="signature_drawn")


# ---------------- Date Control Handler ----------------

def on_date_changed(event=None):
    """Store the date selected in the stable top-menu calendar."""
    current_date = date_picker.get_date()
    print("DATE PICKER =", current_date)
    state["global_selected_date"] = current_date.strftime("%Y-%m-%d")

# ---------------- Dynamic Widgets ----------------

def show_field_widget(field):
    for child in widget_frame.winfo_children():
        child.destroy()

    ftype = field["type"]
    name = field["name"]

    selected_name = instructor_var.get()
    instructor = next((i for i in instructor_list if i["name"] == selected_name), None)

    # Automatically sync granular date items using the top menu selection fallback context
    if ftype == "day":
        default_day = str(date_picker.get_date().day)
        values = [str(i) for i in range(1, 32)]
        var = tk.StringVar(value=state.get(name, default_day))
        cb = ttk.Combobox(widget_frame, values=values, textvariable=var, width=4)
        cb.pack(side="left")
        set_field_value(name, var.get())
        cb.bind("<<ComboboxSelected>>", lambda e: set_field_value(name, var.get()))

    elif ftype == "month":
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        default_month = months[date_picker.get_date().month - 1]
        var = tk.StringVar(value=state.get(name, default_month))
        cb = ttk.Combobox(widget_frame, values=months, textvariable=var, width=6)
        cb.pack(side="left")
        set_field_value(name, var.get())
        cb.bind("<<ComboboxSelected>>", lambda e: set_field_value(name, var.get()))

    elif ftype == "year":
        default_year = str(date_picker.get_date().year)
        values = [str(y) for y in range(2020, 2035)]
        var = tk.StringVar(value=state.get(name, default_year))
        cb = ttk.Combobox(widget_frame, values=values, textvariable=var, width=6)
        cb.pack(side="left")
        set_field_value(name, var.get())
        cb.bind("<<ComboboxSelected>>", lambda e: set_field_value(name, var.get()))

    elif ftype == "text":
        var = tk.StringVar(value=state.get(name, ""))
        entry = tk.Entry(widget_frame, textvariable=var, width=40)
        entry.pack(side="left")
        entry.bind("<Return>", lambda e: set_field_value(name, var.get()))

    elif ftype == "checkbox":
        var = tk.BooleanVar(value=bool(state.get(name, False)))
        cb = tk.Checkbutton(widget_frame, text=name, variable=var,
                            command=lambda: set_field_value(name, var.get()))
        cb.pack(side="left")

    elif ftype == "signature":
        if not instructor:
            messagebox.showerror("Error", "Select an instructor first.")
            return

        sig_path = instructor.get("signature")
        if not sig_path or not resolve_signature_path(sig_path).exists():
            messagebox.showerror("Error", "Instructor has no saved signature or file missing.")
            return

        set_field_value(name, sig_path)
        place_signature_on_canvas(field, sig_path)

def set_field_value(name, value):
    state[name] = value

# ---------------- PDF Export ----------------
from pypdf.generic import NameObject, BooleanObject, NumberObject

def _fit_font_size(text, box_width, box_height, start_size=9.0, min_size=4.5):
    if not text:
        return start_size

    size = start_size
    estimated_width = max(1.0, len(text) * 0.52)

    if estimated_width * size > box_width:
        size = box_width / estimated_width

    return max(min_size, min(start_size, size))


def _draw_static_form_values(page_canvas, page_index, pdf_values):
    """
    Draw form values directly into the PDF page.

    This is necessary because some PDF viewers/renderers do not display
    AcroForm appearance streams generated by pypdf.  The AcroForm values are
    still retained for later retrieval by the application.
    """
    for pdf_name, value in pdf_values.items():
        rect_info = pdf_field_rects.get(pdf_name)
        if not rect_info:
            continue

        field_page, x1_img, y1_img, x2_img, y2_img = rect_info
        if field_page != page_index:
            continue

        field_type = "text"

        for app_name, mapped_name in pdf_field_mapping.items():
            if mapped_name == pdf_name:
                info = next(
                    (f for f in fields if f["name"] == app_name),
                    None
                )
                if info:
                    field_type = info.get("type", "text")
                break

        scale = 200.0 / 72.0
        page_w, page_h = page_canvas._pagesize

        x1 = float(x1_img) / scale
        x2 = float(x2_img) / scale
        y_bottom = page_h - (float(y2_img) / scale)
        y_top = page_h - (float(y1_img) / scale)

        width = max(1.0, x2 - x1)
        height = max(1.0, y_top - y_bottom)

        if field_type == "signature":
            continue

        if field_type == "checkbox":
            if str(value) in ("/Yes", "Yes", "True", "true", "1"):
                page_canvas.setLineWidth(
                    max(0.8, min(1.5, height * 0.12))
                )
                page_canvas.line(
                    x1 + width * 0.18,
                    y_bottom + height * 0.48,
                    x1 + width * 0.42,
                    y_bottom + height * 0.20
                )
                page_canvas.line(
                    x1 + width * 0.42,
                    y_bottom + height * 0.20,
                    x1 + width * 0.82,
                    y_bottom + height * 0.80
                )
            continue

        text = str(value)
        if not text:
            continue

        font_size = _fit_font_size(
            text,
            width - 2,
            height - 1,
            start_size=min(9.0, max(6.0, height * 0.70))
        )

        page_canvas.setFont("Helvetica", font_size)
        page_canvas.setFillColorRGB(0, 0, 0)

        baseline = y_bottom + max(
            1.0,
            (height - font_size) / 2.0
        )

        page_canvas.drawString(
            x1 + 1,
            baseline,
            text
        )


def _add_signature_stamp_annotation(writer, page_num, image_path, x, y, width, height, field_name="Signature"):
    """Add a visible, removable PDF Stamp annotation containing a signature PNG.

    Unlike merge_page(), this does not burn the signature into page content.
    Standard annotation-aware PDF editors can select/delete the signature.
    """
    if width <= 0 or height <= 0:
        return

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.drawImage(
        ImageReader(image_path),
        0,
        0,
        width=width,
        height=height,
        mask="auto"
    )
    c.save()
    packet.seek(0)

    appearance_reader = PdfReader(packet)
    appearance_page = appearance_reader.pages[0]
    contents = appearance_page.get_contents()
    appearance_data = contents.get_data() if contents is not None else b""

    appearance = DecodedStreamObject()
    appearance.set_data(appearance_data)
    appearance[NameObject("/Type")] = NameObject("/XObject")
    appearance[NameObject("/Subtype")] = NameObject("/Form")
    appearance[NameObject("/FormType")] = NumberObject(1)
    appearance[NameObject("/BBox")] = ArrayObject([
        FloatObject(0), FloatObject(0), FloatObject(width), FloatObject(height)
    ])

    resources = appearance_page.get("/Resources")
    if resources is not None:
        resources = resources.get_object() if hasattr(resources, "get_object") else resources
        appearance[NameObject("/Resources")] = resources.clone(writer)

    appearance_ref = writer._add_object(appearance)

    annotation = DictionaryObject()
    annotation[NameObject("/Type")] = NameObject("/Annot")
    annotation[NameObject("/Subtype")] = NameObject("/Stamp")
    annotation[NameObject("/Rect")] = ArrayObject([
        FloatObject(x), FloatObject(y),
        FloatObject(x + width), FloatObject(y + height)
    ])
    annotation[NameObject("/Contents")] = TextStringObject(str(field_name))
    annotation[NameObject("/Name")] = NameObject("/Approved")
    # Print the annotation, but do not lock it. It remains removable/editable.
    annotation[NameObject("/F")] = NumberObject(4)
    annotation[NameObject("/AP")] = DictionaryObject({
        NameObject("/N"): appearance_ref
    })

    writer.add_annotation(page_number=page_num, annotation=annotation)


def overlay_pdf_with_state(
    input_pdf,
    output_pdf,
    fields,
    state,
    burn_signatures=False
):
    for f in fields:

        if f["type"] == "signature":

            print(
                "SIGNATURE FIELD:",
                f["name"],
                "=",
                state.get(f["name"])
            )

    reader = PdfReader(input_pdf)

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    # Mark the export with the pristine source ID.  When this PDF is reopened,
    # the app renders/exports from the cached clean source instead of stacking
    # another flattened appearance on top of this file.
    if True:
        try:
            metadata = {}
            if reader.metadata:
                for k, v in reader.metadata.items():
                    if isinstance(k, str) and isinstance(v, str):
                        metadata[k] = v
            metadata["/PADIManagerExport"] = "1"
            metadata["/PADIManagerBaseID"] = str(current_base_id)

            # Make signature ownership self-contained in the PDF.  This is the
            # authoritative source when the file is reopened; it prevents the
            # instructor dropdown/global state from substituting another signature.
            signature_payload = build_embedded_signature_payload(state)
            if signature_payload:
                metadata["/PADIManagerSignatureData"] = signature_payload
            else:
                metadata.pop("/PADIManagerSignatureData", None)

            metadata[PDF_COMMENT_KEY] = (
                comment_text.get("1.0", "end-1c").strip()
                if "comment_text" in globals() else get_saved_comment(input_pdf)
            )
            writer.add_metadata(metadata)
        except Exception as e:
            print("PDF METADATA WARNING:", e)

    # Keep the AcroForm interactive. Standard PDF editors need the widget
    # annotations to remain visible/editable and may regenerate their visual
    # appearances after a field value changes.
    if "/AcroForm" in writer._root_object:
        acro = writer._root_object["/AcroForm"]
        acro.update({
            NameObject("/NeedAppearances"):
            BooleanObject(True)
        })

    print("\n==============================")
    print("SIGNATURES BEFORE EXPORT")
    print("==============================")

    for f in fields:

        if f["type"] == "signature":

            print(
                f["name"],
                "=",
                repr(state.get(f["name"]))
            )

    print("==============================\n")
    
    pdf_values = {}

    for f in fields:

        value = state.get(f["name"])

        if value in (None, ""):
            continue

        #
        # Signature PNGs are handled later
        #
        if f["type"] == "signature":
            continue

        pdf_name = pdf_field_mapping.get(f["name"])

        if pdf_name:
            if f["type"] == "checkbox":

                if value:
                    pdf_values[pdf_name] = "/Yes"
                else:
                    pdf_values[pdf_name] = "/Off"

            else:

                pdf_values[pdf_name] = str(value)

    print("PDF VALUES =", pdf_values)
    print("\n===== EXPORT VALUES =====")

    for k, v in pdf_values.items():
        print(k, "=", repr(v))

    print("=========================\n")
    # Write the values into the real AcroForm fields and regenerate their
    # appearances.  The fields stay editable in Acrobat, Foxit, Preview,
    # PDF-XChange and other standard form-aware PDF editors.
    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            pdf_values,
            auto_regenerate=True
        )

    #
    # OPTIONAL SIGNATURE BURN-IN
    #
    # By default signatures are NOT merged into the saved PDF. This keeps the
    # exported form free of permanently burned signature artwork. The GUI
    # option "Burn signatures into PDF" enables the old behaviour when a
    # finalized/static copy is required.
    if burn_signatures:
        print("SIGNATURE BURN-IN = ON")

        for page_num, page in enumerate(writer.pages):

            packet = io.BytesIO()

            pdf_page = reader.pages[page_num]

            page_w = float(pdf_page.mediabox.width)
            page_h = float(pdf_page.mediabox.height)

            c = canvas.Canvas(
                packet,
                pagesize=(page_w, page_h)
            )

            # Do NOT draw ordinary text/check-box values into the page content.
            # They remain true AcroForm fields so external PDF editors can
            # change them. Only signature PNGs are optionally stamped here.

            signatures_drawn = 0

            for f in fields:

                if f.get("page", 0) != page_num:
                    continue

                if f["type"] != "signature":
                    continue

                sig_path = state.get(f["name"])

                if not sig_path:
                    continue

                resolved_sig = resolve_signature_path(sig_path)
                if not resolved_sig or not resolved_sig.exists():
                    continue

                print(
                    "STAMPING:",
                    f["name"],
                    "=",
                    resolved_sig
                )

                img_w, img_h = pages[page_num].size

                scale_x = page_w / img_w
                scale_y = page_h / img_h

                x = f["x1"] * scale_x

                y = page_h - (
                    f["y2"] * scale_y
                )

                width = (
                    f["x2"] - f["x1"]
                ) * scale_x

                height = (
                    f["y2"] - f["y1"]
                ) * scale_y

                c.drawImage(
                    ImageReader(resolved_sig),
                    x,
                    y,
                    width=width,
                    height=height,
                    mask="auto"
                )
                signatures_drawn += 1

            c.save()

            # Only merge an overlay if this page actually had a signature.
            if signatures_drawn:
                packet.seek(0)
                overlay_reader = PdfReader(packet)
                page.merge_page(overlay_reader.pages[0])

        # Leave all widget annotations visible and interactive. Hiding them
        # (annotation flag /F = 2) makes the saved PDF look flattened and
        # prevents normal click-to-edit behaviour in standard PDF editors.
    else:
        print("SIGNATURE BURN-IN = OFF (default): adding removable signature stamp annotations")

        # Keep signatures visible in ordinary PDF viewers without flattening
        # them into the page. Each signature is a /Stamp annotation with a
        # custom image appearance. Annotation-aware editors can select/delete
        # it, while the original page content remains untouched.
        for page_num, page in enumerate(writer.pages):
            pdf_page = reader.pages[page_num]
            page_w = float(pdf_page.mediabox.width)
            page_h = float(pdf_page.mediabox.height)

            for f in fields:
                if f.get("page", 0) != page_num or f["type"] != "signature":
                    continue

                sig_path = state.get(f["name"])
                if not sig_path:
                    continue

                resolved_sig = resolve_signature_path(sig_path)
                if not resolved_sig or not resolved_sig.exists():
                    print("SIGNATURE FILE NOT FOUND:", f["name"], "=", resolved_sig)
                    continue

                img_w, img_h = pages[page_num].size
                scale_x = page_w / img_w
                scale_y = page_h / img_h

                x = f["x1"] * scale_x
                y = page_h - (f["y2"] * scale_y)
                width = (f["x2"] - f["x1"]) * scale_x
                height = (f["y2"] - f["y1"]) * scale_y

                print("ADDING REMOVABLE SIGNATURE STAMP:", f["name"], "=", resolved_sig)
                _add_signature_stamp_annotation(
                    writer,
                    page_num,
                    resolved_sig,
                    x,
                    y,
                    width,
                    height,
                    f["name"]
                )

    output_pdf = Path(output_pdf).expanduser().resolve()
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file in the destination directory first. This
    # prevents a partially written PDF from replacing a good existing file.
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{output_pdf.stem}_",
        suffix=".pdf.tmp",
        dir=str(output_pdf.parent)
    )
    try:
        with os.fdopen(fd, "wb") as fp:
            writer.write(fp)
            fp.flush()
            os.fsync(fp.fileno())
        Path(temp_name).replace(output_pdf)
    except Exception:
        try:
            Path(temp_name).unlink(missing_ok=True)
        except Exception:
            pass
        raise

    print("INPUT PDF =", input_pdf)
    print("OUTPUT PDF =", output_pdf)


#def save_progress():
 #   save_state_with_locations()
  #  messagebox.showinfo("Saved", "Progress saved.")

# Track PDF edits separately from the application's automatic JSON persistence.
_main_pdf_saved_snapshot = None
_specialty_close_checks = {}

def _main_pdf_snapshot():
    if not globals().get("pdf_path"):
        return None
    # The calendar selection alone is not an unsaved PDF edit.
    values = {k: v for k, v in state.items() if k != "global_selected_date"}
    return json.dumps(values, sort_keys=True, default=str, ensure_ascii=False)

def _main_pdf_is_dirty():
    """Detect saved-state differences AND text still being typed in an editor."""
    if not globals().get("pdf_path"):
        return False

    if (_main_pdf_saved_snapshot is not None
            and _main_pdf_snapshot() != _main_pdf_saved_snapshot):
        return True

    # A PDF text edit is normally committed on Return. Clicking the window X
    # before Return must not silently discard the uncommitted typed value.
    entry = globals().get("current_inline_entry")
    if entry is not None:
        try:
            if entry.winfo_exists():
                field_name = globals().get("_active_inline_field_name")
                if field_name is not None and entry.get() != str(state.get(field_name, "") or ""):
                    return True
        except (tk.TclError, AttributeError):
            pass
    return False

def export_pdf():
    """Export an editable AcroForm PDF; signature burn-in is optional."""

    if not pdf_path:
        messagebox.showerror("Error", "No PDF loaded.")
        return

    # Preserve the input PDF filename in the Save As dialog.
    default_filename = Path(pdf_path).name

    output = filedialog.asksaveasfilename(
        title="Export PDF",
        initialfile=default_filename,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not output:
        return

    try:
        # Rebuild against the PDF currently being exported so mappings cannot
        # become stale after opening more than one PDF in a session.
        build_pdf_field_mapping()

        export_base = str(current_base_pdf_path or pdf_path)
        print("EXPORT BASE PDF =", export_base)
        overlay_pdf_with_state(
            export_base,
            output,
            fields,
            state,
            burn_signatures=bool(burn_signature_var.get())
        )

        global _main_pdf_saved_snapshot
        _main_pdf_saved_snapshot = _main_pdf_snapshot()

        messagebox.showinfo(
            "Exported",
            f"PDF exported:\n{Path(output).resolve()}"
        )

    except Exception as e:
        print("PDF EXPORT ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Export Error",
            str(e)
        )



# ============================================================
# PADI SPECIALTY TRAINING DOCUMENTATION WORKSHEET
# Added in V24
# ============================================================
# The original PADI Specialty Training Documentation Worksheet is a
# non-AcroForm PDF.  PADI Manager therefore maintains its own data layer,
# writes the values into the appropriate printed lines, and stores a compact
# copy of the data in PDF metadata so a saved worksheet can be reopened and
# edited later.

import zlib

SPECIALTY_WORKSHEET_FILENAME = "PADI Specialty Training Documentation Worksheet.pdf"
SPECIALTY_METADATA_KEY = "/PADISpecialtyStateV1"

SPECIALTY_DEFINITIONS = {
    "Altitude": {
        "page": 0, "academic_y": 250.3, "academic_sig_y": 268.3,
        "dive_y": [302.3, 338.3], "dive_sig_y": [320.3, 356.3]
    },
    "Boat Diver": {
        "page": 0, "academic_y": 406.3, "academic_sig_y": 424.3,
        "dive_y": [458.3, 494.3], "dive_sig_y": [476.3, 512.3]
    },
    "Cavern Diver": {
        "page": 0, "academic_y": 562.3, "academic_sig_y": 580.3,
        "dive_y": [614.3, 650.3, 686.3, 722.3],
        "dive_sig_y": [632.3, 668.3, 704.3, 740.3]
    },
    "Deep Diver": {
        "page": 1, "academic_y": 44.8, "academic_sig_y": 62.8,
        "dive_y": [96.8, 132.8, 168.8, 204.8],
        "dive_sig_y": [114.8, 150.8, 186.8, 222.8]
    },
    "Drift Diver": {
        "page": 1, "academic_y": 276.8, "academic_sig_y": 294.8,
        "dive_y": [328.8, 364.8], "dive_sig_y": [346.8, 382.8]
    },
    "Dry Suit Diver": {
        "page": 1, "academic_y": 437.3, "academic_sig_y": 455.3,
        "dive_y": [489.3, 525.3], "dive_sig_y": [507.3, 543.3]
    },
    "Ice Diver": {
        "page": 1, "academic_y": 597.3, "academic_sig_y": 615.3,
        "dive_y": [649.3, 685.3, 721.3],
        "dive_sig_y": [667.3, 703.3, 739.3]
    },
    "Multilevel Diver": {
        "page": 2, "academic_y": 44.8, "academic_sig_y": 62.8,
        "dive_y": [96.8, 132.8], "dive_sig_y": [114.8, 150.8]
    },
    "Night Diver": {
        "page": 2, "academic_y": 204.8, "academic_sig_y": 222.8,
        "dive_y": [256.8, 292.8, 328.8],
        "dive_sig_y": [274.8, 310.8, 346.8]
    },
    "Peak Performance Buoyancy": {
        "page": 2, "academic_y": 401.3, "academic_sig_y": 419.3,
        "dive_y": [453.3, 489.3], "dive_sig_y": [471.3, 507.3]
    },
    "Search and Recovery": {
        "page": 2, "academic_y": 561.3, "academic_sig_y": 579.3,
        "dive_y": [613.3, 649.3, 685.3, 721.3],
        "dive_sig_y": [631.3, 667.3, 703.3, 739.3]
    },
    "Underwater Naturalist": {
        "page": 3, "academic_y": 42.8, "academic_sig_y": 59.8,
        "dive_y": [111.3, 146.8], "dive_sig_y": [129.3, 163.8]
    },
    "Underwater Navigator": {
        "page": 3, "academic_y": 212.8, "academic_sig_y": 229.8,
        "dive_y": [264.3, 299.8, 334.3],
        "dive_sig_y": [282.3, 316.8, 352.3]
    },
    "Underwater Photographer": {
        "page": 3, "academic_y": 399.8, "academic_sig_y": 416.8,
        "dive_y": [451.3, 486.8], "dive_sig_y": [469.3, 503.8]
    },
    "Wreck Diver": {
        "page": 3, "academic_y": 552.8, "academic_sig_y": 569.8,
        "dive_y": [604.3, 639.8, 674.3, 709.8],
        "dive_sig_y": [622.3, 656.8, 692.3, 726.8]
    },
}

SPECIALTY_NAMES = list(SPECIALTY_DEFINITIONS.keys())
specialty_worksheet_path = None
specialty_state = {"student": {}, "specialties": {}, "student_signature_png": ""}


def _new_specialty_record(name):
    count = len(SPECIALTY_DEFINITIONS[name]["dive_y"])
    return {
        "academic_date": "",
        "academic_instructor": "",
        "academic_padi": "",
        "academic_signed": False,
        "academic_signature_date": "",
        "academic_removed": False,
        "student_signature_png": "",
        "dives": [
            {
                "date": "",
                "instructor": "",
                "padi": "",
                "signed": False,
                "signature_date": "",
                "removed": False,
            }
            for _ in range(count)
        ],
    }


def _ensure_specialty_record(name):
    global specialty_state
    specs = specialty_state.setdefault("specialties", {})
    record = specs.get(name)
    if not isinstance(record, dict):
        record = _new_specialty_record(name)
        specs[name] = record

    record.setdefault("student_signature_png", "")
    record.setdefault("academic_removed", False)

    expected = len(SPECIALTY_DEFINITIONS[name]["dive_y"])
    dives = record.setdefault("dives", [])
    while len(dives) < expected:
        dives.append({
            "date": "", "instructor": "", "padi": "",
            "signed": False, "signature_date": "", "removed": False
        })
    if len(dives) > expected:
        del dives[expected:]
    return record


def _specialty_default_student():
    """Return a completely blank student record for a blank specialty template."""
    return {
        "name": "",
        "address": "",
        "city": "",
        "province": "",
        "country": "",
        "postal": "",
        "phone": "",
        "fax": "",
        "birth_date": "",
        "sex": "",
    }


def _legacy_specialty_default_student_unused():
    """Legacy OW-form prefill retained only for source-history reference."""
    result = {}
    if isinstance(globals().get("state"), dict):
        ow = globals()["state"]
        result["name"] = str(ow.get("Student Name", "") or "")
        result["address"] = str(ow.get("Mailing address 1", "") or "")
        result["city"] = str(ow.get("Mailing address 2", "") or "")
        result["province"] = str(ow.get("Mailing address 3", "") or "")
        result["country"] = str(ow.get("Mailing address 4", "") or "")
        result["postal"] = str(ow.get("Mailing address 5", "") or "")

        birth_parts = [
            str(ow.get("Birth Date", "") or "").strip(),
            str(ow.get("undefined", "") or "").strip(),
            str(ow.get("undefined_2", "") or "").strip(),
        ]
        birth_parts = [p for p in birth_parts if p]
        if birth_parts:
            result["birth_date"] = " / ".join(birth_parts)
    return result


def _encode_specialty_metadata(data):
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    packed = zlib.compress(raw, 9)
    return base64.b64encode(packed).decode("ascii")


def _decode_specialty_metadata(value):
    if not value:
        return None
    try:
        packed = base64.b64decode(str(value))
        raw = zlib.decompress(packed).decode("utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except Exception as e:
        print("SPECIALTY METADATA READ WARNING:", e)
        return None


def _read_specialty_state_from_pdf(path):
    try:
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        return _decode_specialty_metadata(metadata.get(SPECIALTY_METADATA_KEY))
    except Exception as e:
        print("SPECIALTY PDF STATE READ ERROR:", e)
        return None


def _locate_specialty_worksheet():
    """Find the worksheet beside the app or in user data; otherwise ask once."""
    global specialty_worksheet_path

    if specialty_worksheet_path and Path(specialty_worksheet_path).exists():
        return Path(specialty_worksheet_path)

    candidates = [
        RESOURCE_DIR / SPECIALTY_WORKSHEET_FILENAME,
        DATA_DIR / SPECIALTY_WORKSHEET_FILENAME,
        Path.cwd() / SPECIALTY_WORKSHEET_FILENAME,
    ]

    for candidate in candidates:
        if candidate.exists():
            specialty_worksheet_path = str(candidate)
            return candidate

    chosen = filedialog.askopenfilename(
        title="Locate PADI Specialty Training Documentation Worksheet",
        filetypes=[("PDF files", "*.pdf")],
    )
    if not chosen:
        return None

    chosen = Path(chosen)
    cached = DATA_DIR / SPECIALTY_WORKSHEET_FILENAME
    try:
        if chosen.resolve() != cached.resolve():
            shutil.copy2(chosen, cached)
        specialty_worksheet_path = str(cached if cached.exists() else chosen)
    except Exception:
        specialty_worksheet_path = str(chosen)

    return Path(specialty_worksheet_path)


def _draw_specialty_text(c, page_h, x, top_y, width, text, size=10.5, bold=False):
    """Draw specialty values slightly smaller; regular unless explicitly bold."""
    text = str(text or "").strip()
    if not text:
        return

    font_name = "Helvetica-Bold" if bold else "Helvetica"
    font_size = 10.5
    min_font_size = 7.5

    while font_size > min_font_size and c.stringWidth(text, font_name, font_size) > width:
        font_size -= 0.5

    # Slightly taller clearing area for the larger font.
    y = page_h - (float(top_y) + 11.5)
    c.setFillColorRGB(1, 1, 1)
    c.rect(x - 1, y - 2, width + 2, 14, fill=1, stroke=0)

    c.setFillColorRGB(0, 0, 0)
    c.setFont(font_name, font_size)
    c.drawString(x, y, text)


def _specialty_signature_reader(encoded=None):
    if encoded is None:
        encoded = specialty_state.get("student_signature_png", "")
    if not encoded:
        return None
    try:
        return ImageReader(io.BytesIO(base64.b64decode(encoded)))
    except Exception as e:
        print("SPECIALTY SIGNATURE DECODE WARNING:", e)
        return None


def _draw_specialty_signature(c, page_h, top_y, image_reader):
    """Draw the stored student signature clearly on a specialty signature line."""
    if image_reader is None:
        return

    # The worksheet signature underline runs across most of the row.
    # Use a taller box than V24.3 and preserve the cropped signature's aspect
    # ratio so the handwriting is not squashed into an almost invisible strip.
    x = 102
    box_width = 375
    box_height = 16
    y = page_h - (float(top_y) + 14.5)

    # Do not paint a white rectangle over the worksheet.  The stored PNG is
    # transparent, so the original underline remains visible behind it.
    c.drawImage(
        image_reader,
        x,
        y,
        width=box_width,
        height=box_height,
        preserveAspectRatio=True,
        anchor="sw",
        mask="auto"
    )


def _draw_specialty_student_header(c, page_h, student):
    # Page 1 student information area.
    _draw_specialty_text(c, page_h, 89, 59.8, 484, student.get("name", ""), 10.5, bold=True)
    _draw_specialty_text(c, page_h, 69, 76.8, 505, student.get("address", ""), 8)
    _draw_specialty_text(c, page_h, 52, 93.8, 141, student.get("city", ""), 7)
    _draw_specialty_text(c, page_h, 251, 93.8, 74, student.get("province", ""), 7)
    _draw_specialty_text(c, page_h, 359, 93.8, 92, student.get("country", ""), 7)
    _draw_specialty_text(c, page_h, 514, 93.8, 61, student.get("postal", ""), 7)
    _draw_specialty_text(c, page_h, 62, 110.8, 236, student.get("phone", ""), 7)
    _draw_specialty_text(c, page_h, 320, 110.8, 254, student.get("fax", ""), 7)
    _draw_specialty_text(c, page_h, 83, 128.3, 88, student.get("birth_date", ""), 7)

    sex = str(student.get("sex", "")).upper().strip()
    if sex in ("M", "F"):
        c.setFont("Helvetica-Bold", 11)
        c.setFillColorRGB(0, 0, 0)
        if sex == "M":
            c.drawString(211, page_h - 137.2, "X")
        else:
            c.drawString(246, page_h - 137.2, "X")


def _normalize_specialty_signature_flags(record):
    """Set signature flags strictly from required field presence."""
    if not isinstance(record, dict):
        return

    record["academic_signed"] = bool(
        not bool(record.get("academic_removed", False))
        and str(record.get("academic_date", "") or "").strip()
        and str(record.get("academic_instructor", "") or "").strip()
        and str(record.get("academic_signature_date", "") or "").strip()
    )

    for dive in record.get("dives", []):
        if not isinstance(dive, dict):
            continue
        dive["signed"] = bool(
            str(dive.get("date", "") or "").strip()
            and str(dive.get("instructor", "") or "").strip()
        )
        if dive["signed"] and not str(dive.get("signature_date", "") or "").strip():
            dive["signature_date"] = (
                str(record.get("academic_signature_date", "") or "").strip()
                or date.today().strftime("%Y-%m-%d")
            )


def _draw_specialty_record(c, page_h, name, record, signature_image):
    _normalize_specialty_signature_flags(record)
    definition = SPECIALTY_DEFINITIONS[name]

    ay = definition["academic_y"]
    asy = definition["academic_sig_y"]
    if not bool(record.get("academic_removed", False)):
        _draw_specialty_text(c, page_h, 98, ay, 59, record.get("academic_date", ""), 7)
        _draw_specialty_text(c, page_h, 222, ay, 264, record.get("academic_instructor", ""), 7)
        _draw_specialty_text(c, page_h, 505, ay, 69, record.get("academic_padi", ""), 7)

        if record.get("academic_signed"):
            _draw_specialty_signature(c, page_h, asy, signature_image)
            _draw_specialty_text(
                c, page_h, 505, asy, 69,
                record.get("academic_signature_date", ""), 7
            )

    for i, dy in enumerate(definition["dive_y"]):
        if i >= len(record.get("dives", [])):
            break
        dive = record["dives"][i]
        _draw_specialty_text(c, page_h, 92, dy, 66, dive.get("date", ""), 7)
        _draw_specialty_text(c, page_h, 222, dy, 265, dive.get("instructor", ""), 7)
        _draw_specialty_text(c, page_h, 505, dy, 69, dive.get("padi", ""), 7)

        sy = definition["dive_sig_y"][i]
        if (
            dive.get("signed")
            and str(dive.get("instructor", "") or "").strip()
        ):
            _draw_specialty_signature(c, page_h, sy, signature_image)
            _draw_specialty_text(c, page_h, 505, sy, 69, dive.get("signature_date", ""), 7)



def _specialty_pdf_literal(value):
    """Encode simple field appearance text for the built-in Helvetica font."""
    value = str(value or "")
    raw = value.encode("cp1252", errors="replace").decode("latin-1")
    return (
        raw.replace("\\", "\\\\")
           .replace("(", "\\(")
           .replace(")", "\\)")
           .replace("\r", " ")
           .replace("\n", " ")
    )


def _ensure_specialty_acroform(writer):
    """Create a fresh AcroForm and built-in Helvetica resources."""
    font_regular = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
        NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
    })
    font_bold = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica-Bold"),
        NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
    })
    helv_ref = writer._add_object(font_regular)
    helvb_ref = writer._add_object(font_bold)

    fields = ArrayObject()
    font_dict = DictionaryObject({
        NameObject("/Helv"): helv_ref,
        NameObject("/HelvB"): helvb_ref,
    })
    dr = DictionaryObject({
        NameObject("/Font"): font_dict,
    })
    acro = DictionaryObject({
        NameObject("/Fields"): fields,
        NameObject("/NeedAppearances"): BooleanObject(True),
        NameObject("/DR"): dr,
        NameObject("/DA"): TextStringObject("/Helv 9 Tf 0 g"),
    })
    acro_ref = writer._add_object(acro)
    writer._root_object[NameObject("/AcroForm")] = acro_ref
    return fields, helv_ref, helvb_ref


def _specialty_text_field_rect(page_h, x, top_y, width, height=16):
    """Return a PDF rectangle matching the existing specialty overlay placement."""
    baseline = float(page_h) - (float(top_y) + 11.5)
    bottom = baseline - 3.0
    return (
        float(x) - 1.0,
        bottom,
        float(x) + float(width) + 1.0,
        bottom + float(height),
    )


def _add_specialty_editable_text_field(
    writer,
    page,
    acro_fields,
    helv_ref,
    helvb_ref,
    field_name,
    value,
    page_h,
    x,
    top_y,
    width,
    font_size=9.0,
    bold=False,
    height=16,
):
    """Add a borderless editable AcroForm text field with an initial appearance."""
    value = str(value or "")
    x1, y1, x2, y2 = _specialty_text_field_rect(
        page_h, x, top_y, width, height=height
    )
    field_w = max(1.0, x2 - x1)
    field_h = max(1.0, y2 - y1)
    font_key = "/HelvB" if bold else "/Helv"
    font_ref = helvb_ref if bold else helv_ref

    # Initial appearance keeps values visible in viewers that do not immediately
    # regenerate AcroForm appearances.
    appearance = DecodedStreamObject()
    literal = _specialty_pdf_literal(value)
    baseline = max(2.0, (field_h - float(font_size)) / 2.0 + 1.5)
    appearance.set_data(
        (
            "q\n"
            f"1 1 1 rg 0 0 {field_w:.3f} {field_h:.3f} re f\n"
            "BT\n"
            f"{font_key} {float(font_size):.2f} Tf\n"
            "0 g\n"
            f"2 {baseline:.3f} Td\n"
            f"({literal}) Tj\n"
            "ET\n"
            "Q\n"
        ).encode("latin-1", errors="replace")
    )
    appearance[NameObject("/Type")] = NameObject("/XObject")
    appearance[NameObject("/Subtype")] = NameObject("/Form")
    appearance[NameObject("/FormType")] = NumberObject(1)
    appearance[NameObject("/BBox")] = ArrayObject([
        FloatObject(0), FloatObject(0),
        FloatObject(field_w), FloatObject(field_h),
    ])
    appearance[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({
            NameObject(font_key): font_ref,
        })
    })
    appearance_ref = writer._add_object(appearance)

    field = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Widget"),
        NameObject("/FT"): NameObject("/Tx"),
        NameObject("/T"): TextStringObject(str(field_name)),
        NameObject("/V"): TextStringObject(value),
        NameObject("/DV"): TextStringObject(value),
        NameObject("/Rect"): ArrayObject([
            FloatObject(x1), FloatObject(y1),
            FloatObject(x2), FloatObject(y2),
        ]),
        NameObject("/F"): NumberObject(4),
        NameObject("/Ff"): NumberObject(0),
        NameObject("/DA"): TextStringObject(
            f"{font_key} {float(font_size):.2f} Tf 0 g"
        ),
        NameObject("/MK"): DictionaryObject({
            NameObject("/BG"): ArrayObject([
                FloatObject(1), FloatObject(1), FloatObject(1)
            ]),
        }),
        NameObject("/BS"): DictionaryObject({
            NameObject("/W"): NumberObject(0),
        }),
        NameObject("/AP"): DictionaryObject({
            NameObject("/N"): appearance_ref,
        }),
    })
    field_ref = writer._add_object(field)

    annots = page.get("/Annots")
    if annots is None:
        annots_array = ArrayObject()
        page[NameObject("/Annots")] = annots_array
    else:
        annots_array = annots.get_object() if hasattr(annots, "get_object") else annots
    annots_array.append(field_ref)
    acro_fields.append(field_ref)


def _add_specialty_student_editable_fields(
    writer, page, acro_fields, helv_ref, helvb_ref, page_h, student
):
    """Add editable student-information widgets on page 1."""
    specs = [
        ("student.name", "name", 89, 59.8, 484, 10.5, True),
        ("student.address", "address", 69, 76.8, 505, 8.5, False),
        ("student.city", "city", 52, 93.8, 141, 8.0, False),
        ("student.province", "province", 251, 93.8, 74, 8.0, False),
        ("student.country", "country", 359, 93.8, 92, 8.0, False),
        ("student.postal", "postal", 514, 93.8, 61, 8.0, False),
        ("student.phone", "phone", 62, 110.8, 236, 8.0, False),
        ("student.fax", "fax", 320, 110.8, 254, 8.0, False),
        ("student.birth_date", "birth_date", 83, 128.3, 88, 8.0, False),
    ]
    for fname, key, x, top_y, width, size, bold in specs:
        _add_specialty_editable_text_field(
            writer, page, acro_fields, helv_ref, helvb_ref,
            fname, student.get(key, ""), page_h,
            x, top_y, width, font_size=size, bold=bold
        )

    # Sex remains editable as two tiny text widgets containing X/blank.
    sex = str(student.get("sex", "") or "").upper().strip()
    _add_specialty_editable_text_field(
        writer, page, acro_fields, helv_ref, helvb_ref,
        "student.sex_m", "X" if sex == "M" else "",
        page_h, 207, 128.0, 12, font_size=9, bold=True, height=14
    )
    _add_specialty_editable_text_field(
        writer, page, acro_fields, helv_ref, helvb_ref,
        "student.sex_f", "X" if sex == "F" else "",
        page_h, 242, 128.0, 12, font_size=9, bold=True, height=14
    )


def _specialty_field_slug(name):
    return re.sub(r"[^A-Za-z0-9]+", "_", str(name)).strip("_").lower()


def _add_specialty_record_editable_fields(
    writer, page, acro_fields, helv_ref, helvb_ref, page_h, name, record
):
    """Add editable Academics and Dive widgets for one specialty."""
    definition = SPECIALTY_DEFINITIONS[name]
    slug = _specialty_field_slug(name)

    ay = definition["academic_y"]
    _add_specialty_editable_text_field(
        writer, page, acro_fields, helv_ref, helvb_ref,
        f"{slug}.academics.date_completed",
        record.get("academic_date", ""),
        page_h, 98, ay, 59, font_size=8
    )
    _add_specialty_editable_text_field(
        writer, page, acro_fields, helv_ref, helvb_ref,
        f"{slug}.academics.instructor",
        record.get("academic_instructor", ""),
        page_h, 222, ay, 264, font_size=8
    )
    _add_specialty_editable_text_field(
        writer, page, acro_fields, helv_ref, helvb_ref,
        f"{slug}.academics.padi",
        record.get("academic_padi", ""),
        page_h, 505, ay, 69, font_size=8
    )

    asy = definition["academic_sig_y"]
    _add_specialty_editable_text_field(
        writer, page, acro_fields, helv_ref, helvb_ref,
        f"{slug}.academics.signed_date_student",
        record.get("academic_signature_date", ""),
        page_h, 505, asy, 69, font_size=8
    )

    dives = record.get("dives", [])
    for i, dy in enumerate(definition.get("dive_y", [])):
        if i >= len(dives):
            break
        dive = dives[i]
        if not isinstance(dive, dict) or bool(dive.get("removed", False)):
            continue

        prefix = f"{slug}.dive{i + 1}"
        _add_specialty_editable_text_field(
            writer, page, acro_fields, helv_ref, helvb_ref,
            f"{prefix}.date",
            dive.get("date", ""),
            page_h, 92, dy, 66, font_size=8
        )
        _add_specialty_editable_text_field(
            writer, page, acro_fields, helv_ref, helvb_ref,
            f"{prefix}.instructor",
            dive.get("instructor", ""),
            page_h, 222, dy, 265, font_size=8
        )
        _add_specialty_editable_text_field(
            writer, page, acro_fields, helv_ref, helvb_ref,
            f"{prefix}.padi",
            dive.get("padi", ""),
            page_h, 505, dy, 69, font_size=8
        )
        _add_specialty_editable_text_field(
            writer, page, acro_fields, helv_ref, helvb_ref,
            f"{prefix}.signed_date_student",
            dive.get("signature_date", "") if dive.get("signed") else "",
            page_h, 505, definition["dive_sig_y"][i], 69, font_size=8
        )


def _draw_specialty_signatures_only(c, page_h, name, record, signature_image):
    """Flatten only handwritten student signatures; all text stays editable."""
    _normalize_specialty_signature_flags(record)
    definition = SPECIALTY_DEFINITIONS[name]

    asy = definition["academic_sig_y"]
    if (
        not bool(record.get("academic_removed", False))
        and record.get("academic_signed")
    ):
        _draw_specialty_signature(c, page_h, asy, signature_image)

    dives = record.get("dives", [])
    for i, sy in enumerate(definition.get("dive_sig_y", [])):
        if i >= len(dives):
            break
        dive = dives[i]
        if not isinstance(dive, dict) or bool(dive.get("removed", False)):
            continue
        if (
            dive.get("signed")
            and str(dive.get("instructor", "") or "").strip()
        ):
            _draw_specialty_signature(c, page_h, sy, signature_image)


def _export_specialty_worksheet(base_pdf, output_pdf):
    """Save Specialty Worksheet with editable AcroForm text fields."""
    reader = PdfReader(str(base_pdf))
    writer = PdfWriter()

    # Start with clean visible source pages to avoid legacy/Quartz object issues.
    for source_page in reader.pages:
        writer.add_page(copy.deepcopy(source_page))

    acro_fields, helv_ref, helvb_ref = _ensure_specialty_acroform(writer)

    # First add editable text widgets to the copied pages.
    for page_index, page in enumerate(writer.pages):
        page_h = float(page.mediabox.height)

        if page_index == 0:
            student = specialty_state.get("student", {})
            if isinstance(student, dict):
                _add_specialty_student_editable_fields(
                    writer, page, acro_fields,
                    helv_ref, helvb_ref, page_h, student
                )

        for name, definition in SPECIALTY_DEFINITIONS.items():
            if int(definition["page"]) != page_index:
                continue
            record = specialty_state.get("specialties", {}).get(name)
            if isinstance(record, dict):
                _add_specialty_record_editable_fields(
                    writer, page, acro_fields,
                    helv_ref, helvb_ref, page_h, name, record
                )

    # Then flatten only handwritten signatures onto the page contents.
    for page_index in range(len(writer.pages)):
        page = writer.pages[page_index]
        page_w = float(page.mediabox.width)
        page_h = float(page.mediabox.height)
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_w, page_h))
        drew_signature = False

        for name, definition in SPECIALTY_DEFINITIONS.items():
            if int(definition["page"]) != page_index:
                continue
            record = specialty_state.get("specialties", {}).get(name)
            if not isinstance(record, dict):
                continue

            _normalize_specialty_signature_flags(record)
            has_signature = bool(record.get("academic_signed")) or any(
                isinstance(dive, dict)
                and bool(dive.get("signed"))
                and str(dive.get("instructor", "") or "").strip()
                for dive in record.get("dives", [])
            )
            if not has_signature:
                continue

            signature_image = _specialty_signature_reader(
                record.get("student_signature_png", "")
            )
            if signature_image is None:
                # Backward compatibility for older worksheets with only a
                # worksheet-level reusable signature.
                signature_image = _specialty_signature_reader()
            if signature_image is None:
                continue

            _draw_specialty_signatures_only(
                c, page_h, name, record, signature_image
            )
            drew_signature = True

        if drew_signature:
            c.save()
            packet.seek(0)
            overlay = PdfReader(packet)
            if len(overlay.pages) > 0:
                page.merge_page(overlay.pages[0])
        else:
            try:
                c.save()
            except Exception:
                pass

    # Preserve metadata and embed PADI Manager's state for reopening in this app.
    metadata = {}
    try:
        if reader.metadata:
            for k, v in reader.metadata.items():
                if isinstance(k, str) and isinstance(v, str):
                    metadata[k] = v
    except Exception:
        pass

    metadata[SPECIALTY_METADATA_KEY] = _encode_specialty_metadata(
        specialty_state
    )
    metadata["/PADISpecialtyManager"] = "1"
    metadata["/PADISpecialtyEditableFields"] = "1"
    # Preserve notes when the specialty worksheet is exported or overwritten.
    output_existing = Path(output_pdf)
    if output_existing.is_file():
        metadata[PDF_COMMENT_KEY] = get_saved_comment(output_existing)
    else:
        metadata[PDF_COMMENT_KEY] = get_saved_comment(base_pdf)
    writer.add_metadata(metadata)

    output_pdf = Path(output_pdf)
    input_pdf = Path(base_pdf)
    if output_pdf.resolve() == input_pdf.resolve():
        temp_out = output_pdf.with_suffix(".padi_specialty_tmp.pdf")
        with open(temp_out, "wb") as f:
            writer.write(f)
        temp_out.replace(output_pdf)
    else:
        with open(output_pdf, "wb") as f:
            writer.write(f)




def _specialty_draw_student_signature(parent, on_saved=None):
    """Capture the student signature in memory only.

    The signature is stored as Base64 PNG inside specialty_state and is embedded
    into the saved Specialty PDF metadata/appearance.  No standalone signature
    image file is created in SIGNATURE_DIR or elsewhere on disk.
    """
    win = tk.Toplevel(parent)
    win.title("Specialty Worksheet - Student Signature")
    win.geometry("620x300")
    win.transient(parent)

    width, height = 600, 120
    cv = tk.Canvas(win, bg="white", width=width, height=height, relief="sunken", bd=1)
    cv.pack(padx=10, pady=10)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    last = {"x": None, "y": None}

    def down(event):
        last["x"], last["y"] = event.x, event.y

    def move(event):
        if last["x"] is not None:
            cv.create_line(last["x"], last["y"], event.x, event.y, fill="black", width=3)
            draw.line((last["x"], last["y"], event.x, event.y), fill="black", width=3)
        last["x"], last["y"] = event.x, event.y

    def clear():
        cv.delete("all")
        draw.rectangle((0, 0, width, height), fill="white")

    def save():
        # Crop to the actual handwriting so the signature does not become tiny
        # when fitted onto the worksheet's signature line.
        gray = ImageOps.grayscale(img)
        inverted = ImageOps.invert(gray)
        bbox = inverted.getbbox()

        if bbox is None:
            messagebox.showerror(
                "Student Signature",
                "No signature was drawn.",
                parent=win
            )
            return

        left, top, right, bottom = bbox
        pad = 8
        left = max(0, left - pad)
        top = max(0, top - pad)
        right = min(width, right + pad)
        bottom = min(height, bottom + pad)

        cropped = img.crop((left, top, right, bottom)).convert("RGBA")

        # Make the white canvas transparent while preserving dark handwriting.
        pixels = cropped.load()
        for yy in range(cropped.height):
            for xx in range(cropped.width):
                r, g, b, a = pixels[xx, yy]
                luminance = (r + g + b) / 3.0
                if luminance >= 245:
                    pixels[xx, yy] = (255, 255, 255, 0)
                else:
                    # Strengthen anti-aliased handwriting slightly for PDF output.
                    alpha = max(80, 255 - int(luminance))
                    pixels[xx, yy] = (0, 0, 0, alpha)

        bio = io.BytesIO()
        cropped.save(bio, format="PNG")
        specialty_state["student_signature_png"] = base64.b64encode(
            bio.getvalue()
        ).decode("ascii")

        # Remember the date on which this student signature was drawn/saved.
        # This becomes the default Signed Date (Student) for Academics.
        specialty_state["student_signature_date"] = date.today().strftime("%Y-%m-%d")

        if on_saved:
            on_saved()
        win.destroy()

    cv.bind("<Button-1>", down)
    cv.bind("<B1-Motion>", move)

    buttons = ttk.Frame(win)
    buttons.pack(pady=6)
    ttk.Button(buttons, text="Clear", command=clear).pack(side="left", padx=8)
    ttk.Button(buttons, text="Save Signature", command=save).pack(side="left", padx=8)
    ttk.Button(buttons, text="Cancel", command=win.destroy).pack(side="left", padx=8)



def _find_existing_specialty_signature(pdf_path):
    """Return (encoded_png, location_label) for a likely handwritten signature.

    The worksheet contains printed horizontal signature lines, so those long
    horizontal strokes are removed before deciding whether handwriting remains.
    This is intentionally conservative to avoid prompting on a clean template.
    """
    try:
        doc = pdfium.PdfDocument(str(pdf_path))
    except Exception as e:
        print("SPECIALTY SIGNATURE IMPORT OPEN WARNING:", e)
        return None, None

    best = None
    scale = 2.0

    try:
        for specialty_name, definition in SPECIALTY_DEFINITIONS.items():
            page_index = int(definition.get("page", 0))
            if page_index < 0 or page_index >= len(doc):
                continue

            try:
                page = doc[page_index]
                bitmap = page.render(scale=scale)
                rendered = bitmap.to_pil().convert("RGB")
                rendered.load()
            except Exception as e:
                print("SPECIALTY SIGNATURE IMPORT RENDER WARNING:", specialty_name, e)
                continue

            zones = [("Academics", float(definition["academic_sig_y"]))]
            zones.extend(
                (f"Dive {idx}", float(sig_y))
                for idx, sig_y in enumerate(definition.get("dive_sig_y", []), start=1)
            )

            for zone_name, top_y in zones:
                # Signature image is drawn across x ~= 102..477 and vertically
                # around the worksheet's signature row. Keep this crop narrow so
                # labels from adjacent rows are excluded.
                left = max(0, int(100 * scale))
                right = min(rendered.width, int(480 * scale))
                top = max(0, int((top_y - 4.0) * scale))
                bottom = min(rendered.height, int((top_y + 17.0) * scale))
                if right <= left or bottom <= top:
                    continue

                crop = rendered.crop((left, top, right, bottom)).convert("L")
                w, h = crop.size
                px = crop.load()

                # Binary ink mask. The threshold is deliberately dark so light
                # gray form shading does not look like handwriting.
                mask = Image.new("L", (w, h), 255)
                mp = mask.load()
                row_counts = []
                for yy in range(h):
                    count = 0
                    for xx in range(w):
                        if px[xx, yy] < 155:
                            count += 1
                    row_counts.append(count)

                # Remove printed underline rows and their immediate neighbors.
                line_rows = set()
                for yy, count in enumerate(row_counts):
                    if count >= int(w * 0.48):
                        line_rows.update((yy - 1, yy, yy + 1))

                dark_count = 0
                for yy in range(h):
                    if yy in line_rows:
                        continue
                    for xx in range(w):
                        lum = px[xx, yy]
                        if lum < 155:
                            mp[xx, yy] = 0
                            dark_count += 1

                bbox = ImageOps.invert(mask).getbbox()
                if bbox is None:
                    continue

                bw = bbox[2] - bbox[0]
                bh = bbox[3] - bbox[1]
                # Require a meaningful cluster, not a speck or remnant of a line.
                if dark_count < 45 or bw < 24 or bh < 4:
                    continue

                # Handwriting usually has multiple occupied rows and a moderate
                # width. Printed remnants tend to be either tiny or nearly full-width.
                if bw > int(w * 0.97) and bh <= 5:
                    continue

                score = dark_count + (bw * bh * 0.08)
                if best is None or score > best[0]:
                    # Crop around detected ink and convert white to transparency.
                    pad = 6
                    x1 = max(0, bbox[0] - pad)
                    y1 = max(0, bbox[1] - pad)
                    x2 = min(w, bbox[2] + pad)
                    y2 = min(h, bbox[3] + pad)
                    source = rendered.crop(
                        (left + x1, top + y1, left + x2, top + y2)
                    ).convert("RGBA")
                    source_mask = mask.crop((x1, y1, x2, y2))

                    rgba = Image.new("RGBA", source.size, (255, 255, 255, 0))
                    rp = rgba.load()
                    sp = source.load()
                    sm = source_mask.load()
                    for sy in range(source.height):
                        for sx in range(source.width):
                            if sm[sx, sy] < 128:
                                r, g, b, _ = sp[sx, sy]
                                lum = (r + g + b) / 3.0
                                alpha = max(95, min(255, 255 - int(lum)))
                                rp[sx, sy] = (0, 0, 0, alpha)

                    out = io.BytesIO()
                    rgba.save(out, format="PNG")
                    encoded = base64.b64encode(out.getvalue()).decode("ascii")
                    best = (
                        score,
                        encoded,
                        f"{specialty_name} - {zone_name}"
                    )

            try:
                bitmap.close()
            except Exception:
                pass
            try:
                page.close()
            except Exception:
                pass
    finally:
        try:
            doc.close()
        except Exception:
            pass

    if best is None:
        return None, None
    return best[1], best[2]


def _offer_import_existing_specialty_signature(pdf_path, parent=None):
    """Detect and optionally import a visible signature from an existing PDF.

    Imported signature pixels remain in memory and are embedded back into the
    Specialty PDF when it is saved.  No external signature file is written.
    """
    global specialty_state

    # If PADI Manager metadata already supplied a reusable signature, there is
    # nothing to import from the flattened PDF appearance.
    if str(specialty_state.get("student_signature_png", "") or "").strip():
        return False

    encoded, location = _find_existing_specialty_signature(pdf_path)
    if not encoded:
        return False

    use_it = messagebox.askyesno(
        "Existing Student Signature Detected",
        "A possible existing student signature was detected in the worksheet:\n\n"
        f"{location}\n\n"
        "Import this signature as the reusable Student Signature?",
        parent=parent
    )
    if not use_it:
        return False

    specialty_state["student_signature_png"] = encoded
    # Do not invent a signing date for an imported signature. The user can use
    # the existing Signed Date field in the worksheet or select the correct date.
    specialty_state["student_signature_date"] = ""
    return True

def open_specialty_worksheet():
    """Open the separate Specialty Training Documentation Worksheet editor."""
    global specialty_state, specialty_worksheet_path

    # IMPORTANT: opening the Specialty editor from the main program must NOT
    # auto-locate, auto-load, or inspect any Specialty worksheet/template.
    # A Specialty PDF becomes active only after the user explicitly clicks
    # "Open Existing / Template PDF" and selects a file.
    template = None
    specialty_worksheet_path = None
    worksheet_loaded = [False]
    import_open_water_signature_command = [None]
    saved_specialty_snapshot = [None]

    def specialty_snapshot():
        save_controls_to_state(active_specialty_name[0])
        return json.dumps(specialty_state, sort_keys=True, default=str, ensure_ascii=False)

    def specialty_is_dirty():
        return (saved_specialty_snapshot[0] is not None
                and specialty_snapshot() != saved_specialty_snapshot[0])

    def close_specialty(check_only=False):
        if specialty_is_dirty() and not messagebox.askyesno(
            "Unsaved Specialty Worksheet",
            "The Specialty Worksheet has changes that have not been saved to PDF.\n\nExit without saving?",
            parent=win
        ):
            return False
        if not check_only:
            _specialty_close_checks.pop(str(win), None)
            win.destroy()
        return True


    # Always start the Specialty window with a clean working state.
    # Previously saved specialty data is loaded only when the user explicitly
    # chooses "Open Existing / Template PDF" inside this window.
    specialty_state = {
        "student": _specialty_default_student(),
        "specialties": {},
        "student_signature_png": "",
        "student_signature_date": "",
    }

    win = tk.Toplevel(root)
    win.title("PADI Specialty Training Documentation Worksheet - PDF Backdrop")
    win.protocol("WM_DELETE_WINDOW", close_specialty)
    _specialty_close_checks[str(win)] = close_specialty
    # Baseline before any specialty editing, including a not-yet-opened template.
    saved_specialty_snapshot[0] = json.dumps(
        specialty_state, sort_keys=True, default=str, ensure_ascii=False
    )

    # Size the Specialty editor to the actual display instead of forcing a
    # 1450-pixel-wide window.  On smaller Mac displays the old fixed geometry
    # could make the window appear maximized and push Worksheet Data off-screen.
    win.update_idletasks()
    screen_w = max(900, win.winfo_screenwidth())
    screen_h = max(700, win.winfo_screenheight())
    window_w = min(1280, max(1000, int(screen_w * 0.90)))
    window_h = min(820, max(680, int(screen_h * 0.86)))
    x = max(0, (screen_w - window_w) // 2)
    y = max(0, (screen_h - window_h) // 3)
    win.geometry(f"{window_w}x{window_h}+{x}+{y}")
    win.minsize(980, 650)

    # Larger/bold specialty-entry text for easier reading.
    specialty_style = ttk.Style(win)
    specialty_style.configure("SpecialtyBold.TEntry", font=("Arial", 10, "normal"))
    specialty_style.configure("SpecialtyBold.TCombobox", font=("Arial", 10, "normal"))

    # ---- Top controls ----
    top = ttk.Frame(win, padding=8)
    top.pack(fill="x")

    ttk.Label(top, text="Specialty:").pack(side="left")
    # Require an explicit specialty selection for every newly opened worksheet.
    local_specialty_var = tk.StringVar(value="")
    spec_combo = ttk.Combobox(
        top, textvariable=local_specialty_var,
        values=SPECIALTY_NAMES, state="readonly", width=28
    )
    spec_combo.pack(side="left", padx=(5, 15))

    ttk.Label(top, text="Instructor:").pack(side="left")
    local_instructor_var = tk.StringVar(value=instructor_var.get())
    inst_combo = ttk.Combobox(
        top, textvariable=local_instructor_var,
        values=[i["name"] for i in instructor_list],
        state="readonly", width=26
    )
    inst_combo.pack(side="left", padx=5)

    # Calendar picker in the top action area.
    ttk.Label(top, text="Date:").pack(side="left", padx=(22, 4))
    specialty_date_picker = StableDatePicker(
        top,
        width=12,
        date_pattern="yyyy-mm-dd",
    )
    try:
        specialty_date_picker.set_date(date_picker.get_date())
    except Exception:
        specialty_date_picker.set_date(date.today())
    specialty_date_picker.pack(side="left", padx=(0, 8))
    specialty_date_picker.bind(
        "<<DateEntrySelected>>",
        lambda e: status_label.config(
            text=f"Specialty date selected: {specialty_date_picker.get_date().strftime('%Y-%m-%d')}"
        ) if "status_label" in globals() else None
    )

    # Container for the action buttons moved from the red/orange areas.
    top_actions = ttk.Frame(top)
    top_actions.pack(side="left", padx=(4, 0))

    # ---- Split editor: actual PDF backdrop on the left, controls on the right ----
    paned = ttk.Panedwindow(win, orient="horizontal")
    paned.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    preview_frame = ttk.LabelFrame(paned, text="PDF Worksheet Backdrop", padding=4)
    editor_frame = ttk.LabelFrame(paned, text="Worksheet Data", padding=4)
    # Prefer more space for Worksheet Data. The PDF preview auto-fits to
    # whatever width remains on the left.
    paned.add(preview_frame, weight=1)
    paned.add(editor_frame, weight=3)

    def _set_initial_specialty_split():
        """Open with the PDF pane only slightly wider than the worksheet page."""
        try:
            win.update_idletasks()
            total_width = max(900, paned.winfo_width())

            # Keep the PDF pane deliberately compact so the Worksheet Data
            # controls on the right are always visible. The PDF itself scales
            # to the available preview width and remains scrollable.
            desired_preview_width = 540

            # Never allow the preview to consume more than ~43% of the editor.
            # Also reserve at least 520 px for the data-entry side.
            max_preview_width = max(420, min(int(total_width * 0.43), total_width - 520))
            desired_preview_width = min(desired_preview_width, max_preview_width)
            desired_preview_width = max(420, desired_preview_width)

            paned.sashpos(0, desired_preview_width)
        except Exception as e:
            print("SPECIALTY INITIAL SPLIT WARNING:", e)

    # Run after Tk has calculated the actual specialty-window dimensions.
    win.after(120, _set_initial_specialty_split)

    preview_toolbar = ttk.Frame(preview_frame)
    preview_toolbar.pack(fill="x", pady=(0, 4))
    preview_page_label = ttk.Label(preview_toolbar, text="Page 1 of 4")
    preview_page_label.pack(side="left", padx=4)
    ttk.Label(
        preview_toolbar,
        text="The selected specialty is outlined on the original PADI worksheet."
    ).pack(side="left", padx=12)

    preview_holder = ttk.Frame(preview_frame)
    preview_holder.pack(fill="both", expand=True)
    preview_canvas = tk.Canvas(
        preview_holder, background="#808080", highlightthickness=0
    )
    preview_vsb = ttk.Scrollbar(
        preview_holder, orient="vertical", command=preview_canvas.yview
    )
    preview_hsb = ttk.Scrollbar(
        preview_holder, orient="horizontal", command=preview_canvas.xview
    )
    preview_canvas.configure(
        yscrollcommand=preview_vsb.set,
        xscrollcommand=preview_hsb.set
    )
    preview_canvas.grid(row=0, column=0, sticky="nsew")
    preview_vsb.grid(row=0, column=1, sticky="ns")
    preview_hsb.grid(row=1, column=0, sticky="ew")
    preview_holder.rowconfigure(0, weight=1)
    preview_holder.columnconfigure(0, weight=1)

    def _specialty_mousewheel(event):
        """Scroll the complete PDF backdrop vertically with the mouse wheel."""
        if getattr(event, "delta", 0):
            # Windows/macOS
            direction = -1 if event.delta > 0 else 1
            preview_canvas.yview_scroll(direction * 3, "units")
        elif getattr(event, "num", None) == 4:
            preview_canvas.yview_scroll(-3, "units")
        elif getattr(event, "num", None) == 5:
            preview_canvas.yview_scroll(3, "units")
        return "break"

    preview_canvas.bind("<MouseWheel>", _specialty_mousewheel)
    preview_canvas.bind("<Button-4>", _specialty_mousewheel)
    preview_canvas.bind("<Button-5>", _specialty_mousewheel)

    # Keep wheel scrolling active while the pointer is anywhere over the backdrop.
    preview_canvas.bind("<Enter>", lambda e: preview_canvas.focus_set())
    preview_canvas.bind("<Prior>", lambda e: preview_canvas.yview_scroll(-1, "pages"))
    preview_canvas.bind("<Next>", lambda e: preview_canvas.yview_scroll(1, "pages"))
    preview_canvas.bind("<Home>", lambda e: preview_canvas.yview_moveto(0.0))
    preview_canvas.bind("<End>", lambda e: preview_canvas.yview_moveto(1.0))

    # Keep a Tk reference alive for the rendered PDF image.
    preview_state = {
        "photo": None,
        "scale": 1.0,
        "page": 0,
        "live_images": [],
        "after_id": None,
        "fit_after_id": None,
        "last_navigation": None,
    }

    def _preview_pdf_path():
        # There is deliberately no automatic/default Specialty template.
        # The only valid preview source is a PDF explicitly selected with
        # "Open Existing / Template PDF".
        if specialty_worksheet_path:
            candidate = Path(specialty_worksheet_path)
            if candidate.exists():
                return candidate
        return None

    def _live_preview_text(x, top_y, width, value, font_size=10, bold=False):
        """Paint a current nonblank value over the loaded PDF backdrop.

        Blank editor values deliberately do NOT cover the PDF. This preserves
        text already present in an existing specialty PDF when its metadata is
        absent, incomplete, or from an older PADI Manager version.
        """
        value = str(value or "").strip()
        if not value:
            return

        s = preview_state["scale"]
        margin = 12

        x1 = margin + (float(x) - 1.0) * s
        y1 = margin + (float(top_y) - 2.0) * s
        x2 = margin + (float(x) + float(width) + 2.0) * s
        y2 = margin + (float(top_y) + 13.5) * s

        # Only cover this field when we actually have a replacement value.
        preview_canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="white", outline="",
            tags=("live_preview",)
        )

        # Start large/bold and reduce only for long values.
        size = int(font_size)
        approx_width = max(1.0, len(value) * size * 0.58)
        available = max(1.0, float(width) * s)
        if approx_width > available:
            size = max(8, int(size * available / approx_width))

        preview_canvas.create_text(
            margin + float(x) * s,
            margin + (float(top_y) - 2.0) * s,
            text=value,
            anchor="nw",
            fill="black",
            font=("Arial", size, "bold" if bold else "normal"),
            tags=("live_preview",)
        )

    def _live_preview_signature(top_y, enabled, encoded_signature=None):
        """Overlay the signature committed to a specific specialty."""
        if not enabled:
            return

        encoded = encoded_signature or ""
        if not encoded:
            # Backward-compatible fallback for the currently selected specialty.
            # Older records may predate per-specialty signature snapshots.
            encoded = str(
                specialty_state.get("student_signature_png", "") or ""
            )
        if not encoded:
            return

        try:
            raw = base64.b64decode(encoded)
            sig = Image.open(io.BytesIO(raw)).convert("RGBA")
            sig.load()

            s = preview_state["scale"]
            max_w = max(1, int(365 * s))
            max_h = max(1, int(22 * s))

            ratio = min(
                max_w / max(1, sig.width),
                max_h / max(1, sig.height)
            )
            nw = max(1, int(sig.width * ratio))
            nh = max(1, int(sig.height * ratio))
            sig = sig.resize((nw, nh), Image.LANCZOS)

            photo = ImageTk.PhotoImage(sig, master=win)
            preview_state["live_images"].append(photo)
            preview_canvas.create_image(
                12 + 102 * s,
                12 + (float(top_y) - 4.0) * s,
                image=photo,
                anchor="nw",
                tags=("live_preview",)
            )
        except Exception as e:
            print("SPECIALTY LIVE SIGNATURE PREVIEW ERROR:", e)

    def _draw_live_specialty_values(page_index):
        """Draw ALL entered specialties on the displayed PDF page.

        Previously only the currently selected specialty was drawn. When the
        user switched the dropdown, earlier unsaved entries therefore vanished
        from the backdrop even though they still existed in specialty_state.
        """
        preview_state["live_images"] = []

        # Student header only exists on page 1.
        if page_index == 0:
            student = specialty_state.get("student", {})
            _live_preview_text(
                89, 59.8, 484, student.get("name", ""),
                font_size=10, bold=True
            )
            _live_preview_text(69, 76.8, 505, student.get("address", ""))
            _live_preview_text(52, 93.8, 141, student.get("city", ""))
            _live_preview_text(251, 93.8, 74, student.get("province", ""))
            _live_preview_text(359, 93.8, 92, student.get("country", ""))
            _live_preview_text(514, 93.8, 61, student.get("postal", ""))
            _live_preview_text(62, 110.8, 236, student.get("phone", ""))
            _live_preview_text(320, 110.8, 254, student.get("fax", ""))
            _live_preview_text(83, 128.3, 88, student.get("birth_date", ""))

            sex = str(student.get("sex", "") or "").upper().strip()
            s = preview_state["scale"]
            if sex == "M":
                preview_canvas.create_text(
                    12 + 211 * s, 12 + 126 * s,
                    text="X", anchor="nw",
                    font=("Arial", 11, "bold"),
                    tags=("live_preview",)
                )
            elif sex == "F":
                preview_canvas.create_text(
                    12 + 246 * s, 12 + 126 * s,
                    text="X", anchor="nw",
                    font=("Arial", 11, "bold"),
                    tags=("live_preview",)
                )

        all_records = specialty_state.get("specialties", {})

        # Draw every specialty that belongs to this page. This preserves
        # previously entered unsaved specialties while another one is edited.
        for specialty_name in SPECIALTY_NAMES:
            definition = SPECIALTY_DEFINITIONS.get(specialty_name)
            if not definition or int(definition["page"]) != page_index:
                continue

            rec = all_records.get(specialty_name)
            if not isinstance(rec, dict):
                continue

            ay = definition["academic_y"]
            asy = definition["academic_sig_y"]
            academic_removed = bool(rec.get("academic_removed", False))

            if not academic_removed:
                _live_preview_text(
                    98, ay, 59, rec.get("academic_date", "")
                )
                _live_preview_text(
                    222, ay, 264, rec.get("academic_instructor", "")
                )
                _live_preview_text(
                    505, ay, 69, rec.get("academic_padi", "")
                )

                academic_signature_eligible = bool(
                    str(rec.get("academic_date", "") or "").strip()
                    and str(rec.get("academic_instructor", "") or "").strip()
                    and str(rec.get("academic_signature_date", "") or "").strip()
                )

                # Current specialty may use the newly drawn reusable signature
                # immediately; completed specialties use their own stored snapshot.
                academic_signature_png = str(
                    rec.get("student_signature_png", "") or ""
                )
                if specialty_name == local_specialty_var.get():
                    academic_signature_png = (
                        academic_signature_png
                        or str(specialty_state.get("student_signature_png", "") or "")
                    )

                _live_preview_signature(
                    asy,
                    academic_signature_eligible,
                    academic_signature_png
                )
                _live_preview_text(
                    505, asy, 69,
                    rec.get("academic_signature_date", "")
                    if academic_signature_eligible else ""
                )

            dives = rec.get("dives", [])
            for i, dy in enumerate(definition.get("dive_y", [])):
                if i >= len(dives):
                    break

                dive = dives[i]
                if not isinstance(dive, dict):
                    continue
                if bool(dive.get("removed", False)):
                    continue

                _live_preview_text(
                    92, dy, 66, dive.get("date", "")
                )
                _live_preview_text(
                    222, dy, 265, dive.get("instructor", "")
                )
                _live_preview_text(
                    505, dy, 69, dive.get("padi", "")
                )

                sy = definition["dive_sig_y"][i]

                dive_signature_eligible = bool(
                    str(dive.get("date", "") or "").strip()
                    and str(dive.get("instructor", "") or "").strip()
                )

                dive_signature_png = str(
                    rec.get("student_signature_png", "") or ""
                )
                if specialty_name == local_specialty_var.get():
                    dive_signature_png = (
                        dive_signature_png
                        or str(specialty_state.get("student_signature_png", "") or "")
                    )

                _live_preview_signature(
                    sy,
                    dive_signature_eligible,
                    dive_signature_png
                )
                if dive_signature_eligible and dive_signature_png:
                    _live_preview_text(
                        505, sy, 69,
                        dive.get("signature_date", "")
                        or rec.get("academic_signature_date", "")
                        or date.today().strftime("%Y-%m-%d")
                    )


    def _schedule_backdrop_autofit(event=None):
        """Re-fit the PDF after the preview pane/window is resized."""
        old = preview_state.get("fit_after_id")
        if old:
            try:
                win.after_cancel(old)
            except Exception:
                pass
        preview_state["fit_after_id"] = win.after(
            180, render_specialty_backdrop
        )

    preview_canvas.bind("<Configure>", _schedule_backdrop_autofit)

    def _apply_auto_signature_rules():
        """Automatically sign eligible rows in the current specialty."""
        current_signature = str(
            specialty_state.get("student_signature_png", "") or ""
        )
        if not current_signature:
            return

        current_name = active_specialty_name[0]
        if current_name not in SPECIALTY_DEFINITIONS:
            return
        current_rec = _ensure_specialty_record(current_name)

        academic_date = (
            record_vars["academic_date"].get().strip()
            if record_vars.get("academic_date") is not None else ""
        )
        academic_instructor = (
            record_vars["academic_instructor"].get().strip()
            if record_vars.get("academic_instructor") is not None else ""
        )
        academic_signed_date = (
            record_vars["academic_signature_date"].get().strip()
            if record_vars.get("academic_signature_date") is not None else ""
        )

        academic_eligible = bool(
            not bool(current_rec.get("academic_removed", False))
            and academic_date
            and academic_instructor
            and academic_signed_date
        )

        any_signature_eligible = academic_eligible

        # Snapshot first, before changing traced BooleanVars.
        if academic_eligible:
            current_rec["student_signature_png"] = current_signature

        if record_vars.get("academic_signed") is not None:
            if bool(record_vars["academic_signed"].get()) != academic_eligible:
                record_vars["academic_signed"].set(academic_eligible)

        for row in record_vars.get("dives", []):
            dive_date = row["date"].get().strip() if row.get("date") is not None else ""
            dive_instructor = (
                row["instructor"].get().strip()
                if row.get("instructor") is not None else ""
            )
            dive_eligible = bool(dive_date and dive_instructor)
            any_signature_eligible = any_signature_eligible or dive_eligible

            if row.get("signed") is not None:
                if bool(row["signed"].get()) != dive_eligible:
                    row["signed"].set(dive_eligible)

        # Commit the CURRENT reusable signature to THIS specialty only.
        # Once stored here, later redrawing for another specialty cannot
        # alter this specialty's already-applied signature.
        if any_signature_eligible:
            current_rec["student_signature_png"] = current_signature

        save_controls_to_state(current_name)

        # save_controls_to_state does not own the snapshot field, so re-assert it.
        if any_signature_eligible:
            current_rec["student_signature_png"] = current_signature

    def schedule_live_preview(*_args):
        """Apply signature eligibility rules, then refresh the backdrop."""
        try:
            _apply_auto_signature_rules()
        except Exception as e:
            print("AUTO SIGNATURE RULE WARNING:", e)
        old = preview_state.get("after_id")
        if old:
            try:
                win.after_cancel(old)
            except Exception:
                pass

        preview_state["after_id"] = win.after(
            120, render_specialty_backdrop
        )

    def render_specialty_backdrop(*_args):
        """Render only a Specialty PDF explicitly selected by the user."""
        preview_canvas.delete("all")

        if not worksheet_loaded[0]:
            preview_canvas.create_text(
                24, 28, anchor="nw",
                text="Click 'Open Existing / Template PDF' to select a Specialty worksheet.",
                fill="white", font=("Arial", 11, "bold")
            )
            preview_page_label.config(text="No Specialty PDF loaded")
            return

        name = local_specialty_var.get() or SPECIALTY_NAMES[0]
        definition = SPECIALTY_DEFINITIONS.get(name, SPECIALTY_DEFINITIONS[SPECIALTY_NAMES[0]])
        page_index = int(definition["page"])
        pdf_file = _preview_pdf_path()
        if pdf_file is None or not pdf_file.exists():
            preview_canvas.create_text(
                24, 28, anchor="nw",
                text="No Specialty PDF loaded.",
                fill="white", font=("Arial", 11, "bold")
            )
            preview_page_label.config(text="No Specialty PDF loaded")
            return

        try:
            doc = pdfium.PdfDocument(str(pdf_file))
            page = doc[page_index]

            # Auto-fit the PDF page to the CURRENT width of the backdrop.
            # This keeps the backdrop compact and gives Worksheet Data more room.
            try:
                page_w, page_h = page.get_size()
                preview_canvas.update_idletasks()
                available_w = max(260, preview_canvas.winfo_width() - 28)
                fit_scale = available_w / max(1.0, float(page_w))

                # Fit-to-width only: never enlarge the worksheet unnecessarily.
                preview_state["scale"] = max(0.45, min(1.08, fit_scale))
            except Exception:
                preview_state["scale"] = 0.85

            bitmap = page.render(scale=preview_state["scale"])
            pil = bitmap.to_pil().convert("RGB")
            photo = ImageTk.PhotoImage(pil)
            preview_state["photo"] = photo
            preview_state["page"] = page_index

            preview_canvas.delete("all")
            margin = 12
            preview_canvas.create_image(margin, margin, image=photo, anchor="nw")

            # Overlay CURRENT editor values, including unsaved changes.
            _draw_live_specialty_values(page_index)

            # Highlight the complete specialty block while leaving the PDF visible.
            ys = [definition["academic_y"], definition["academic_sig_y"]]
            ys.extend(definition.get("dive_y", []))
            ys.extend(definition.get("dive_sig_y", []))
            top_pdf = max(0.0, min(ys) - 27.0)
            bottom_pdf = min(float(pil.height) / preview_state["scale"], max(ys) + 24.0)
            s = preview_state["scale"]
            preview_canvas.create_rectangle(
                margin + 18 * s,
                margin + top_pdf * s,
                margin + 590 * s,
                margin + bottom_pdf * s,
                outline="#d00000",
                width=3
            )
            preview_canvas.create_text(
                margin + 24 * s,
                margin + (top_pdf + 5) * s,
                text=name,
                anchor="nw",
                fill="#d00000",
                font=("Arial", 11, "bold")
            )

            # Stack ALL worksheet pages in one vertically scrollable canvas.
            # Keep the live overlays and red selection box on the selected page.
            gap = 22
            page_height = pil.height + gap
            selected_offset = page_index * page_height
            preview_canvas.move("all", 0, selected_offset)
            all_photos = [None] * len(doc)
            all_photos[page_index] = photo
            for other_index in range(len(doc)):
                if other_index == page_index:
                    continue
                other_page = None
                other_bitmap = None
                try:
                    other_page = doc[other_index]
                    other_bitmap = other_page.render(scale=preview_state["scale"])
                    other_pil = other_bitmap.to_pil().convert("RGB")
                    other_photo = ImageTk.PhotoImage(other_pil)
                    all_photos[other_index] = other_photo
                    preview_canvas.create_image(
                        margin, margin + other_index * page_height,
                        image=other_photo, anchor="nw"
                    )
                finally:
                    if other_bitmap is not None:
                        try:
                            other_bitmap.close()
                        except Exception:
                            pass
                    if other_page is not None:
                        try:
                            other_page.close()
                        except Exception:
                            pass
            preview_state["all_photos"] = all_photos  # prevent Tk image GC
            full_width = pil.width + margin * 2
            full_height = len(doc) * page_height + margin * 2
            preview_canvas.configure(scrollregion=(0, 0, full_width, full_height))
            preview_page_label.config(
                text=f"All {len(doc)} pages — {name} on page {page_index + 1} — {Path(pdf_file).name}"
            )
            # Navigate only when the selected specialty or source PDF changes.
            # A routine live redraw must not snap the scrollbar back to the
            # specialty while the user is browsing other worksheet pages.
            navigation_key = (str(pdf_file), name)
            if preview_state.get("last_navigation") != navigation_key:
                preview_state["last_navigation"] = navigation_key
                # Tk Canvas.yview_moveto takes a fraction of the ENTIRE scroll
                # region, not a fraction of the scrollable distance. Dividing
                # by (full_height - viewport_height) positioned later
                # specialties too far down the worksheet.
                target_y = max(0.0, selected_offset + margin + top_pdf * s - 45.0)
                preview_canvas.yview_moveto(
                    max(0.0, min(1.0, target_y / max(1.0, full_height)))
                )

            try:
                page.close()
                doc.close()
            except Exception:
                pass
        except Exception as e:
            preview_canvas.delete("all")
            preview_canvas.create_text(
                20, 20, anchor="nw",
                text=f"Unable to render PDF backdrop:\n{e}",
                fill="white", font=("Arial", 11)
            )
            print("SPECIALTY PDF BACKDROP ERROR:", e)

    # ---- Scrollable data editor on the right ----
    outer = ttk.Frame(editor_frame)
    outer.pack(fill="both", expand=True)
    sc = tk.Canvas(outer, highlightthickness=0)
    sb = ttk.Scrollbar(outer, orient="vertical", command=sc.yview)
    body = ttk.Frame(sc)
    body.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
    body_window = sc.create_window((0, 0), window=body, anchor="nw")
    sc.configure(yscrollcommand=sb.set)
    sc.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    def _resize_editor_body(event):
        sc.itemconfigure(body_window, width=max(1, event.width))
    sc.bind("<Configure>", _resize_editor_body)

    student_vars = {}
    record_vars = {"dives": []}

    def clear_body():
        for child in body.winfo_children():
            child.destroy()
        student_vars.clear()
        record_vars.clear()
        record_vars["dives"] = []

    def get_selected_instructor():
        name = local_instructor_var.get()
        return next((i for i in instructor_list if i.get("name") == name), None)

    active_specialty_name = [local_specialty_var.get()]

    def save_controls_to_state(specialty_name_override=None):
        """Save visible controls only to the specialty they were created for."""
        student = specialty_state.setdefault("student", {})
        for key, var in student_vars.items():
            try:
                student[key] = var.get()
            except Exception:
                pass

        target_name = specialty_name_override or active_specialty_name[0]
        if target_name not in SPECIALTY_DEFINITIONS:
            return

        rec = _ensure_specialty_record(target_name)
        # Signature flags below are stored only inside this specialty record.

        try:
            rec["academic_date"] = record_vars["academic_date"].get()
            rec["academic_instructor"] = record_vars["academic_instructor"].get()
            rec["academic_padi"] = record_vars["academic_padi"].get()
            rec["academic_signature_date"] = record_vars["academic_signature_date"].get()
            rec["academic_signed"] = bool(record_vars["academic_signed"].get())
            rec["academic_removed"] = bool(rec.get("academic_removed", False))
        except Exception:
            pass

        rows = record_vars.get("dives", [])
        rec_dives = rec.get("dives", [])
        for idx, rowvars in enumerate(rows):
            if idx >= len(rec_dives):
                break
            try:
                rec_dives[idx]["date"] = rowvars["date"].get()
                rec_dives[idx]["instructor"] = rowvars["instructor"].get()
                rec_dives[idx]["padi"] = rowvars["padi"].get()
                if not str(rec_dives[idx].get("signature_date", "") or "").strip() and rowvars["signed"].get():
                    rec_dives[idx]["signature_date"] = (
                        str(rec.get("academic_signature_date", "") or "").strip()
                        or date.today().strftime("%Y-%m-%d")
                    )
                rec_dives[idx]["signed"] = bool(rowvars["signed"].get())
                rec_dives[idx]["removed"] = bool(
                    rec_dives[idx].get("removed", False)
                )
            except Exception:
                pass


    def apply_instructor_to_rows():
        inst = get_selected_instructor()
        if not inst:
            messagebox.showerror("Specialty Worksheet", "Select an instructor first.", parent=win)
            return
        name = inst.get("name", "")
        padi = inst.get("padi_number", "")
        if record_vars.get("academic_instructor"):
            record_vars["academic_instructor"].set(name)
            record_vars["academic_padi"].set(padi)
        for row in record_vars.get("dives", []):
            row["instructor"].set(name)
            row["padi"].set(padi)

    def fill_today():
        """Apply the specialty-window calendar date to all current specialty date fields."""
        chosen = specialty_date_picker.get_date().strftime("%Y-%m-%d")

        # Update the Tk variables currently displayed in the right-hand editor.
        if record_vars.get("academic_date") is not None:
            record_vars["academic_date"].set(chosen)

        # Signature dates are intentionally NOT auto-populated.
        for row in record_vars.get("dives", []):
            if row.get("date") is not None:
                row["date"].set(chosen)

        # Persist those GUI values immediately to specialty_state.
        save_controls_to_state()

        # Rebuild the body so every visible field definitely reflects the new date.
        build_body()
        schedule_live_preview()


    def signature_status_text():
        return "Student signature in worksheet" if specialty_state.get("student_signature_png") else "No student signature"

    def build_body(*args):
        # IMPORTANT:
        # Never save controls here. When the dropdown changes, the widgets still
        # contain the PREVIOUS specialty's values. Saving from build_body() would
        # copy those values into the newly selected specialty.
        current_name = local_specialty_var.get()

        clear_body()

        # Only after the old widgets have been discarded do these newly-created
        # controls belong to the selected specialty.
        active_specialty_name[0] = current_name
        student = specialty_state.setdefault("student", {})
        defaults = _specialty_default_student()
        for k, v in defaults.items():
            student.setdefault(k, v)

        student_box = ttk.LabelFrame(body, text="Student Information", padding=8)
        student_box.pack(fill="x", padx=8, pady=6)

        student_fields = [
            ("name", "Student Name", 0, 0, 38),
            ("address", "Address", 1, 0, 38),
            ("city", "City", 2, 0, 22),
            ("province", "State/Province", 2, 2, 16),
            ("country", "Country", 3, 0, 18),
            ("postal", "Zip/Postal Code", 3, 2, 14),
            ("phone", "Phone", 4, 0, 20),
            ("fax", "Fax", 4, 2, 20),
            ("birth_date", "Birth Date", 5, 0, 18),
        ]
        for key, label, row, col, width in student_fields:
            ttk.Label(student_box, text=label + ":").grid(
                row=row, column=col, sticky="w", padx=4, pady=3
            )
            var = tk.StringVar(value=student.get(key, ""))
            def _student_live_update(*_args):
                student = specialty_state.setdefault("student", {})
                for _key, _var in student_vars.items():
                    try:
                        student[_key] = _var.get()
                    except Exception:
                        pass
                schedule_live_preview()

            var.trace_add("write", _student_live_update)
            student_vars[key] = var
            ttk.Entry(student_box, textvariable=var, width=width, style="SpecialtyBold.TEntry").grid(
                row=row, column=col + 1, sticky="ew", padx=4, pady=3
            )

        ttk.Label(student_box, text="Sex:").grid(row=5, column=2, sticky="w", padx=4)
        sexvar = tk.StringVar(value=student.get("sex", ""))
        sexvar.trace_add("write", schedule_live_preview)
        student_vars["sex"] = sexvar
        sexframe = ttk.Frame(student_box)
        sexframe.grid(row=5, column=3, sticky="w")
        ttk.Radiobutton(sexframe, text="M", variable=sexvar, value="M").pack(side="left")
        ttk.Radiobutton(sexframe, text="F", variable=sexvar, value="F").pack(side="left")

        # Visible student signature preview in the Student Information box.
        ttk.Label(student_box, text="Student Signature:").grid(
            row=6, column=0, sticky="nw", padx=4, pady=(8, 3)
        )
        student_sig_preview = tk.Canvas(
            student_box,
            width=320,
            height=64,
            background="white",
            highlightthickness=1,
            highlightbackground="#999999"
        )
        student_sig_preview.grid(
            row=6, column=1, columnspan=3,
            sticky="w", padx=4, pady=(8, 3)
        )
        student_sig_preview._photo = None

        def refresh_student_signature_preview():
            student_sig_preview.delete("all")
            encoded = specialty_state.get("student_signature_png", "")
            if not encoded:
                student_sig_preview.create_text(
                    160, 32,
                    text="Click here to draw student signature",
                    fill="#666666",
                    font=("Arial", 9)
                )
                student_sig_preview._photo = None
                return
            try:
                raw = base64.b64decode(encoded)
                img = Image.open(io.BytesIO(raw)).convert("RGBA")
                img.load()
                max_w, max_h = 300, 50
                ratio = min(
                    max_w / max(1, img.width),
                    max_h / max(1, img.height)
                )
                nw = max(1, int(img.width * ratio))
                nh = max(1, int(img.height * ratio))
                img = img.resize((nw, nh), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img, master=win)
                student_sig_preview._photo = photo
                student_sig_preview.create_image(
                    160, 32, image=photo, anchor="center"
                )
            except Exception as e:
                student_sig_preview.create_text(
                    160, 32,
                    text="Unable to display signature",
                    fill="#666666",
                    font=("Arial", 9)
                )
                student_sig_preview._photo = None
                print("STUDENT SIGNATURE PREVIEW ERROR:", e)

        refresh_student_signature_preview()

        # Keep the signature controls on separate rows so they remain visible
        # even when the right-hand Specialty data pane is narrow.
        sigframe = ttk.Frame(student_box)
        sigframe.grid(row=7, column=0, columnspan=4, sticky="ew", pady=(5, 0))
        sig_label = ttk.Label(sigframe, text=signature_status_text())
        sig_label.pack(side="top", anchor="w", pady=(0, 5))

        sig_button_frame = ttk.Frame(sigframe)
        sig_button_frame.pack(side="top", fill="x", anchor="w")

        def _import_open_water_student_signature():
            """Copy the current main-editor Open Water student signature into
            Specialty memory only. No new signature file is created.
            """
            source_value = state.get("student_signature", "")
            if not source_value:
                messagebox.showinfo(
                    "Import Open Water Signature",
                    "No student signature is currently loaded in the Open Water form.",
                    parent=win,
                )
                return

            try:
                source_path = resolve_signature_path(source_value)
            except Exception:
                source_path = Path(str(source_value))

            if not source_path or not Path(source_path).exists():
                messagebox.showinfo(
                    "Import Open Water Signature",
                    "The Open Water student signature is not currently available.",
                    parent=win,
                )
                return

            try:
                # Read the existing Open Water signature and convert it directly
                # to PNG bytes held inside specialty_state.  Do not create a new
                # signature file for the Specialty worksheet.
                with Image.open(source_path) as source_img:
                    source_img = source_img.convert("RGBA")
                    out = io.BytesIO()
                    source_img.save(out, format="PNG")
                specialty_state["student_signature_png"] = base64.b64encode(
                    out.getvalue()
                ).decode("ascii")

                # Do not invent or overwrite the Specialty signing date.
                specialty_state["student_signature_date"] = ""

                sig_label.config(text=signature_status_text())
                refresh_student_signature_preview()
                save_controls_to_state(active_specialty_name[0])
                render_specialty_backdrop()

                messagebox.showinfo(
                    "Import Open Water Signature",
                    "The student signature from the Open Water form was imported into this Specialty worksheet.\n\n"
                    "It is kept in the Specialty PDF data and no separate Specialty signature file is created.",
                    parent=win,
                )
            except Exception as e:
                messagebox.showerror(
                    "Import Open Water Signature",
                    f"The Open Water student signature could not be imported.\n\n{e}",
                    parent=win,
                )

        # Expose the import action to the top action bar.  The button itself
        # is kept beside "Save Specialty PDF" rather than changing the
        # Student Signature section layout.
        import_open_water_signature_command[0] = _import_open_water_student_signature

        def _after_specialty_signature_saved():
            sig_label.config(text=signature_status_text())
            refresh_student_signature_preview()

            # The current specialty's Signed Date (Student) is the date on
            # which the currently drawn student signature was created/saved.
            current_rec = _ensure_specialty_record(local_specialty_var.get())
            signature_created_date = str(
                specialty_state.get("student_signature_date", "") or ""
            ).strip()
            if signature_created_date:
                current_rec["academic_signature_date"] = signature_created_date

                if record_vars.get("academic_signature_date") is not None:
                    record_vars["academic_signature_date"].set(
                        signature_created_date
                    )

                # StableDatePicker has its own display StringVar, so update
                # the actual picker as well as the backing record variable.
                try:
                    academic_signature_date_picker.set_date(
                        signature_created_date
                    )
                    academic_signature_date_picker._display_var.set(
                        signature_created_date
                    )
                    _update_signed_date_highlight()
                except Exception as e:
                    print("SIGNED DATE PICKER UPDATE WARNING:", e)

            # Automatically apply to Academics only when Date Completed
            # and Instructor are both present.
            academic_date = (
                record_vars["academic_date"].get().strip()
                if record_vars.get("academic_date") is not None else ""
            )
            academic_instructor = (
                record_vars["academic_instructor"].get().strip()
                if record_vars.get("academic_instructor") is not None else ""
            )
            if record_vars.get("academic_signed") is not None:
                record_vars["academic_signed"].set(
                    bool(academic_date and academic_instructor)
                )

            # Automatically apply to each dive only when that dive has
            # both a Dive Date and an Instructor.
            for row in record_vars.get("dives", []):
                dive_date = (
                    row["date"].get().strip()
                    if row.get("date") is not None else ""
                )
                instructor_name = (
                    row["instructor"].get().strip()
                    if row.get("instructor") is not None else ""
                )
                row["signed"].set(
                    bool(dive_date and instructor_name)
                )

            save_controls_to_state(active_specialty_name[0])
            current_rec = _ensure_specialty_record(local_specialty_var.get())
            for dive in current_rec.get("dives", []):
                if dive.get("signed") and not dive.get("signature_date"):
                    dive["signature_date"] = (
                        str(current_rec.get("academic_signature_date", "") or "").strip()
                        or date.today().strftime("%Y-%m-%d")
                    )
            schedule_live_preview()

        def _open_student_signature_draw():
            _specialty_draw_student_signature(
                win,
                _after_specialty_signature_saved
            )

        def _student_signature_preview_clicked(event=None):
            # The empty signature box acts as a shortcut to the drawing tool.
            # If a signature already exists, keep the normal Draw/Replace button
            # as the explicit way to replace it.
            if not specialty_state.get("student_signature_png"):
                _open_student_signature_draw()

        student_sig_preview.bind(
            "<Button-1>",
            _student_signature_preview_clicked
        )
        student_sig_preview.configure(cursor="hand2")

        ttk.Button(
            sig_button_frame,
            text="Draw/Replace Student Signature",
            command=_open_student_signature_draw
        ).pack(side="left", padx=(0, 6))

        def _apply_existing_student_signature():
            """Apply an already imported/drawn signature to eligible rows."""
            if not specialty_state.get("student_signature_png"):
                messagebox.showinfo(
                    "Student Signature",
                    "No student signature is loaded. Import it from the Open Water form or draw one first.",
                    parent=win
                )
                return
            if local_specialty_var.get() not in SPECIALTY_DEFINITIONS:
                messagebox.showinfo(
                    "Select Specialty",
                    "Select the correct specialty before applying the student signature.",
                    parent=win
                )
                return
            _after_specialty_signature_saved()
            messagebox.showinfo(
                "Student Signature",
                "The stored student signature has been assigned to eligible Academics and Dive entries. "
                "Check the required dates and instructor names before saving the PDF.",
                parent=win
            )

        ttk.Button(
            sig_button_frame,
            text="Apply Existing Student Signature",
            command=_apply_existing_student_signature
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            sig_button_frame,
            text="Import Signature from Open Water",
            command=_import_open_water_student_signature
        ).pack(side="left", padx=(0, 6))



        name = current_name
        if name not in SPECIALTY_DEFINITIONS:
            ttk.Label(
                body,
                text="Select a specialty from the dropdown above before entering course details.",
                foreground="#a05000",
                wraplength=420
            ).pack(anchor="w", padx=12, pady=12)
            win.after_idle(render_specialty_backdrop)
            return
        rec = _ensure_specialty_record(name)

        # If this specialty has not yet stored a Signed Date (Student),
        # default it to the creation date of the currently saved signature.
        if not str(rec.get("academic_signature_date", "") or "").strip():
            signature_created_date = str(
                specialty_state.get("student_signature_date", "") or ""
            ).strip()
            if signature_created_date:
                rec["academic_signature_date"] = signature_created_date

        # Selected specialty heading: larger, bold, and enclosed in a rectangle.
        specialty_title = tk.Label(
            body,
            text=name,
            font=("Arial", 14, "bold"),
            relief="solid",
            borderwidth=2,
            padx=10,
            pady=2,
        )
        section = ttk.LabelFrame(body, labelwidget=specialty_title, padding=8)
        section.pack(fill="x", padx=8, pady=6)
        section.columnconfigure(1, weight=1)
        section.columnconfigure(2, weight=0)

        def _watch_var(var):
            try:
                var.trace_add("write", schedule_live_preview)
            except Exception:
                pass
            return var

        def entry_row(parent, row, label, value="", width=18):
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=4, pady=3)
            var = tk.StringVar(value=value)
            _watch_var(var)
            ttk.Entry(parent, textvariable=var, width=width, style="SpecialtyBold.TEntry").grid(
                row=row, column=1, sticky="ew", padx=4, pady=3
            )
            return var

        ttk.Label(section, text="Academics / Confined Water", font=("Arial", 10, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 5)
        )
        # Academics / Confined Water Date Completed uses a calendar picker.
        ttk.Label(section, text="Date Completed:").grid(
            row=1, column=0, sticky="w", padx=4, pady=3
        )

        academic_removed = bool(rec.get("academic_removed", False))
        academic_date_value = str(rec.get("academic_date", "") or "").strip()
        if not academic_date_value and not academic_removed:
            academic_date_value = date.today().strftime("%Y-%m-%d")

        record_vars["academic_date"] = tk.StringVar(
            value=academic_date_value
        )
        _watch_var(record_vars["academic_date"])

        academic_date_picker = StableDatePicker(
            section,
            width=16,
            date_pattern="yyyy-mm-dd"
        )
        try:
            if academic_date_value:
                academic_date_picker.set_date(academic_date_value)
            else:
                academic_date_picker.set_date(date.today())
                academic_date_picker._display_var.set("")
        except Exception:
            academic_date_picker.set_date(date.today())
            if academic_date_value:
                record_vars["academic_date"].set(
                    academic_date_picker.get_date().strftime("%Y-%m-%d")
                )
            else:
                academic_date_picker._display_var.set("")

        academic_date_picker.grid(
            row=1, column=1, sticky="w", padx=4, pady=3
        )

        def _academic_date_selected(event=None):
            rec["academic_removed"] = False
            selected = academic_date_picker.get_date().strftime("%Y-%m-%d")
            record_vars["academic_date"].set(selected)
            save_controls_to_state()
            schedule_live_preview()

        academic_date_picker.bind(
            "<<DateEntrySelected>>",
            _academic_date_selected
        )

        def _sync_academic_date_picker(*_args):
            value = record_vars["academic_date"].get().strip()
            if not value:
                return
            try:
                current = academic_date_picker.get_date().strftime("%Y-%m-%d")
                if current != value:
                    academic_date_picker.set_date(value)
            except Exception:
                pass

        record_vars["academic_date"].trace_add(
            "write",
            _sync_academic_date_picker
        )

        # Academics / Confined Water instructor dropdown.
        ttk.Label(section, text="Instructor Name:").grid(
            row=2, column=0, sticky="w", padx=4, pady=3
        )
        record_vars["academic_instructor"] = tk.StringVar(
            value=rec.get("academic_instructor", "")
        )
        _watch_var(record_vars["academic_instructor"])

        academic_instructor_combo = ttk.Combobox(
            section,
            textvariable=record_vars["academic_instructor"],
            values=[inst.get("name", "") for inst in instructor_list],
            state="readonly",
            width=34
        )
        academic_instructor_combo.grid(
            row=2, column=1, sticky="ew", padx=4, pady=3
        )

        record_vars["academic_padi"] = entry_row(
            section, 3, "PADI #:", rec.get("academic_padi", ""), 18
        )

        def _academic_instructor_selected(event=None):
            rec["academic_removed"] = False
            selected_name = record_vars["academic_instructor"].get()
            inst = next(
                (item for item in instructor_list
                 if item.get("name") == selected_name),
                None
            )

            # Academics selection affects Academics only.
            if inst:
                record_vars["academic_padi"].set(
                    str(inst.get("padi_number", "") or "")
                )
            else:
                record_vars["academic_padi"].set("")

            save_controls_to_state()
            schedule_live_preview()

        academic_instructor_combo.bind(
            "<<ComboboxSelected>>",
            _academic_instructor_selected
        )
        record_vars["academic_signed"] = tk.BooleanVar(
            value=bool(rec.get("academic_signed", False))
        )
        record_vars["academic_signed"].trace_add(
            "write", schedule_live_preview
        )

        # Academic student-signature date uses a calendar picker.
        ttk.Label(section, text="Signed Date (Student):").grid(
            row=4, column=0, sticky="w", padx=4, pady=3
        )
        record_vars["academic_signature_date"] = tk.StringVar(
            value=rec.get("academic_signature_date", "")
        )
        _watch_var(record_vars["academic_signature_date"])

        academic_signature_date_picker = StableDatePicker(
            section,
            width=16,
            date_pattern="yyyy-mm-dd"
        )
        try:
            existing_sig_date = record_vars["academic_signature_date"].get().strip()
            if existing_sig_date:
                academic_signature_date_picker.set_date(existing_sig_date)
            else:
                # Keep an internal calendar month/date available, but leave the
                # Signature Date visibly blank until the user selects a date.
                academic_signature_date_picker.set_date(date.today())
                academic_signature_date_picker._display_var.set("")
        except Exception:
            academic_signature_date_picker.set_date(date.today())
            academic_signature_date_picker._display_var.set("")

        academic_signature_date_picker.grid(
            row=4, column=1, sticky="w", padx=4, pady=3
        )

        # ttk.Entry in StableDatePicker is readonly, so Windows ignores a
        # direct background= setting. Use dedicated ttk styles and explicitly
        # map the readonly field background.
        signed_date_style = ttk.Style(win)

        signed_date_style.configure(
            "SignedDateEmpty.TEntry",
            fieldbackground="#fff59d",
            foreground="black"
        )
        signed_date_style.map(
            "SignedDateEmpty.TEntry",
            fieldbackground=[
                ("readonly", "#fff59d"),
                ("disabled", "#fff59d"),
                ("!disabled", "#fff59d")
            ],
            foreground=[
                ("readonly", "black"),
                ("!disabled", "black")
            ]
        )

        signed_date_style.configure(
            "SignedDateNormal.TEntry",
            fieldbackground="white",
            foreground="black"
        )
        signed_date_style.map(
            "SignedDateNormal.TEntry",
            fieldbackground=[
                ("readonly", "white"),
                ("!disabled", "white")
            ],
            foreground=[
                ("readonly", "black"),
                ("!disabled", "black")
            ]
        )

        def _update_signed_date_highlight(*_args):
            """Yellow while Signed Date (Student) is empty; white when populated."""
            value = record_vars["academic_signature_date"].get().strip()
            try:
                entry = academic_signature_date_picker._entry
                entry.configure(
                    style=(
                        "SignedDateNormal.TEntry"
                        if value
                        else "SignedDateEmpty.TEntry"
                    )
                )
            except Exception as e:
                print("SIGNED DATE HIGHLIGHT WARNING:", e)

        def _academic_signature_date_selected(event=None):
            rec["academic_removed"] = False
            selected = academic_signature_date_picker.get_date().strftime("%Y-%m-%d")
            record_vars["academic_signature_date"].set(selected)
            _update_signed_date_highlight()
            save_controls_to_state()
            schedule_live_preview()

        academic_signature_date_picker.bind(
            "<<DateEntrySelected>>",
            _academic_signature_date_selected
        )

        record_vars["academic_signature_date"].trace_add(
            "write", _update_signed_date_highlight
        )
        _update_signed_date_highlight()

        def _sync_academic_signature_picker(*_args):
            value = record_vars["academic_signature_date"].get().strip()
            try:
                if value:
                    current = academic_signature_date_picker.get_date().strftime(
                        "%Y-%m-%d"
                    )
                    if current != value:
                        academic_signature_date_picker.set_date(value)

                    # Force the visible readonly entry to match the backing value.
                    academic_signature_date_picker._display_var.set(value)
                else:
                    academic_signature_date_picker._display_var.set("")

                _update_signed_date_highlight()
            except Exception as e:
                print("SIGNED DATE SYNC WARNING:", e)

        record_vars["academic_signature_date"].trace_add(
            "write",
            _sync_academic_signature_picker
        )

        # Action buttons moved from the top red area into the green area.
        action_panel = ttk.Frame(section, padding=(12, 4))
        action_panel.grid(
            row=1, column=2, rowspan=4,
            sticky="n", padx=(18, 4), pady=2
        )
        ttk.Button(
            action_panel,
            text="Apply Selected Instructor\nto All Rows",
            command=apply_instructor_to_rows,
            width=24
        ).pack(fill="x", pady=(0, 8))

        ttk.Button(
            action_panel,
            text="Use Calendar Date",
            command=fill_today,
            width=24
        ).pack(fill="x")

        def _remove_academic_entry():
            if not messagebox.askyesno(
                "Remove Academic Entry",
                "Clear all Academics / Confined Water entries for this specialty?",
                parent=win
            ):
                return

            rec["academic_removed"] = True
            rec["academic_date"] = ""
            rec["academic_instructor"] = ""
            rec["academic_padi"] = ""
            rec["academic_signature_date"] = ""
            rec["academic_signed"] = False

            record_vars["academic_date"].set("")
            record_vars["academic_instructor"].set("")
            record_vars["academic_padi"].set("")
            record_vars["academic_signature_date"].set("")
            record_vars["academic_signed"].set(False)

            try:
                academic_date_picker.set_date(date.today())
                academic_date_picker._display_var.set("")
            except Exception:
                pass
            try:
                academic_signature_date_picker.set_date(date.today())
                academic_signature_date_picker._display_var.set("")
                _update_signed_date_highlight()
            except Exception:
                pass

            save_controls_to_state(active_specialty_name[0])
            # save_controls_to_state reads the blank controls; preserve the
            # explicit removed marker so today's default does not reappear.
            rec["academic_removed"] = True
            render_specialty_backdrop()

        ttk.Button(
            action_panel,
            text="Remove Academic Entry",
            command=_remove_academic_entry,
            width=24
        ).pack(fill="x", pady=(8, 0))

        start_row = 6
        for i, dive in enumerate(rec["dives"], start=1):
            r = start_row + (i - 1) * 6
            ttk.Separator(section, orient="horizontal").grid(
                row=r, column=0, columnspan=4, sticky="ew", pady=6
            )
            ttk.Label(section, text=f"Dive {i}", font=("Arial", 10, "bold")).grid(
                row=r + 1, column=0, columnspan=4, sticky="w"
            )
            rowvars = {}

            if i >= 1:
                # ---------------------------------------------------------
                # Independent date picker for every required specialty dive
                # ---------------------------------------------------------
                ttk.Label(section, text="Dive Date:").grid(
                    row=r + 2, column=0, sticky="w", padx=4, pady=3
                )
                initial_dive_date = str(dive.get("date", "") or "").strip()
                if not initial_dive_date and not bool(dive.get("removed", False)):
                    initial_dive_date = date.today().strftime("%Y-%m-%d")

                rowvars["date"] = tk.StringVar(value=initial_dive_date)
                _watch_var(rowvars["date"])

                dive_date_picker = StableDatePicker(
                    section,
                    width=16,
                    date_pattern="yyyy-mm-dd"
                )
                try:
                    if initial_dive_date:
                        dive_date_picker.set_date(initial_dive_date)
                    else:
                        dive_date_picker.set_date(date.today())
                        dive_date_picker._display_var.set("")
                except Exception:
                    dive_date_picker.set_date(date.today())
                    if initial_dive_date:
                        rowvars["date"].set(
                            dive_date_picker.get_date().strftime("%Y-%m-%d")
                        )
                    else:
                        dive_date_picker._display_var.set("")

                dive_date_picker.grid(
                    row=r + 2, column=1, sticky="w", padx=4, pady=3
                )

                def _dive_date_selected(
                    event=None,
                    var=rowvars["date"],
                    picker=dive_date_picker,
                    dive_record=dive
                ):
                    dive_record["removed"] = False
                    var.set(picker.get_date().strftime("%Y-%m-%d"))
                    save_controls_to_state(active_specialty_name[0])
                    schedule_live_preview()

                dive_date_picker.bind("<<DateEntrySelected>>", _dive_date_selected)

                # Keep the picker synchronized when "Use Calendar Date" or
                # another action changes the backing StringVar.
                def _sync_dive_picker(*_args, var=rowvars["date"], picker=dive_date_picker):
                    value = var.get().strip()
                    if not value:
                        return
                    try:
                        if picker.get_date().strftime("%Y-%m-%d") != value:
                            picker.set_date(value)
                    except Exception:
                        pass

                rowvars["date"].trace_add("write", _sync_dive_picker)

                # ---------------------------------------------------------
                # Independent instructor dropdown for every required specialty dive
                # ---------------------------------------------------------
                ttk.Label(section, text="Instructor Name:").grid(
                    row=r + 3, column=0, sticky="w", padx=4, pady=3
                )
                rowvars["instructor"] = tk.StringVar(
                    value=dive.get("instructor", "")
                )
                _watch_var(rowvars["instructor"])

                dive_instructor_combo = ttk.Combobox(
                    section,
                    textvariable=rowvars["instructor"],
                    values=[inst.get("name", "") for inst in instructor_list],
                    state="readonly",
                    width=34
                )
                dive_instructor_combo.grid(
                    row=r + 3, column=1, sticky="ew", padx=4, pady=3
                )

                rowvars["padi"] = entry_row(
                    section, r + 4, "PADI #:", dive.get("padi", ""), 18
                )

                def _dive_instructor_selected(
                    event=None,
                    name_var=rowvars["instructor"],
                    padi_var=rowvars["padi"],
                    dive_record=dive
                ):
                    # This selection applies ONLY to this dive.
                    dive_record["removed"] = False
                    selected_name = name_var.get()

                    inst = next(
                        (item for item in instructor_list
                         if item.get("name") == selected_name),
                        None
                    )

                    if inst:
                        selected_padi = str(
                            inst.get("padi_number", "") or ""
                        )
                        padi_var.set(selected_padi)
                        dive_record["instructor"] = selected_name
                        dive_record["padi"] = selected_padi
                    else:
                        padi_var.set("")
                        dive_record["instructor"] = ""
                        dive_record["padi"] = ""

                    # Do NOT populate any later dive rows.
                    save_controls_to_state(active_specialty_name[0])
                    schedule_live_preview()

                dive_instructor_combo.bind(
                    "<<ComboboxSelected>>",
                    _dive_instructor_selected
                )

            else:
                # Other dives retain the standard editable fields.
                rowvars["date"] = entry_row(
                    section, r + 2, "Dive Date:", dive.get("date", "")
                )
                rowvars["instructor"] = entry_row(
                    section, r + 3, "Instructor Name:",
                    dive.get("instructor", ""), 28
                )
                rowvars["padi"] = entry_row(
                    section, r + 4, "PADI #:", dive.get("padi", "")
                )

            rowvars["signed"] = tk.BooleanVar(
                value=bool(dive.get("signed", False))
                and bool(str(dive.get("instructor", "") or "").strip())
            )

            def _validate_dive_signed(*_args, row=rowvars):
                if row["signed"].get():
                    instructor_name = ""
                    if row.get("instructor") is not None:
                        instructor_name = row["instructor"].get().strip()
                    if not instructor_name:
                        row["signed"].set(False)
                        return
                schedule_live_preview()

            rowvars["signed"].trace_add("write", _validate_dive_signed)
            def _remove_dive_entry(
                row=rowvars,
                dive_record=dive,
                picker=dive_date_picker,
                dive_number=i
            ):
                if not messagebox.askyesno(
                    "Remove Dive Entry",
                    f"Clear all entries for Dive {dive_number}?",
                    parent=win
                ):
                    return

                dive_record["removed"] = True
                dive_record["date"] = ""
                dive_record["instructor"] = ""
                dive_record["padi"] = ""
                dive_record["signed"] = False
                dive_record["signature_date"] = ""

                row["date"].set("")
                row["instructor"].set("")
                row["padi"].set("")
                row["signed"].set(False)

                try:
                    picker.set_date(date.today())
                    picker._display_var.set("")
                except Exception:
                    pass

                save_controls_to_state(active_specialty_name[0])

                # save_controls_to_state reads the blank widgets; keep the
                # explicit removed marker so today's default stays suppressed.
                dive_record["removed"] = True
                render_specialty_backdrop()

            ttk.Button(
                section,
                text="Remove Dive Entry",
                command=_remove_dive_entry,
                width=20
            ).grid(
                row=r + 4, column=2,
                sticky="n", padx=(18, 4), pady=3
            )

            record_vars["dives"].append(rowvars)

        win.after_idle(render_specialty_backdrop)

    def open_existing():
        nonlocal template
        global specialty_state, specialty_worksheet_path
        chosen = filedialog.askopenfilename(
            title="Open Specialty Worksheet",
            filetypes=[("PDF files", "*.pdf")],
            parent=win
        )
        if not chosen:
            return
        loaded_data = _read_specialty_state_from_pdf(chosen)
        if not isinstance(loaded_data, dict):
            messagebox.showinfo(
                "Specialty Worksheet",
                "This PDF does not contain PADI Manager specialty data.\n"
                "It will be used as a blank worksheet/template.",
                parent=win
            )
            specialty_state = {
                "student": _specialty_default_student(),
                "specialties": {},
                "student_signature_png": "",
                "student_signature_date": "",
            }
        else:
            specialty_state = loaded_data
        # The selected PDF is now the ONLY active Specialty template/backdrop.
        template = Path(chosen)
        specialty_worksheet_path = chosen
        worksheet_loaded[0] = True

        try:
            _offer_import_existing_specialty_signature(chosen, parent=win)
        except Exception as e:
            print("SPECIALTY SIGNATURE IMPORT WARNING:", e)

        # Force an explicit choice after loading a template or saved worksheet.
        local_specialty_var.set("")
        active_specialty_name[0] = ""
        preview_state["last_navigation"] = None
        build_body()
        saved_specialty_snapshot[0] = specialty_snapshot()
        win.after_idle(render_specialty_backdrop)

    def save_pdf():
        global specialty_worksheet_path
        if not worksheet_loaded[0] or not specialty_worksheet_path:
            messagebox.showinfo(
                "Specialty Worksheet",
                "Open an existing/template Specialty PDF first.",
                parent=win
            )
            return

        if local_specialty_var.get() not in SPECIALTY_DEFINITIONS:
            messagebox.showwarning(
                "Select Specialty",
                "Please select the correct specialty from the dropdown before saving.",
                parent=win
            )
            return

        # Commit the currently displayed specialty before writing the PDF.
        try:
            save_controls_to_state(active_specialty_name[0])
        except Exception as e:
            print("SPECIALTY SAVE COMMIT WARNING:", e)
        save_controls_to_state()
        save_controls_to_state()

        # Use the current input worksheet filename as the Save As default.
        default = Path(specialty_worksheet_path).name

        output = filedialog.asksaveasfilename(
            title="Save PADI Specialty Worksheet",
            initialfile=default,
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            parent=win
        )
        if not output:
            return
        try:
            base = Path(specialty_worksheet_path or template)
            _export_specialty_worksheet(base, output)
            specialty_worksheet_path = output
            saved_specialty_snapshot[0] = specialty_snapshot()
            messagebox.showinfo(
                "Specialty Worksheet",
                f"Worksheet saved:\n{Path(output).resolve()}",
                parent=win
            )
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(
                "Specialty Worksheet Save Error", str(e), parent=win
            )

    ttk.Button(
        top_actions, text="Open Existing / Template PDF",
        command=open_existing
    ).pack(side="left", padx=3)

    ttk.Button(
        top_actions, text="Save Specialty PDF",
        command=save_pdf
    ).pack(side="left", padx=3)

    def import_open_water_signature_from_top():
        """Import the main Open Water student signature into the loaded Specialty PDF."""
        if not worksheet_loaded[0]:
            messagebox.showinfo(
                "Import Open Water Signature",
                "Open an existing / template Specialty PDF first.",
                parent=win,
            )
            return
        command = import_open_water_signature_command[0]
        if command is None:
            messagebox.showinfo(
                "Import Open Water Signature",
                "The Specialty worksheet controls are not ready yet.",
                parent=win,
            )
            return
        command()

    ttk.Button(
        top_actions, text="Import Open Water Signature",
        command=import_open_water_signature_from_top
    ).pack(side="left", padx=3)

    def _on_specialty_changed(*_args):
        """Commit the old specialty and then display the new specialty."""
        if not worksheet_loaded[0]:
            return

        previous_name = active_specialty_name[0]
        new_name = local_specialty_var.get()

        if not new_name or new_name == previous_name:
            return

        # Commit the OLD controls before they are destroyed.
        try:
            save_controls_to_state(previous_name)
        except Exception as e:
            print("SPECIALTY SWITCH SAVE WARNING:", e)

        # Now the new controls may be created from the new specialty's own record.
        active_specialty_name[0] = new_name
        build_body()

        # The preview now draws every saved in-memory specialty on this page.
        render_specialty_backdrop()

    local_specialty_var.trace_add("write", _on_specialty_changed)

    bottom = ttk.Frame(win, padding=8)
    bottom.pack(fill="x")
    ttk.Button(bottom, text="Close", command=close_specialty).pack(side="right", padx=4)

    # Do not build the Specialty data-entry form at startup. The form becomes
    # active only after Open Existing / Template PDF has selected a PDF.
    #
    # IMPORTANT: keep the scrollable editor widgets (outer/sc/body) alive.
    # Destroying editor_frame children here leaves build_body() holding Tk
    # references to widgets that no longer exist and causes
    # "bad window path name ...canvas.!frame" when a template is opened.
    clear_body()
    ttk.Label(
        body,
        text="No Specialty worksheet loaded.\n\nClick 'Open Existing / Template PDF' above to begin.",
        justify="center",
        anchor="center"
    ).pack(fill="both", expand=True, padx=20, pady=40)
    render_specialty_backdrop()

    # Signature import is therefore also possible only from open_existing().


# ---------------- Add New Instructor ----------------

def add_instructor_window():
    global instructor_window
    instructor_window = tk.Toplevel(root)
    win = instructor_window
    win.title("Instructor Manager")
    win.geometry("400x650")

    # Force window to front
    win.lift()
    win.focus_force()

    # ---------------- Existing Instructor ----------------

    tk.Label(win, text="Existing Instructor").pack(pady=5)

    existing_var = tk.StringVar()

    existing_combo = ttk.Combobox(
        win,
        textvariable=existing_var,
        values=[i["name"] for i in instructor_list],
        width=30
    )
    existing_combo.pack(pady=5)

    # ---------------- Instructor Details ----------------

    tk.Label(win, text="Name:").pack(pady=5)
    name_var = tk.StringVar()
    tk.Entry(win, textvariable=name_var).pack()

    tk.Label(win, text="Email:").pack(pady=5)
    email_var = tk.StringVar()
    tk.Entry(win, textvariable=email_var).pack()

    tk.Label(win, text="Phone Number:").pack(pady=5)
    phone_var = tk.StringVar()
    tk.Entry(win, textvariable=phone_var).pack()

    tk.Label(win, text="PADI Number:").pack(pady=5)
    padi_var = tk.StringVar()
    tk.Entry(win, textvariable=padi_var).pack()

    tk.Label(win, text="PADI Store Number:").pack(pady=5)
    store_var = tk.StringVar(value="4491")
    tk.Entry(win, textvariable=store_var).pack()

    tk.Label(win, text="Initials:").pack(pady=5)
    initials_var = tk.StringVar()
    tk.Entry(win, textvariable=initials_var).pack()

    tk.Label(win, text="Signature (draw inside app):").pack(pady=5)
    signature_var = tk.StringVar()

    
    

    def open_signature_draw():

        name = name_var.get()
        padi = padi_var.get()

        if not name:
            messagebox.showerror(
                "Error",
                "Enter name first."
            )
            return

        if not padi:
            messagebox.showerror(
                "Error",
                "Enter PADI number first."
            )
            return

        draw_signature_window(
            name,
            padi,
            signature_var
        )

    tk.Button(win, text="Draw Signature", command=open_signature_draw).pack(pady=10)

    def delete_instructor():
        name = name_var.get()

        if not name:
            messagebox.showerror("Error", "Enter or select an instructor name.")
            return

        instructor = next(
            (i for i in instructor_list if i["name"] == name),
            None
        )

        if not instructor:
            messagebox.showerror("Error", f"Instructor '{name}' not found.")
            return

        if not messagebox.askyesno(
            "Delete Instructor",
            f"Delete instructor '{name}'?"
        ):
            return

        instructor_list.remove(instructor)
        save_instructors({"instructors": instructor_list})

        instructor_dropdown["values"] = [
            i["name"] for i in instructor_list
        ]

        instructor_var.set("")

        messagebox.showinfo(
            "Deleted",
            f"Instructor '{name}' removed."
        )

        win.destroy()

    def load_selected(event=None):
        
        name = existing_var.get()

        instructor = next(
            (i for i in instructor_list if i["name"] == name),
            None
        )

        if not instructor:
            return

        name_var.set(instructor.get("name", ""))
        email_var.set(instructor.get("email", ""))
        phone_var.set(instructor.get("phone", ""))
        padi_var.set(instructor.get("padi_number", ""))
        store_var.set(instructor.get("store_number", "4491"))
        initials_var.set(instructor.get("initials", ""))
        signature_var.set(instructor.get("signature", ""))
        
    existing_combo.bind("<<ComboboxSelected>>", load_selected)

    def save_new():
        name = name_var.get()
        email = email_var.get()
        phone = phone_var.get()
        padi = padi_var.get()
        store = store_var.get()
        initials = initials_var.get()
        signature = signature_var.get()
        print("DEBUG signature_var =", signature)

        if not signature or not resolve_signature_path(signature).exists():
            messagebox.showerror("Error", "Signature must be drawn and saved.")
            return

        if not name or not email or not phone or not padi or not store or not initials:
            messagebox.showerror("Error", "All fields are required.")
            return

        new_inst = {
            "name": name,
            "email": email,
            "phone": phone,
            "padi_number": padi,
            "store_number": store,
            "initials": initials,
            "signature": signature
        }

        instructor_list.append(new_inst)
        save_instructors({"instructors": instructor_list})

        instructor_dropdown["values"] = [i["name"] for i in instructor_list]
        instructor_var.set(name)
        update_instructor_info()


        messagebox.showinfo("Saved", "Instructor added successfully.")
        
        win.destroy()

    btn_frame = tk.Frame(win)
    
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)


    tk.Button(
        btn_frame,
        text="Save Instructor",
        command=save_new
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="Delete Instructor",
        command=delete_instructor,
        bg="tomato"
    ).pack(side="left", padx=10)


# ---------------- Instructor Info Display ----------------

def update_instructor_info(*args):
    name = instructor_var.get()
    instructor = next((i for i in instructor_list if i["name"] == name), None)

    if not instructor:
        instructor_info.config(text="No instructor selected")
        return

    sig_path = instructor.get("signature")
    if sig_path and resolve_signature_path(sig_path).exists():
        sig_status = "✔ Signature saved"
    elif sig_path:
        sig_status = "✘ Signature path set but file missing"
    else:
        sig_status = "✘ No signature path set"

    info_text = (
        f"Name: {instructor['name']}   "
        f"Email: {instructor['email']}   "
        f"Phone: {instructor['phone']}\n"
        f"PADI#: {instructor['padi_number']}   "
        f"Store#: {instructor.get('store_number', '4491')}   "
        f"Initials: {instructor.get('initials', 'N/A')}   "
        f"{sig_status}"
    )


    instructor_info.config(text=info_text)

def toggle_identify_mode():
    global identify_mode, mask_edit_mode
    identify_mode = not identify_mode
    canvas_pdf.unbind("<Button-3>")


    if identify_mode:
        mask_edit_mode = False

        # Unbind ALL right-click handlers from mask edit mode
        canvas_pdf.unbind("<ButtonPress-3>")
        canvas_pdf.unbind("<ButtonRelease-3>")
        canvas_pdf.unbind("<Button-3>")   # ← REQUIRED

        # Bind identify-mode delete handler


        status_label.config(text="Identify Mode: Left-click to inspect, Right-click to delete")
        update_button_colors()

    else:
        canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal, add="+")
        if IS_MACOS:
            canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal, add="+")

        status_label.config(text="Identify Mode: OFF")
        update_button_colors()




def auto_detect_fields():
    global fields

    if not pdf_path or not pages:
        messagebox.showerror("Error", "Load a PDF first.")
        return

    # Run AcroForm detection
    auto_fields = detect_acroform_fields(pdf_path, pages)

    # Run heuristic detection
    heuristic_fields = []
    for idx, img in enumerate(pages):
        heuristic_fields.extend(heuristic_signature_boxes(img, idx))

    # Merge results
    new_fields = auto_fields + heuristic_fields

    if not new_fields:
        messagebox.showinfo("Auto-Detect Fields", "No fields detected.")
        return

    # Filter out duplicates by name
    existing_names = {f["name"] for f in fields}
    unique_new_fields = [f for f in new_fields if f["name"] not in existing_names]

    if not unique_new_fields:
        messagebox.showinfo("Auto-Detect Fields", "All detected fields already exist.")
        return

    # Append only unique fields
    fields.extend(unique_new_fields)

    draw_all_field_boxes()
    redraw_all_signatures()

    messagebox.showinfo(
        "Auto-Detect Fields",
        f"Added {len(unique_new_fields)} new fields.\n\n"
        "Changes are in memory only and will reset when a new PDF is loaded."
    )

def on_pdf_right_click(event):
    if not pages:
        return

    global identify_mode
    if not identify_mode:
        return  # only delete in identify mode

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)
    if not field:
        return

    print("CLICKED FIELD =", repr(field["name"]))

    if messagebox.askyesno("Delete Field", f"Delete field '{field['name']}'?"):
        fields.remove(field)
        #save_fields(fields)

        # ⭐ REQUIRED FIX — clear hover state
        global hover_field
        hover_field = None

        draw_all_field_boxes()
        redraw_all_signatures()

        messagebox.showinfo("Field Deleted", f"Field '{field['name']}' removed from the current session.")

 
def update_button_colors():

    if mask_edit_mode:
        btn_mask_edit.config(bg="orange")
    else:
        btn_mask_edit.config(bg=root.cget("bg"))

    if identify_mode:
        btn_identify.config(bg="lightgreen")
    else:
        btn_identify.config(bg=root.cget("bg"))

    if rename_mode:
        btn_rename.config(bg="lightgreen")
    else:
        btn_rename.config(bg=root.cget("bg"))


# ---------------- GUI SETUP ----------------

def _on_application_close():
    """Intercept the main window X and protect unsaved PDF edits."""
    try:
        root.lift()
    except tk.TclError:
        pass

    # Check the main PDF even when the Specialty window is still open.
    # Keep the confirmation tied to the main root so it cannot disappear
    # behind the application window.
    if _main_pdf_is_dirty():
        if not messagebox.askyesno(
            "Unsaved PDF Changes",
            "The Open Water PDF contains changes that have not been saved to PDF.\n\n"
            "Exit PADI Manager without saving these changes?",
            parent=root,
            default="no",
        ):
            return

    for key, check in list(_specialty_close_checks.items()):
        try:
            if not check(check_only=True):
                return
        except tk.TclError:
            _specialty_close_checks.pop(key, None)

    root.destroy()


def _write_crash_log(exc_type, exc_value, exc_tb):
    """Persist unexpected GUI errors where a macOS .app user can retrieve them."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        log_path = DATA_DIR / "crash.log"
        with log_path.open("a", encoding="utf-8") as f:
            f.write("\n" + "=" * 72 + "\n")
            f.write(f"Platform: {sys.platform}\nPython: {sys.version}\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    except Exception:
        pass
    traceback.print_exception(exc_type, exc_value, exc_tb)


def _tk_exception_handler(exc_type, exc_value, exc_tb):
    _write_crash_log(exc_type, exc_value, exc_tb)
    try:
        messagebox.showerror(
            "PADI Manager Error",
            f"An unexpected error occurred:\n\n{exc_value}\n\n"
            f"A diagnostic log was written to:\n{DATA_DIR / 'crash.log'}"
        )
    except Exception:
        pass


sys.excepthook = _write_crash_log


def show_about_dialog():
    """Display ownership, copyright, warranty and liability information."""
    about = tk.Toplevel(root)
    about.title(f"About {APP_NAME}")
    about.geometry("760x620")
    about.minsize(620, 480)
    about.transient(root)

    header = ttk.Frame(about, padding=(14, 12, 14, 6))
    header.pack(fill="x")

    ttk.Label(
        header,
        text=f"{APP_NAME} {APP_VERSION}",
        font=("Arial", 15, "bold")
    ).pack(anchor="w")

    ttk.Label(
        header,
        text="Proprietary software © 2026 Harald Steiner",
        font=("Arial", 10, "bold")
    ).pack(anchor="w", pady=(5, 0))

    ttk.Label(
        header,
        text="Contact: steinerh@telus.net"
    ).pack(anchor="w", pady=(2, 0))

    body_frame = ttk.Frame(about, padding=(14, 4, 14, 10))
    body_frame.pack(fill="both", expand=True)

    scroll = ttk.Scrollbar(body_frame, orient="vertical")
    scroll.pack(side="right", fill="y")

    body = tk.Text(
        body_frame,
        wrap="word",
        yscrollcommand=scroll.set,
        font=("Arial", 10),
        padx=10,
        pady=10,
        relief="sunken",
        borderwidth=1
    )
    body.pack(side="left", fill="both", expand=True)
    scroll.config(command=body.yview)

    notice = """PROPRIETARY SOFTWARE AND COPYRIGHT

This software is proprietary software developed and owned by Harald Steiner. All rights are reserved. The software may not be copied, modified, redistributed, sold, sublicensed, or incorporated into other software without the prior written permission of the copyright owner.

Copyright © 2026 Harald Steiner
Contact: steinerh@telus.net


DISCLAIMER AND USER RESPONSIBILITY

This software is provided for administrative assistance and convenience only. Use of this software is entirely at the user's own risk.

The user is solely responsible for reviewing and verifying all information, forms, records, dates, signatures, instructor information, certification details, and other documents created, modified, displayed, or exported using this software before relying on, submitting, signing, distributing, or retaining them.

The software is not intended to replace the user's professional judgment or responsibility to comply with applicable training standards, procedures, documentation requirements, laws, regulations, organizational policies, or other professional obligations.


NO WARRANTY

This software is provided "as is" and "as available", without warranty of any kind, express or implied, including but not limited to warranties of accuracy, completeness, reliability, availability, merchantability, fitness for a particular purpose, non-infringement, or suitability for any particular use.

No representation or warranty is made that the software will operate without interruption or error, preserve all data, correctly interpret every PDF document, or produce records suitable for every purpose.


LIMITATION OF LIABILITY

To the maximum extent permitted by applicable law, the copyright owner, developer, and any person involved in making this software available shall not be liable for any direct, indirect, incidental, consequential, special, exemplary, or other loss, damage, claim, cost, expense, data loss, documentation error, certification issue, business interruption, or other consequence arising from the installation, use, misuse, malfunction, inability to use, or reliance on this software or its output.


WILSON DIVING, VICTORIA

Wilson Diving, Victoria, British Columbia, is not the developer or owner of this software and assumes no responsibility or liability for the software, its operation, maintenance, availability, output, accuracy, use, misuse, or any consequence arising from its use.

Any use of this software in connection with Wilson Diving does not transfer responsibility for the software to Wilson Diving and does not constitute a warranty or guarantee by Wilson Diving.


PADI TRADEMARK AND INDEPENDENCE

PADI® is a registered trademark of PADI. References to PADI, PADI programs, courses, forms, or training records are used only to identify the documents and workflows with which this software may be used.

This software is independently developed and is not represented as being developed, endorsed, approved, certified, supported, or warranted by PADI unless such authorization has been separately obtained in writing.


ACCEPTANCE

By using this software, the user acknowledges that software errors and document-processing errors can occur and accepts responsibility for independently reviewing the resulting records and documents before use.
"""

    body.insert("1.0", notice)
    body.config(state="disabled")
    body.see("1.0")

    button_row = ttk.Frame(about, padding=(14, 0, 14, 12))
    button_row.pack(fill="x")

    ttk.Button(
        button_row,
        text="Close",
        command=about.destroy,
        width=12
    ).pack(side="right")


root = tk.Tk()
root.report_callback_exception = _tk_exception_handler
root.title(f"{APP_NAME} {APP_VERSION} - Specialty PDF Backdrop")
root.geometry("1200x800")
root.protocol("WM_DELETE_WINDOW", _on_application_close)

hover_info_label = tk.Label(
    root,
    text="",
    bg="lightyellow",
    relief="solid",
    borderwidth=1,
    justify="left"
)

top_frame = ttk.Frame(root)
top_frame.pack(fill="x", pady=5)
try:
    # Decode the embedded logo; no external logo.png is required.
    logo_bytes = base64.b64decode(EMBEDDED_LOGO_PNG)
    logo_img = Image.open(io.BytesIO(logo_bytes)).convert("RGBA")
    logo_img = logo_img.resize((64, 64), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(top_frame, image=logo_photo)
    logo_label.image = logo_photo   # keep reference alive for Tkinter
    logo_label.pack(side="left", padx=5)

except Exception as e:
    print("Embedded logo load failed:", e)

tk.Label(top_frame, text="Instructor:").pack(side="left", padx=5)
instructor_var = tk.StringVar()
instructor_dropdown = ttk.Combobox(
    top_frame,
    textvariable=instructor_var,
    values=[i["name"] for i in instructor_list],
    width=25
)
instructor_dropdown.pack(side="left")

tk.Button(
    top_frame,
    text="Add/Manage Instructor",
    command=add_instructor_window
).pack(side="left", padx=10)

tk.Button(
    top_frame,
    text="About",
    command=show_about_dialog,
    width=9
).pack(side="left", padx=(0, 8))


# --- Integrated Date Picker Widget ---
tk.Label(top_frame, text="Select Date:").pack(side="left", padx=(15, 2))


date_picker = StableDatePicker(
    top_frame,
    width=12,
    date_pattern="yyyy-mm-dd"
)
date_picker.set_date(date.today())
date_picker.pack(side="left", padx=5)
date_picker.bind("<<DateEntrySelected>>", on_date_changed)

instructor_info = tk.Label(top_frame, text="No instructor selected", anchor="w", justify="left")
instructor_info.pack(side="left", padx=20)

instructor_var.trace_add("write", update_instructor_info)


mid_frame = ttk.Frame(root)
mid_frame.pack(fill="x", pady=5)

tk.Button(mid_frame, text="Load PDF", command=load_pdf).pack(side="left", padx=5)
pdf_label = tk.Label(mid_frame, text="No PDF loaded")

pdf_label.pack(side="left", padx=10)

# Specialty worksheet workflow (separate from the Open Water AcroForm editor).
# Keep the selected specialty in a hidden variable for compatibility with the
# specialty window and saved worksheet state.  The user-facing specialty
# dropdown exists ONLY inside open_specialty_worksheet().
specialty_var = tk.StringVar(value=SPECIALTY_NAMES[0])
tk.Button(
    mid_frame,
    text="Specialty Worksheet",
    command=open_specialty_worksheet
).pack(side="left", padx=(8, 8))

tk.Button(mid_frame, text="Prev Page", command=prev_page).pack(side="left", padx=5)
tk.Button(mid_frame, text="Next Page", command=next_page).pack(side="left", padx=5)

tk.Button(mid_frame, text="Zoom +", command=zoom_in).pack(side="left", padx=5)
tk.Button(mid_frame, text="Zoom -", command=zoom_out).pack(side="left", padx=5)
tk.Button(mid_frame, text="Fit Page", command=zoom_fit).pack(side="left", padx=5)


tk.Button(
    mid_frame,
    text="Save/Update PDF",
    command=export_pdf
).pack(side="left", padx=5)

# Signature export mode. Default is OFF so signatures stay in the app state
# and are not permanently merged into the PDF page artwork.
burn_signature_var = tk.BooleanVar(value=False)
burn_signature_check = tk.Checkbutton(
    mid_frame,
    text="Burn signatures into PDF",
    variable=burn_signature_var,
    onvalue=True,
    offvalue=False
)
burn_signature_check.pack(side="left", padx=(6, 4))

# ------------------------------------------------------------
# Main-menu comment box
# ------------------------------------------------------------
# No separate Comment button/window.  The textbox is always visible
# beside Save/Update PDF and reads/writes comments.json.
comment_frame = tk.Frame(mid_frame)
comment_frame.pack(
    side="left",
    padx=(6, 10),
    pady=0,
    fill="y"
)

comment_text = tk.Text(
    comment_frame,
    width=34,
    height=2,
    wrap="word",
    undo=True,
    font=("Arial", 9)
)

comment_scrollbar = tk.Scrollbar(
    comment_frame,
    orient="vertical",
    command=comment_text.yview
)

comment_text.configure(
    yscrollcommand=comment_scrollbar.set
)

comment_text.pack(
    side="left",
    fill="both",
    expand=True
)

comment_scrollbar.pack(
    side="right",
    fill="y"
)

def update_comment_box_color(event=None):
    content = comment_text.get("1.0", "end-1c").strip()

    if content:
        comment_text.configure(bg="orange")
    else:
        comment_text.configure(bg="white")

comment_text.bind("<KeyRelease>", update_comment_box_color)

# Set initial color
update_comment_box_color()





status_label = tk.Label(root, text="Mask Edit Mode: OFF")
status_label.pack(pady=5)

#
# Main area = PDF viewer + right tools panel
#
main_view_frame = tk.Frame(root)
main_view_frame.pack(fill="both", expand=True)

#
# PDF Viewer Area
#
pdf_frame = tk.Frame(main_view_frame)
pdf_frame.pack(side="left", fill="both", expand=True)

#
# Right Tools Panel
#
tools_frame = tk.Frame(
    main_view_frame,
    width=110,
    relief="groove",
    bd=2
)

tools_frame.pack(
    side="right",
    fill="y",
    padx=5,
    pady=5
)
weite=10
tools_frame.pack_propagate(False)

# Legend for clickable fields that trigger multiple automatic updates.
action_legend = tk.Label(
    tools_frame,
    text="Orange dashed =\nauto-fill/action",
    fg="darkorange",
    justify="center",
    wraplength=100
)
action_legend.pack(fill="x", pady=(2, 6))

btn_mask_edit = tk.Button(
    tools_frame,
    text="Toggle Mask Edit",
    command=toggle_mask_edit,
    width=weite
)

btn_identify = tk.Button(
    tools_frame,
    text="Identify Field",
    command=toggle_identify_mode,
    width=weite
)

btn_rename = tk.Button(
    tools_frame,
    text="Rename Field",
    command=toggle_rename_mode,
    width=weite
)

btn_close_pdf = tk.Button(
    tools_frame,
    text="Close PDF",
    command=close_pdf,
    width=weite
)

#
# Right-side tool buttons
#
btn_mask_edit.pack(
    fill="x",
    pady=2
)

btn_identify.pack(
    fill="x",
    pady=2
)

btn_rename.pack(
    fill="x",
    pady=2
)

tk.Button(
    tools_frame,
    text="Auto-Detect Fields",
    command=auto_detect_fields
).pack(
    fill="x",
    pady=2
)





btn_close_pdf.pack(
    fill="x",
    pady=2
)

tk.Button(
    tools_frame,
    text="Field Logic 10056",
    command=show_program_fields
).pack(
    fill="x",
    pady=2
)

update_button_colors()
update_button_colors()

v_scroll = tk.Scrollbar(pdf_frame, orient="vertical")
h_scroll = tk.Scrollbar(pdf_frame, orient="horizontal")

canvas_pdf = tk.Canvas(
    pdf_frame,
    bg="grey",
    width=900,
    height=600,
    scrollregion=(0, 0, 2000, 2000),
    yscrollcommand=v_scroll.set,
    xscrollcommand=h_scroll.set
)
canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal, add="+")
if IS_MACOS:
    canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal, add="+")

canvas_pdf.focus_set()

v_scroll.config(command=canvas_pdf.yview)
h_scroll.config(command=canvas_pdf.xview)

v_scroll.pack(side="right", fill="y")
h_scroll.pack(side="bottom", fill="x")
canvas_pdf.pack(side="left", fill="both", expand=True)

def _on_mousewheel(event):
    """Cross-platform wheel/trackpad scrolling."""
    delta = getattr(event, "delta", 0)
    if not delta:
        return
    if IS_MACOS:
        # macOS Tk reports small, high-resolution trackpad deltas.
        units = -1 if delta > 0 else 1
    else:
        units = int(-delta / 120)
        if units == 0:
            units = -1 if delta > 0 else 1
    canvas_pdf.yview_scroll(units, "units")

canvas_pdf.bind("<Button-1>", on_pdf_click)
canvas_pdf.bind("<Motion>", on_pdf_motion)
canvas_pdf.bind("<Leave>", on_pdf_leave)
canvas_pdf.bind("<MouseWheel>", _on_mousewheel)
# Linux/X11 fallback; harmless for source runs outside macOS/Windows.
canvas_pdf.bind("<Button-4>", lambda e: canvas_pdf.yview_scroll(-1, "units"))
canvas_pdf.bind("<Button-5>", lambda e: canvas_pdf.yview_scroll(1, "units"))



def bind_mask_edit_events():
    # LEFT CLICK = create field
    canvas_pdf.bind("<ButtonPress-1>", on_mask_left_press)
    canvas_pdf.bind("<ButtonRelease-1>", on_mask_left_release)

    # RIGHT CLICK = delete field
    canvas_pdf.bind("<Button-3>", on_mask_right_click)
    if IS_MACOS:
        canvas_pdf.bind("<Control-Button-1>", on_mask_right_click)


def unbind_mask_edit_events():
    canvas_pdf.unbind("<ButtonPress-1>")
    canvas_pdf.unbind("<ButtonRelease-1>")
    canvas_pdf.unbind("<Button-3>")

    canvas_pdf.bind("<Button-1>", on_pdf_click)
    canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal)
    if IS_MACOS:
        canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal)

# ---------------- Mask Edit: LEFT CLICK = Create Field ----------------

def on_mask_left_press(event):
    global drag_start
    if not mask_edit_mode or not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)
    drag_start = (canvas_x, canvas_y)


def on_mask_left_release(event):
    global drag_start
    if not mask_edit_mode or not pages or drag_start is None:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    x1_canvas, y1_canvas = drag_start
    x2_canvas, y2_canvas = canvas_x, canvas_y

    # Ignore tiny drags
    if abs(x2_canvas - x1_canvas) < 5 or abs(y2_canvas - y1_canvas) < 5:
        drag_start = None
        return

    x1 = int(min(x1_canvas, x2_canvas) / zoom_level)
    y1 = int(min(y1_canvas, y2_canvas) / zoom_level)
    x2 = int(max(x1_canvas, x2_canvas) / zoom_level)
    y2 = int(max(y1_canvas, y2_canvas) / zoom_level)

    new_field = {
        "name": f"field_{len(fields)+1}",
        "type": "text",
        "page": current_page,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    }

    fields.append(new_field)
    draw_all_field_boxes()
    messagebox.showinfo("Field Created", f"New field created:\n{new_field['name']}")

    drag_start = None


# ---------------- Mask Edit: RIGHT CLICK = Delete Field ----------------

def on_mask_right_click(event):
    if not mask_edit_mode or not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)
    if not field:
        return

    if messagebox.askyesno("Delete Field", f"Delete field '{field['name']}'?"):
        fields.remove(field)
        draw_all_field_boxes()
        redraw_all_signatures()



canvas_pdf.bind("<ButtonPress-2>", on_pdf_button_press)
canvas_pdf.bind("<ButtonRelease-2>", on_pdf_button_release)

canvas_pdf.bind("<B3-Motion>", lambda e: None)
canvas_pdf.bind("<B2-Motion>", lambda e: None)

widget_frame = ttk.Frame(root)
widget_frame.pack(fill="x", pady=5)

if __name__ == "__main__":
    # Delay first render so canvas dimensions are correct
    # Only render after Tk finishes drawing the window
    root.after(200, lambda: render_page() if pages else None)
    root.mainloop()

