# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import scraping.nips
import msacademic
import pandas as pd
from multiprocessing import Pool


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('downloading data')
    papers = make_nips()
    
def make_nips():
    logger = logging.getLogger(__name__)
    downloaded = []
    logger.info('scraping years')
    years = scraping.nips.getYears()
    yearsf = filter(lambda x: x[-4:] < 2013, years)
    for year in yearsf:
        year_numb = year[-4:]
        logger.info('scraping: ' + str(year_numb))
        papers = scraping.nips.getPapers(year)
        downloaded = None
        with Pool(5) as p:
            downloaded = p.map( msacademic.parsePaper, list(zip(papers,list(range(0,len(papers))))))
        logger.info('making final data set from raw nips '+ str(year_numb))
        df = pd.DataFrame(downloaded)
        df.to_csv("data/raw/nips_" + str(year_numb) + ".csv")
            
            
    logger.info('finished downloading dataset')
    return downloaded


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
