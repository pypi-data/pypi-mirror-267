# Readme

Quid is a tool for quotation detection in two texts, called source and target. If possible, the source text should be
the one that is quoted by the target text. This allows the algorithm to handle common properties of quotations, for
example, ellipses or inaccurate quotations. The following is an example output: 

~~~
0	52	This is a long Text and the long test goes on and on
0	45	This is a long Text [...] test goes on and on
~~~

## Demo
A demo website can be found [here](https://pages.cms.hu-berlin.de/schluesselstellen/quidweb/).

## Installation
~~~
pip install Quid
~~~

## Usage
There are two ways to use the algorithm, in code and from the command line.

### In Code

The [Quid in Code Readme](Quid-in-Code-Readme.md) describes the use of Quid in code and gives an overview of the
various arguments.

To use all default arguments, the most basic use would like this:

~~~
from quid.core.Quid import Quid

quid = Quid()
matches = quid.compare('file 1 content', 'file 2 content')
~~~

### Command line
The `quid compare` command provides a command line interface to the algorithm.

To use all default arguments, the most basic command would look like this:

~~~
quid compare file_1_path file_2_path
~~~

By default, the result is returned as a json structure: `List[Match]`. `Match` stores two `MatchSpans`. One for
the source text and one for the target text. `MatchSpan` stores the `start` and `end` character positions for the
matching spans in the source and target text. For example:

~~~
[
  {
    "source_span": {
      "start": 0,
      "end": 52,
      "text": "This is a long Text and the long test goes on and on"
    },
    "target_span": {
      "start": 0,
      "end": 45,
      "text": "This is a long Text [...] test goes on and on"
    }
  }
]
~~~

Alternatively, the result can be printed in a human-readable text format with the command line option
`--output-type text`. This will result in the following output:

~~~
0	52	This is a long Text and the long test goes on and on
0	45	This is a long Text [...] test goes on and on 
~~~

In case the matching text is not needed, the option `--no-text` allows to exclude the text from the output.

There are more command line options which are described in the
[Command Line Readme](Quid-Command-Line-Readme.md).

## Parallel processing
Quid supports using multiple processes when comparing multiple target texts with the source texts. To use multiple
processes the command line option `--max-num-processes` is used. The default is 1.

## Processing "long" texts
Depending on the length of the texts and the hardware used, processing times can get quite long. For texts longer than
a couple of hundreds of thousands characters, it can make sense to use the `--split-long-texts` command line option (or
`split_long_texts` argument) and set `--max-num-processes` (or `max_num_processes` argument) to define the number of
parallel processes to be used. If `--split-long-texts` is used, texts longer than the default of 30000 tokens will be
split. This limit can also be changed using the `--split-length` command line option (or `split_length` argument).
When run from the command line, using `--split-long-texts` automatically shows a progress bar. To show a progress bar
when using Quid in code, the `show_progress` argument can be set to `True`.

*Note*: `--split-long-texts` does not work in combination with comparing multiple target texts (i.e. passing a folder as
`target-path`).

## Passager
The package `passager` contains code to extract key passages from the found matches. The `passage` command produces
several json files.
The resulting data structure is documented in the [data structure readme](DATA_STRUCTURE_README.md).

The [passager readme](Passager-Readme.md) contains more information on command line options.

## Visualization
The package `visualization` contains code to create the content for a web page to visualize the key passages.
For a white label version of the website, see [QuidEx-wh](https://scm.cms.hu-berlin.de/schluesselstellen/quidex-wh).

The [visualizer readme](Visualizer-Readme.md) contains more information on command line options.

## Logging
By default, the log level is set to `WARN`. This can be changed with the `--log-level` command line option.
For example:

~~~
quid --log-level INFO compare …
~~~

## Performance
For in-depth information on the evaluation, see our paper below.
Performance of the current version of Quid is as follows:

| Work             | Precision | Recall | F-Score |
|------------------|-----------|--------|---------|
| Die Judenbuche   | 0.83      | 0.92   | 0.87    |
| Micheal Kohlhaas | 0.71      | 0.93   | 0.81    |

## History
Quid was formerly known as Lotte and later renamed. Earlier publications use the name Lotte.

## Data
All data, which can be made available, can be found [here](https://scm.cms.hu-berlin.de/schluesselstellen/quid-resources).
Due to copyright restrictions, it is unfortunately not possible to publish the complete scholarly works.

## Citation
If you use Quid or base your work on our code, please cite our paper:
~~~
@inproceedings{arnold2021lotte,
  title = {{L}otte and {A}nnette: {A} {F}ramework for {F}inding and {E}xploring {K}ey {P}assages in {L}iterary {W}orks},
  author = {Arnold, Frederik and Jäschke, Robert},
  booktitle = {Proceedings of the Workshop on Natural Language Processing for Digital Humanities},
  year = {2021},
  publisher = {NLP Association of India (NLPAI)},
  url = {https://aclanthology.org/2021.nlp4dh-1.7},
  pages = {55--63}
}
~~~

## Acknowledgements
The algorithm is inspired by _sim_text_ by Dick Grune [^1]
and _Similarity texter: A text-comparison web tool based on the “sim_text” algorithm_ by Sofia Kalaidopoulou (2016) [^2]

[^1]: https://dickgrune.com/Programs/similarity_tester/ (Stand: 12.04.2021)

[^2]: https://people.f4.htw-berlin.de/~weberwu/simtexter/522789_Sofia-Kalaidopoulou_bachelor-thesis.pdf (Stand: 12.04.2021)
