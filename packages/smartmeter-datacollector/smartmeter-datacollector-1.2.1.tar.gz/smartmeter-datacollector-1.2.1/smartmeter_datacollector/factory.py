#
# Copyright (C) 2024 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
import logging
from configparser import ConfigParser
from typing import List

from .collector import Collector
from .config import InvalidConfigError
from .sinks.data_sink import DataSink
from .sinks.logger_sink import LoggerSink
from .sinks.mqtt_sink import MqttConfig, MqttDataSink
from .smartmeter.iskraam550 import IskraAM550
from .smartmeter.kamstrup_han import KamstrupHAN
from .smartmeter.lge360 import LGE360
from .smartmeter.lge450 import LGE450
from .smartmeter.lge570 import LGE570
from .smartmeter.meter import Meter, MeterError


def build_meters(config: ConfigParser) -> List[Meter]:
    meters = []
    for section_name in filter(lambda sec: sec.startswith("reader"), config.sections()):
        meter_config = config[section_name]
        meter_type = meter_config.get('type')
        try:
            if meter_type == "lge450":
                meters.append(LGE450(
                    port=meter_config.get('port', "/dev/ttyUSB0"),
                    baudrate=meter_config.getint('baudrate', LGE450.BAUDRATE),
                    decryption_key=meter_config.get('key'),
                    use_system_time=meter_config.getboolean('systemtime', False)
                ))
            elif meter_type == "lge570":
                meters.append(LGE570(
                    port=meter_config.get('port', "/dev/ttyUSB0"),
                    baudrate=meter_config.getint('baudrate', LGE570.BAUDRATE),
                    decryption_key=meter_config.get('key'),
                    use_system_time=meter_config.getboolean('systemtime', False)
                ))
            elif meter_type == "lge360":
                meters.append(LGE360(
                    port=meter_config.get('port', "/dev/ttyUSB0"),
                    baudrate=meter_config.getint('baudrate', LGE360.BAUDRATE),
                    decryption_key=meter_config.get('key'),
                    use_system_time=meter_config.getboolean('systemtime', False)
                ))
            elif meter_type == "iskraam550":
                meters.append(IskraAM550(
                    port=meter_config.get('port', "/dev/ttyUSB0"),
                    baudrate=meter_config.getint('baudrate', IskraAM550.BAUDRATE),
                    decryption_key=meter_config.get('key'),
                    use_system_time=meter_config.getboolean('systemtime', False)
                ))
            elif meter_type == "kamstrup_han":
                meters.append(KamstrupHAN(
                    port=meter_config.get('port', "/dev/ttyUSB0"),
                    baudrate=meter_config.getint('baudrate', KamstrupHAN.BAUDRATE),
                    decryption_key=meter_config.get('key'),
                    use_system_time=meter_config.getboolean('systemtime', False)
                ))
            else:
                raise InvalidConfigError(f"'type' is invalid or missing: {meter_type}")
        except MeterError as ex:
            logging.warning("%s Skipping smart meter.", ex)
            continue
    return meters


def build_sinks(config: ConfigParser) -> List[DataSink]:
    sinks = []
    for section_name in filter(lambda sec: sec.startswith("sink"), config.sections()):
        sink_config = config[section_name]
        sink_type = sink_config.get('type')

        if sink_type == "logger":
            sinks.append(LoggerSink(
                logger_name=sink_config.get('name', "DataLogger")
            ))
        elif sink_type == "mqtt":
            mqtt_config = MqttConfig.from_sink_config(sink_config)
            sinks.append(MqttDataSink(mqtt_config))
        else:
            raise InvalidConfigError(f"'type' is invalid or missing: {sink_type}")
    return sinks


def build_collector(readers: List[Meter], sinks: List[DataSink]) -> Collector:
    collector = Collector()

    for sink in sinks:
        collector.register_sink(sink)
    for reader in readers:
        reader.register(collector)
    return collector
