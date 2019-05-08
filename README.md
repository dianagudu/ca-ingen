# ca-ingen
Combinatorial Auctions Input Generator with realistic bundles for cloud resources

### prerequisites

* Cloud bundles generator [ingen](https://github.com/dianagudu/inputgen)
* All libs in requirements.txt

### usage

    python cagecli.py --help

    Usage: cagecli.py create [OPTIONS] INPUT OUTPUT

    Options:
    --count INTEGER  number of instances to create
    --help           Show this message and exit.

where INPUT contains the auction set parameters according to [template\_auction\_set\_params](template_auction_set_params):

    bids:
        amount: ${BIDS_N}
        model: ${BIDS_MODEL}
        binning_type: ${BIDS_BINNING_TYPE}
        binning_counts: ${BIDS_BINNING_COUNTS}
        domain: ${BIDS_DOMAIN}
    asks:
        amount: ${ASKS_N}
        model: ${ASKS_MODEL}
        binning_type: ${ASKS_BINNING_TYPE}
        binning_counts: ${ASKS_BINNING_COUNTS}
        domain: ${ASKS_DOMAIN}
    cost_model:
        slope: ${SLOPE}
        fixed: ${FIXED}
    valuations:
        dist_means: ${DIST_MEANS}
        a_sigma: ${A_SIGMA}
        b_sigma: ${B_SIGMA}


