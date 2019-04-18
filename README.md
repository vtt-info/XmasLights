# XmasLights
This project implements some Christmas Lights in MicroPython on an ESP32 and a NeoPixel RGB Strip of 240 LEDs.

## Hardware
### Parts List
[ESP32 Board](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/overview)  
Adafruit HUZZAH32 ESP32 Feather board

[NeoPixel Strip](https://www.adafruit.com/product/1138?length=4)  
4 metre NeoPixel RGB LED Strip with 60 LED's per metre

[Level Shifter](https://www.adafruit.com/product/757)  
Bi-Directional Level Shifter

## Software
### Light Patterns
#### RainbowTrain
#### SolidColour
#### SolidColourSlide
#### AlternateColour
#### SideFill
#### RandomFill
#### MiddleFill
#### MountainCarChase
#### BouncyBalls
#### BackwardsSlidingStripes
#### FireSparks
#### RandomColourTrain
#### RandomColourStrips
#### GreenSparks
#### RedWithGreenSparks
#### SnowSparkles
#### PurplePinkSparkles


```python
np = neopixel.NeoPixel(machine.Pin(13), PIXELS)
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
