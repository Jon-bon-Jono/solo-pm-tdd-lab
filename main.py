import logging
from solo_pm_tdd_lab.core import clamp, rolling_mean, zscore
from solo_pm_tdd_lab.logging_utils import setup_logging
from functools import partial

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting program")
    data = [1,2,3,4,5,6,7,8,9,10]
    logger.debug("data=%s", data)
    
    clamp_partial = partial(clamp, lo=2, hi=8)
    logger.info("Clamping data")
    data_cleaned = list(map(clamp_partial, data))
    logger.debug("data_cleaned=%s", data_cleaned)
    
    clamp_partial_broken = partial(clamp, lo=8, hi=2)
    data_cleaned_broken = []
    try:
        data_cleaned_broken = list(map(clamp_partial_broken, data))
    except Exception:
        logger.exception("clamp failed")
    
    logger.info("Computing rolling mean of clamped data")
    data_rm = rolling_mean(data_cleaned, window_size=2)
    
    logger.info("Finished")


if __name__ == "__main__":
    setup_logging(debug=True)
    main()