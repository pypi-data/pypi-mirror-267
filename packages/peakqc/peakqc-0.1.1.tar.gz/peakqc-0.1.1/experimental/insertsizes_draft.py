""" Count insertsizes"""
# Author: Jan Detleffsen

# Imports
import pandas as pd
import numpy as np
import gzip
import datetime
from multiprocessing import Manager, Lock, Pool
from tqdm import tqdm

import peakqc.general as utils


from beartype import beartype
import numpy.typing as npt
from beartype.typing import Any, Optional

@beartype
def _is_gz_file(filepath: str) -> bool:
    """
    Check wheather file is a compressed .gz file.

    Parameters
    ----------
    filepath : str
        Path to file.

    Returns
    -------
    bool
        True if the file is a compressed .gz file.
    """

    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'


@beartype
def init_pool_processes(the_lock: Any) -> None:
    '''
    Initialize each process with a global variable lock.

    Parameters
    ----------
    the_lock : Any
        Lock object to be used by the processes.

    Returns
    -------
    None
    '''
    global lock
    lock = the_lock


@beartype
def _check_in_list(element: Any, alist: list[Any] | set[Any]) -> bool:
    """
    Check if element is in list.

    Parameters
    ----------
    element : Any
        Element that is checked for.
    alist : list[Any] | set[Any]
        List or set in which the element is searched for.

    Returns
    -------
    bool
        True if element is in list else False
    """

    return element in alist


@beartype
def _check_true(element: Any, alist: Optional[list[Any]] = None) -> bool:  # true regardless of input
    """
    Return True regardless of input

    Parameters
    ----------
    element : Any
        Element that is checked for.
    alist: Optional[list[Any]]
        List or set in which the element is searched for.

    Returns
    -------
    bool
        True if element is in list else False
    """

    return True


@beartype
def _custom_callback(error: Exception) -> None:
    """
    Error callback function for multiprocessing.

    Parameters
    ----------
    error : Exception
        Error that is raised.

    Returns
    -------
    None
    """
    print(error, flush=True)


@beartype
def insertsize_from_fragments(fragments: str,
                              barcodes: Optional[list[str]] = None,
                              n_threads: int = 8) -> pd.DataFrame:
    """
    Count the insertsizes of fragments in a fragments file and get basic statistics (mean and total count) per barcode.

    Parameters
    ----------
    fragments : str
        Path to fragments file.
    barcodes : list[str], optional
        List of barcodes to count. If None, all barcodes are counted.
    n_threads : int, default 8
        Number of threads to use for multiprocessing.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the mean insertsizes and total counts per barcode.
    """
    print('Count insertsizes from fragments...')
    # Open fragments file
    if _is_gz_file(fragments):
        f = gzip.open(fragments, "rt")
    else:
        f = open(fragments, "r")

    # Prepare function for checking against barcodes list
    if barcodes is not None:
        barcodes = set(barcodes)
        check_in = _check_in_list
    else:
        check_in = _check_true

    # Initialize iterator
    iterator = pd.read_csv(fragments,
                           delimiter='\t',
                           header=None,
                           names=['chr', 'start', 'stop', 'barcode', 'count'],
                           iterator=True,
                           chunksize=5000000)

    # start timer
    start_time = datetime.datetime.now()

    # Initialize multiprocessing
    m = Manager() # initialize manager
    lock = Lock() # initialize lock
    managed_dict = m.dict() # initialize managed dict
    managed_dict['output'] = {}
    # initialize pool
    pool = Pool(processes=n_threads,
                initializer=init_pool_processes,
                initargs=(lock,),
                maxtasksperchild=48)
    jobs = []
    print('Starting counting fragments...')
    # split fragments into chunks
    for chunk in tqdm(iterator, desc="Processing Chunks"):
        # apply async job wit callback function
        job = pool.apply_async(_count_fragments_worker,
                               args=(chunk, barcodes, check_in, managed_dict),
                               error_callback=_custom_callback)
        jobs.append(job)

    # close pool
    pool.close()
    # wait for all jobs to finish
    pool.join()
    # reset settings
    count_dict = managed_dict['output']

    # Close file and print elapsed time
    end_time = datetime.datetime.now()
    f.close()
    elapsed = end_time - start_time
    print("Done reading file - elapsed time: {0}".format(str(elapsed).split(".")[0]))

    # Convert dict to pandas dataframe
    print("Converting counts to dataframe...")
    table = pd.DataFrame.from_dict(count_dict, orient="index")
    # round mean_insertsize to 2 decimals
    table["mean_insertsize"] = table["mean_insertsize"].round(2)

    print("Done getting insertsizes from fragments!")

    return table


