# Electrostatic Detection

Arduino Nano electrostatic sensing projects authored in Mixly. This repository
contains project sources rather than a portable Mixly distribution.

## Sources

| File | Purpose |
| --- | --- |
| `src/standalone/electrostatic-detection.mix` | Standalone sensing and OLED display |
| `src/standalone/electrostatic-detection.mil` | Companion Mixly XML library/workspace |
| `src/generation-2/transmitter.mix` | Dual analog sensing and NEC infrared transmission |
| `src/generation-2/receiver.mix` | Infrared reception, OLED display, clock, temperature, and humidity |

The MIX files declare format 1.2.0 and Arduino Nano with the old ATmega328
bootloader. The MIL file is XML, not a ZIP archive, and preserves an older
workspace variant rather than duplicating the standalone MIX file. English
variable and procedure names are consistent across files. Block types, IDs,
pins, numeric constants, and protocol values are preserved. MIX files retain
their escaped XML serialization; MIL retains ordinary XML and its library marker.

## External dependencies

Install [Mixly](https://github.com/mixly/Mixly_Arduino) and Arduino AVR board
support outside this repository. Select Arduino Nano / ATmega328P (Old Bootloader).
Use a Mixly release supporting the existing block names and review imported
blocks before generating code. No external packages are vendored here.

The retained block generators require:

- [U8g2](https://github.com/olikraus/u8g2): `U8g2lib.h`, SSD1306 128x64 OLED support.
- [DHT sensor library](https://github.com/adafruit/DHT-sensor-library): `DHT.h` for DHT11; install its declared dependencies too.
- [Rtc by Makuna](https://github.com/Makuna/Rtc): `RtcDS1302.h` and `ThreeWire.h`.
- [Arduino-IRremote](https://github.com/Arduino-IRremote/Arduino-IRremote): a legacy API compatible with Mixly's `ir_recv` and `ir_send_nec` generators. The latest API may require migration.
- Arduino AVR core and its Wire library.

Open the appropriate MIX source in Mixly. Import the MIL companion through
Mixly's library workflow if needed. Review the generated code and physical
circuit before uploading. Display workspaces use DHT11 on pin 2 and DS1302
RST/DAT/CLK on pins 5/4/3. The receiver uses infrared input on pin 12. Consult
each workspace for all other assignments, including its explicit software I2C
configuration. The infrared workspaces preserve NEC and the offset `33333333`.

These are preserved experimental sources. This repository provides no wiring
schematic, calibrated measurement accuracy, hardware safety assessment, or
hardware test results.

## Offline validation

Run `python -m unittest discover -s tests -q` with Python 3. Checks decode the
four XML workspaces, verify English names and procedure references, and inspect
board and protocol markers. They do not execute firmware, run Mixly, download
tools, or contact hardware. Compilation and device behavior still require a
compatible external Mixly environment and suitable hardware.

## Scope and license

Competition submissions, personal appendices, presentations, demonstration media,
updaters, unrelated experiments, and bundled SDK/vendor tools are excluded from
the maintained tree. The old distribution changelog described Mixly releases,
not this project, and was removed. Git history is preserved; this cleanup does
not erase earlier content from history.

The original Apache License 2.0 text is retained in [LICENSE](LICENSE). Mixly,
Blockly, Arduino, and external libraries retain their respective authors and
licenses. Repository organization and maintenance: frostmoon-rui.
