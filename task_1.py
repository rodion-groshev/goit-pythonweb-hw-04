from argparse import ArgumentParser
from aiopath import Path, AsyncPath
from aioshutil import copyfile
import asyncio
import logging
import shutil

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)

parser = ArgumentParser()
parser.add_argument("--source")
parser.add_argument("--output")
args = parser.parse_args()
path_source = Path(args.source)
path_output = Path(args.output)


async def read_folder(source, output):
    async for item in source.iterdir():
        if await item.is_dir():
            await read_folder(item, output)
        elif await item.is_file():
            await copy_file(item, output)


async def copy_file(file, output):
    str_file = str(file).split("\\")[-1]
    extension = str(file).split(".")[1]
    new_path = AsyncPath(f"{output}/{extension}")
    if await file.exists():
        await new_path.mkdir(exist_ok=True, parents=True)
        try:
            await copyfile(file, new_path / str_file)
            logger.info(f"File: {file} copied to {new_path}")
        except shutil.SameFileError:
            logger.error(f"This file {str_file} already copied")


if __name__ == '__main__':
    asyncio.run(read_folder(path_source, path_output))
    logger.info("End of the program")