def _count_fragments_worker(chunk: pd.DataFrame,
                            barcodes: Optional[list[str]] = None,
                            check_in: Any = _check_true,
                            managed_dict: dict = {'output': {}}) -> None:
    """
    Worker function for counting fragments.

    Parameters
    ----------
    chunk : pd.DataFrame
        Chunk of fragments file.
    barcodes : list[str], optional
        List of barcodes to count. If None, all barcodes are counted.
    check_in : Any, default _check_true
        Function for checking if barcode is in barcodes list.
    managed_dict : dict, default None
        Dictionary for multiprocessing.

    Returns
    -------
    None

    """

    # Initialize count_dict
    count_dict = {}
    # Iterate over chunk
    for row in chunk.itertuples():
        start = int(row[2])
        end = int(row[3])
        barcode = row[4]
        count = int(row[5])
        size = end - start - 9  # length of insertion (-9 due to to shifted cutting of Tn5)

        # Only add fragment if check is true
        if check_in(barcode, barcodes) is True:
            count_dict = _add_fragment(count_dict, barcode, size, count) # add fragment to count_dict

    # Update managed_dict
    lock.acquire() # acquire lock
    latest = managed_dict['output']
    managed_dict['output'] = _update_count_dict(latest, count_dict) # update managed dict
    lock.release() # release lock


@beartype
def _add_fragment(count_dict: dict[str, int],
                  barcode: str,
                  size: int,
                  count: int = 1,
                  max_size: int=1000) -> dict:
    """
    Add fragment of size 'size' to count_dict.

    Parameters
    ----------
    count_dict : dict[str, int]
        Dictionary containing the counts per insertsize.
    barcode : str
        Barcode of the read.
    size : int
        Insertsize to add to count_dict.
    count : int, default 1
        Number of reads to add to count_dict.

    Returns
    -------
    dict
        Updated count_dict.
    """

    # Initialize if barcode is seen for the first time
    if barcode not in count_dict:
        count_dict[barcode] = {"mean_insertsize": 0, "insertsize_count": 0}

    # Add read to dict
    if size > 0 and size <= max_size:  # do not save negative insertsize, and set a cap on the maximum insertsize to limit outlier effects

        count_dict[barcode]["insertsize_count"] += count

        # Update mean
        mu = count_dict[barcode]["mean_insertsize"]
        total_count = count_dict[barcode]["insertsize_count"]
        diff = (size - mu) / total_count
        count_dict[barcode]["mean_insertsize"] = mu + diff

        # Save to distribution
        if 'dist' not in count_dict[barcode]:  # initialize distribution
            count_dict[barcode]['dist'] = np.zeros(max_size + 1)
        count_dict[barcode]['dist'][size] += count # add count to distribution

    return count_dict


@beartype
def _update_count_dict(count_dict_1: dict, count_dict_2: dict) -> dict:
    """
    Updates the managed dict with the new counts.

    Parameters
    ----------
    count_dict_1 : dict
        Dictionary containing the counts per insertsize.
    count_dict_2 : dict
        Dictionary containing the counts per insertsize.

    Returns
    -------
    dict
        Updated count_dict.
    """
    # Check if count_dict_1 is empty:
    if len(count_dict_1) == 0:
        return count_dict_2

    # make Dataframes for computation
    df1 = pd.DataFrame(count_dict_1).T
    df2 = pd.DataFrame(count_dict_2).T

    # merge distributions
    combined_dists = df1['dist'].combine(df2['dist'], func=_update_dist)
    # merge counts
    merged_counts = pd.merge(df1["insertsize_count"], df2["insertsize_count"], left_index=True, right_index=True,
                             how='outer').fillna(0)
    # sum total counts/barcode
    updated_counts = merged_counts.sum(axis=1)

    # calculate scaling factors
    x_scaling_factor = merged_counts["insertsize_count_x"] / updated_counts
    y_scaling_factor = merged_counts["insertsize_count_y"] / updated_counts

    # merge mean insertsizes
    merged_mean_insertsizes = pd.merge(df1["mean_insertsize"], df2["mean_insertsize"], left_index=True,
                                       right_index=True, how='outer').fillna(0)

    # scale mean insertsizes
    merged_mean_insertsizes["mean_insertsize_x"] = merged_mean_insertsizes["mean_insertsize_x"] * x_scaling_factor
    merged_mean_insertsizes["mean_insertsize_y"] = merged_mean_insertsizes["mean_insertsize_y"] * y_scaling_factor

    # sum the scaled means
    updated_means = merged_mean_insertsizes.sum(axis=1)

    # build the updated dictionary
    updated_dict = pd.DataFrame(
        {'mean_insertsize': updated_means, 'insertsize_count': updated_counts, 'dist': combined_dists}).T.to_dict()

    return updated_dict


