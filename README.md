# A 991-LUT implementation of the EPFL sine benchmark

`sin_991.blif` implements the `sin` benchmark of the EPFL combinational benchmark suite (24 inputs, 25 outputs) with 991 LUTs of at most 6 inputs and 103 levels.

The best size table in `lsils/benchmarks` listed 994 LUTs and 115 levels on 31 October 2026, credited to F.-X. Reichl and F. Slivovsky (SAT-based exact synthesis of subcircuits). An open pull request, number 38, proposes 992.

## Method

This result starts from their published netlist, `best_results/size/sin_size_2026.blif`, and applies one standard ABC pass:

    read_blif sin_size_2026.blif
    strash
    if -K 6 -a
    mfs2 -W 6 -F 200 -D 200 -M 3000 -a
    write_blif sin_991.blif

Most of the gain is due to their netlist and to ABC. No language model is called at run time.

## Verification

    python3 exhaustive.py sin_991.blif sin.blif

The script compares the netlist with the benchmark's `sin.blif` on all 2^24 inputs, for each of the 25 outputs, by simulation.

## Prior art

Searched on 31 October 2026: the `lsils/benchmarks` table and its open pull requests, and recent arXiv papers on the EPFL benchmarks and LUT mapping. None reports fewer than 991 single-output 6-input LUTs for `sin`. One paper reports lower counts for dual-output fracturable LUTs, a different measure. A smaller unpublished netlist remains possible.

## Use of a language model

The scripts were generated with Claude (Anthropic), which was also used as a writing tool for this text.

## Licence

MIT licence, as for `lsils/benchmarks`.
