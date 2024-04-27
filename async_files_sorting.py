from argparse import ArgumentParser
from aiopath import AsyncPath
from aioshutil import copyfile
import logging

logging.basicConfig(filename='file_sorting.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

async def read_folder(input_dir):
    async for file in input_dir.iterdir():
        if await file.is_file():
            print(f'Found file: {file.name}')
            yield file

async def copy_file(file, output_dir):
    subfolder_name = file.suffix[1:]
    subfolder = output_dir / subfolder_name
    await subfolder.mkdir(exist_ok=True)
    destination = subfolder / file.name
    await copyfile(file, destination)


async def main(input_dir, output_dir):
    async for file in read_folder(input_dir):
        await copy_file(file, output_dir)       

if __name__ == '__main__':
    import asyncio
    args_parser = ArgumentParser(description='Sort files in a directory by their extension')

    args_parser.add_argument('input', type=str, help='Path to the directory with files')
    args_parser.add_argument('output', type=str, help='Path to the directory where files will be sorted')

    input_dir = AsyncPath(args_parser.parse_args().input)
    output_dir = AsyncPath(args_parser.parse_args().output)
    asyncio.run(main(input_dir, output_dir))