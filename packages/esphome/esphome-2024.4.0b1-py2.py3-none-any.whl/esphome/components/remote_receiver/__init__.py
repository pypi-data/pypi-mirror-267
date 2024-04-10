import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import remote_base, esp32_rmt
from esphome.const import (
    CONF_BUFFER_SIZE,
    CONF_DUMP,
    CONF_FILTER,
    CONF_ID,
    CONF_IDLE,
    CONF_PIN,
    CONF_TOLERANCE,
    CONF_MEMORY_BLOCKS,
    CONF_RMT_CHANNEL,
)
from esphome.core import CORE, TimePeriod

AUTO_LOAD = ["remote_base"]
remote_receiver_ns = cg.esphome_ns.namespace("remote_receiver")
RemoteReceiverComponent = remote_receiver_ns.class_(
    "RemoteReceiverComponent", remote_base.RemoteReceiverBase, cg.Component
)

MULTI_CONF = True
CONFIG_SCHEMA = remote_base.validate_triggers(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(RemoteReceiverComponent),
            cv.Required(CONF_PIN): cv.All(pins.internal_gpio_input_pin_schema),
            cv.Optional(CONF_DUMP, default=[]): remote_base.validate_dumpers,
            cv.Optional(CONF_TOLERANCE, default=25): cv.All(
                cv.percentage_int, cv.Range(min=0)
            ),
            cv.SplitDefault(
                CONF_BUFFER_SIZE,
                esp32="10000b",
                esp8266="1000b",
                bk72xx="1000b",
                rtl87xx="1000b",
            ): cv.validate_bytes,
            cv.Optional(CONF_FILTER, default="50us"): cv.All(
                cv.positive_time_period_microseconds,
                cv.Range(max=TimePeriod(microseconds=255)),
            ),
            cv.Optional(
                CONF_IDLE, default="10ms"
            ): cv.positive_time_period_microseconds,
            cv.Optional(CONF_MEMORY_BLOCKS, default=3): cv.Range(min=1, max=8),
            cv.Optional(CONF_RMT_CHANNEL): esp32_rmt.validate_rmt_channel(tx=False),
        }
    ).extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    if CORE.is_esp32:
        if (rmt_channel := config.get(CONF_RMT_CHANNEL, None)) is not None:
            var = cg.new_Pvariable(
                config[CONF_ID], pin, rmt_channel, config[CONF_MEMORY_BLOCKS]
            )
        else:
            var = cg.new_Pvariable(config[CONF_ID], pin, config[CONF_MEMORY_BLOCKS])
    else:
        var = cg.new_Pvariable(config[CONF_ID], pin)

    dumpers = await remote_base.build_dumpers(config[CONF_DUMP])
    for dumper in dumpers:
        cg.add(var.register_dumper(dumper))

    triggers = await remote_base.build_triggers(config)
    for trigger in triggers:
        cg.add(var.register_listener(trigger))
    await cg.register_component(var, config)

    cg.add(var.set_tolerance(config[CONF_TOLERANCE]))
    cg.add(var.set_buffer_size(config[CONF_BUFFER_SIZE]))
    cg.add(var.set_filter_us(config[CONF_FILTER]))
    cg.add(var.set_idle_us(config[CONF_IDLE]))
