# EPFL benchmark records

Archive: [doi:10.5281/zenodo.23842203](https://doi.org/10.5281/zenodo.23842203) (all versions).

LUT-6 netlists that improve the best size listed for the [EPFL combinational benchmark suite](https://github.com/lsils/benchmarks) (at most 6 inputs per LUT).

| Benchmark | Previous best (LUTs, levels) | New size (LUTs, levels) | File |
|---|---:|---:|---|
| `sin` (24 inputs, 25 outputs) | 994, 115 (F.-X. Reichl and F. Slivovsky, SAT-based exact synthesis of subcircuits) | **991**, 103 | `circuits/sin_991.blif` |

Values read in `lsils/benchmarks` on 31 October 2026. An open pull request, number 38, proposes 992 for `sin`.

## Method

`sin_991.blif` starts from their published netlist, `best_results/size/sin_size_2026.blif`, and applies one standard ABC pass:

    read_blif sin_size_2026.blif
    strash
    if -K 6 -a
    mfs2 -W 6 -F 200 -D 200 -M 3000 -a
    write_blif sin_991.blif

Most of the gain is due to their netlist and to ABC. No language model is called at run time.

## Verification

    python3 exhaustive.py circuits/sin_991.blif sin.blif

The script compares the netlist with the benchmark's `sin.blif` on all 2^24 inputs, for each of the 25 outputs, by simulation.

## Prior art

Searched on 31 October 2026: the `lsils/benchmarks` table and its open pull requests, and recent arXiv papers on the EPFL benchmarks and LUT mapping. None reports fewer than 991 single-output 6-input LUTs for `sin`. One paper reports lower counts for dual-output fracturable LUTs, a different measure. A smaller unpublished netlist remains possible.

## Use of a language model

The scripts were generated with Claude (Anthropic), which was also used as a writing tool for this text.

## Licence

MIT licence, as for `lsils/benchmarks`.
