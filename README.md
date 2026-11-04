# EPFL benchmark records

Archive: [doi:10.5281/zenodo.23842203](https://doi.org/10.5281/zenodo.23842203) (all versions).

LUT-6 netlists that improve the best size listed for the [EPFL combinational benchmark suite](https://github.com/lsils/benchmarks) (at most 6 inputs per LUT).

| Benchmark | Previous best (LUTs, levels) | New size (LUTs, levels) | File |
|---|---:|---:|---|
| `sin` (24 inputs, 25 outputs) | 994, 115 (F.-X. Reichl and F. Slivovsky, SAT-based exact synthesis of subcircuits) | **991**, 103 | `circuits/sin_991.blif` |
| `mem_ctrl` (memory controller) | 1669, 27 (F.-X. Reichl and F. Slivovsky); 1663, 26 in open pull request 39 (T. Ursin) | **1662**, 26 | `circuits/mem_ctrl_1662.blif` |
| `log2` (32 inputs, 32 outputs) | 5986, 300 (F.-X. Reichl and F. Slivovsky); 5985, 206 in open pull request 39 (T. Ursin) | **5984**, 206 | `circuits/log2_5984.blif` |

`sin`: values read in `lsils/benchmarks` on 31 October 2026. An open pull request, number 38, proposed 992.

`mem_ctrl`: values read on 2 November 2026. Pull request 39 by Touko Ursin, not merged on that date, proposes 1663 LUTs (`best_results/size/mem_ctrl_size_2027.blif`).

`log2`: values read on 4 November 2026. Pull request 39, not merged on that date, proposes 5985 LUTs.

## Method

### sin

`sin_991.blif` starts from their published netlist, `best_results/size/sin_size_2026.blif`, and applies one standard ABC pass:

    read_blif sin_size_2026.blif
    strash
    if -K 6 -a
    mfs2 -W 6 -F 200 -D 200 -M 3000 -a
    write_blif sin_991.blif

Most of the gain is due to their netlist and to ABC. No language model is called at run time.

### mem_ctrl

`mem_ctrl_1662.blif` starts from Touko Ursin's 1663-LUT netlist in pull request 39. It is one LUT smaller. The gain comes from a randomised hill climb over standard ABC commands (`mfs2`, `lutpack`, `&satlut`, `&mfs`, remapping with `if -K 6`), accepting a move only if the LUT count does not grow; the winning move was an `mfs2` pass. Almost all of the result is due to Ursin's netlist, the Reichl and Slivovsky netlist before it, and ABC. No language model is called at run time.

### log2

`log2_5984.blif` starts from Touko Ursin's 5985-LUT netlist in pull request 39 and is one LUT smaller. It comes from the same randomised hill climb over standard ABC commands as `mem_ctrl`; the winning move was an `mfs2` pass. The input and output names are those of the benchmark. Almost all of the result is due to Ursin's netlist, the Reichl and Slivovsky netlist before it, and ABC. No language model is called at run time.

## Verification

    python3 exhaustive.py circuits/sin_991.blif sin.blif

The script compares the netlist with the benchmark's `sin.blif` on all 2^24 inputs, for each of the 25 outputs, by simulation.

    berkeley-abc -c "cec circuits/mem_ctrl_1662.blif mem_ctrl.blif"

ABC's combinational equivalence check against the benchmark's `random_control/mem_ctrl.blif` reports "Networks are equivalent". As a negative control, the same check reports a difference when one LUT is inverted. SHA-256 of the netlist: `63f25b6bf4f26fbcb40f972fbd675ce48db87d9ca2b6641687228b9db687ca86`.

For `log2`, ABC's `cec` does not conclude within an hour against the benchmark's `arithmetic/log2.blif`, so equivalence is shown in two steps, each reported "Networks are equivalent" by `cec`: `log2_5984.blif` against Ursin's 5985-LUT netlist of pull request 39, and that netlist against the published `best_results/size/log2_size_2026.blif`, which the benchmark maintainers checked against `log2.blif`. As a negative control, `cec` reports a difference when one LUT is inverted. SHA-256 of the netlist: `9ec2ae393b3bb5f2b21ba459605abe03c0a91e61e174639d27d537024f3299be`.

## Prior art

`sin`, searched on 31 October 2026: the `lsils/benchmarks` table and its open pull requests, and recent arXiv papers on the EPFL benchmarks and LUT mapping. None reports fewer than 991 single-output 6-input LUTs for `sin`. One paper reports lower counts for dual-output fracturable LUTs, a different measure. A smaller unpublished netlist remains possible.

`mem_ctrl`, searched on 2 November 2026: the table, its open pull requests (the best is 1663, number 39), 25 recent arXiv papers and Zenodo. None reports a single-output 6-input LUT count below 1662; the papers that mention `mem_ctrl` report other measures (FPGA LUT counts under standard flows, area, delay). A smaller unpublished netlist remains possible.

`log2`, searched on 4 November 2026: the table, its open pull requests (the best is 5985, number 39), 25 recent arXiv papers and Zenodo. None reports a single-output 6-input LUT count below 5984; lower figures in two papers count dual-output fracturable LUTs or inter-die edges, other measures. A smaller unpublished netlist remains possible.

## Use of a language model

The scripts were generated with Claude (Anthropic), which was also used as a writing tool for this text.

## Licence

MIT licence, as for `lsils/benchmarks`.