@beartype
def _update_dist(dist_1: npt.ArrayLike, dist_2: npt.ArrayLike) -> npt.ArrayLike:
    """
    Updates the Insertsize Distributions.

    Parameters
    ----------
    dist_1 : npt.ArrayLike
        Insertsize distribution 1.
    dist_2 : npt.ArrayLike
        Insertsize distribution 2.

    Returns
    -------
    npt.ArrayLike
        Updated insertsize distribution.
    """
    # check if both distributions are not empty
    if not np.isnan(dist_1).any() and not np.isnan(dist_2).any():
        updated_dist = dist_1 + dist_2 # add distributions
        return updated_dist.astype(int)
    # if one of the distributions is empty, return the other one
    elif np.isnan(dist_1).any():
        return dist_2.astype(int)
    elif np.isnan(dist_2).any():
        return dist_1.astype(int)


start_run = time.time()

regions = None
bam = bamfile
chunk_size = 100000
n_threads = 10
barcode_tag = 'CB'

utils.check_module("pysam")
import pysam

if isinstance(regions, str):
    regions = [regions]

# Prepare function for checking against barcodes list
if barcodes is not None:
    barcodes = set(barcodes)
    check_in = _check_in_list
else:
    check_in = _check_true

# Open bamfile
print("Opening bam file...")
if not os.path.exists(bam + ".bai"):
    print("Bamfile has no index - trying to index with pysam...")
    pysam.index(bam)

bam_obj = open_bam(bam, "rb", require_index=True)
chromosome_lengths = dict(zip(bam_obj.references, bam_obj.lengths))

# Create chunked genome regions:
print(f"Creating chunks of size {chunk_size}bp...")

if regions is None:
    regions = [f"{chrom}:0-{length}" for chrom, length in chromosome_lengths.items()]
elif isinstance(regions, str):
    regions = [regions]

# Create chunks from larger regions
regions_split = []
for region in regions:
    chromosome, start, end = re.split("[:-]", region)
    start = int(start)
    end = int(end)
    for chunk_start in range(start, end, chunk_size):
        chunk_end = chunk_start + chunk_size
        if chunk_end > end:
            chunk_end = end
        regions_split.append(f"{chromosome}:{chunk_start}-{chunk_end}")

# start timer
start_time = datetime.datetime.now()

# Count insertsize per chunk using multiprocessing
print(f"Counting insertsizes across {len(regions_split)} chunks...")
count_dict = {}
read_count = 0
# pbar = tqdm(total=len(regions_split), desc="Progress: ", unit="chunks")
for region in tqdm(regions_split):
    chrom, start, end = re.split("[:-]", region)
    for read in bam_obj.fetch(chrom, int(start), int(end)):
        read_count += 1
        try:
            barcode = read.get_tag(barcode_tag)
        except Exception:  # tag was not found
            barcode = "NA"

        # Add read to dict
        if check_in(barcode, barcodes) is True:
            size = abs(read.template_length) - 9  # length of insertion
            count_dict = _add_fragment(count_dict, barcode, size)

        # Close file and print elapsed time
end_time = datetime.datetime.now()
bam_obj.close()
elapsed = end_time - start_time
print("Done reading file - elapsed time: {0}".format(str(elapsed).split(".")[0]))

# Convert dict to pandas dataframe
print("Converting counts to dataframe...")
table = pd.DataFrame.from_dict(count_dict, orient="index")
# round mean_insertsize to 2 decimals
table["mean_insertsize"] = table["mean_insertsize"].round(2)

print("Done getting insertsizes from fragments!")

finish_run = time.time()

print(f'Run finished in: {finish_run - start_run}')


if __name__ == "__main__":
    # Test
    import episcanpy as epi

    fragments = "/mnt/workspace2/jdetlef/data/public_data/fragments_heart_left_ventricle_194_sorted.bed"
    h5ad_file = "/mnt/workspace2/jdetlef/data/public_data/heart_lv_SM-JF1NY.h5ad"#

    # fragments = "/home/jan/Workspace/bio_data/small_fragments.bed"
    #fragments = "/home/jan/Workspace/bio_data/fragments_heart_left_ventricle_194_sorted.bed"
    #h5ad_file = "/home/jan/Workspace/bio_data/heart_lv_SM-JF1NY.h5ad"
    adata = epi.read_h5ad(h5ad_file)
    adata_barcodes = adata.obs.index.tolist()
    # split index for barcodes CBs
    barcodes = []
    for entry in adata_barcodes:
        barcode = entry.split('+')[1]
        barcodes.append(barcode)

    table = insertsize_from_fragments(fragments, barcodes, n_threads=16)
    print(table)