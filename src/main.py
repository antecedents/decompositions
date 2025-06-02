"""Module main.py"""
import logging
import os
import sys


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Data
    data, codes = src.data.interface.Interface(
        s3_parameters=s3_parameters, arguments=arguments).exc()

    # Modelling
    messages = src.modelling.interface.Interface(
      data=data, arguments=arguments).exc(codes=codes)
    logger.info(messages)

    # Transfer
    src.transfer.interface.Interface(
       connector=connector, service=service, s3_parameters=s3_parameters).exc()

    # Cache
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.data.interface
    import src.functions.cache
    import src.modelling.interface
    import src.preface.interface
    import src.transfer.interface

    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()
