import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from nb_cli_plugin_webui.app.logging import LoguruHandler

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(30)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())
