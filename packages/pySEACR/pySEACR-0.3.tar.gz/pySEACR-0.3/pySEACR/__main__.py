"""Command line tool for pySEACR."""
import argparse
import os

from pySEACR.auc_from_bdg import BDG
from pySEACR.normalize import Normalize
from pySEACR.threshold_finder import ThresholdFinder


def parse_args():
    """
    Parse command line arguments.

    Returns:
        namespace
    """
    parser = argparse.ArgumentParser(
        prog='pySEACR',
        description='Sparse Enrichment Analysis for CUT&RUN',
    )
    parser.add_argument(
        'exp',
        help='Experimental/Treatment bedgraph',
    )
    parser.add_argument(
        'ctrl',
        help='Control/IGG bedgraph or a scalar from 0 to 1',
    )
    parser.add_argument(
        '-n',
        '--norm',
        help='Normalize the data before finding peaks',
        action='store_true',
    )
    parser.add_argument(
        '-s',
        '--stringent',
        help='Use the stringent peak threshold',
        action='store_true',
    )

    return parser.parse_args()


def normalize(exp, ctrl):
    """
    Normalize the values in the control data.

    Parameters:
        exp (BDG): BDG file object of experimental/treatment data
        ctrl (BDG): BDG file object of the contorl/IgG data

    Returns:
        Normalized numpy.array
    """
    normer = Normalize(exp, ctrl)
    return ctrl.vec * normer.constant()


def thresh_from_ctrl(exp, ctrl_file, norm, use_stringent):
    """
    Compute height thresholds by comparing two files.

    Parameters:
        exp (BDG): Experimental/treatment BDG file object
        ctrl_file (str): Path to the control/IgG bdg file
        norm (str): If yes, will normalize data before calculating thresholds
        use_stringent (bool): Whether to use the stringent threshold

    Returns:
        height threshold and genome threshold
    """
    ctrl = BDG(ctrl_file)
    if norm:
        ctrl.vec = normalize(exp, ctrl)

    thresholds = ThresholdFinder(exp, ctrl)
    auc_thresh = thresholds.relaxed()
    check = thresholds.thresh_check()

    if use_stringent:
        stringent = thresholds.stringent(auc_thresh)
        auc_thresh = stringent if check is None else check[1]
    elif check is not None:
        auc_thresh = check[0]

    return auc_thresh, thresholds.genome()


def main(args):
    """
    pySEACR main body.

    Parameters:
        args (namespace): Command line arguments
    """
    exp = BDG(args.exp)

    auc_thresh = 0
    genome = 0
    if os.path.isfile(args.ctrl):
        auc_thresh, genome = thresh_from_ctrl(
            exp,
            args.ctrl,
            args.norm,
            args.stringent,
        )
    else:
        args.ctrl = float(args.ctrl)
        thresholds = ThresholdFinder(exp, args.ctrl)
        vec_input = exp.max if args.stringent else exp.vec
        auc_thresh = thresholds.static(vec_input)

    print_output(exp.regions, auc_thresh, genome)


def print_output(stretches, height, width):
    """
    Print pySEACR results in BED format.

    Parameters:
        stretches (list): AUC stretches from a BDG
        height (float): Minimum peak height
        width (float): Minimum peak width
    """
    for stretch in stretches:
        if stretch.peak > height and stretch.n > width:
            print('\t'.join([str(_) for _ in (
                stretch.contig,
                stretch.coord[0],
                stretch.coord[1],
                stretch.auc,
                stretch.peak,
                stretch.peak_coords(),
                stretch.n,
            )]))


if __name__ == '__main__':
    main(parse_args())
