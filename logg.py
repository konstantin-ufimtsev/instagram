import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='[%d.%m.%Y-%H:%M:%S]',
    level=logging.INFO,
    filename="log.log",
    filemode='a',
    encoding='utf-8'
    )

