from pyconfig_extension import IConfigurationSection, IConfiguration
from pyserilog import LoggerConfiguration
from pyserilog.configuration.logger_settings_configuration import LoggerSettingsConfiguration

from pyserilog_settings_configuration.settings.configuration_reader import ConfigurationReader
from pyserilog_settings_configuration.settings.configuration_reader_options import ConfigurationReaderOptions


def configure_from_setting(setting_configuration: LoggerSettingsConfiguration,
                           conf: IConfiguration,
                           option: ConfigurationReaderOptions = None
                           ) -> LoggerConfiguration:
    if option is None:
        option = ConfigurationReaderOptions()
    if option is not None and option.section_name is not None and len(option.section_name) > 0:
        serilog_section = conf.get_section(option.section_name)
    else:
        serilog_section = conf

    setting_configuration.settings(ConfigurationReader(serilog_section, conf))
