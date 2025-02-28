# vcf-visual
A tool for generating summary graph of vcf file to help overview the vcf stat quickly.

## Ability
- Generate summary graph of vcf file using the diy axis
- Add filtrations when generating the graph
- Support structural variants (SV)


## Usage

1. Install the package using pip:
```shell
pip install vcfvisual
```

2. Run the command:

```shell
vcfvisual --vcf_file <path_to_vcf_file> --exp <Expression> --plot_type <plot_type> [--plot_path <path_to_save_plot>]
```

3. this program needs user to provide a expression which contains the axis and operation. Please print the help message before using it.

``` shell
vcfvisual --help # print the help message
vcfvisual --support # check the supported expression and plot_type
```


## Example

1. bar chart

the bar chart needs a categorical variable as x-axis, and a operation


- visualize the number of variants in each chromosome

```shell
vcfvisual --vcf_file example.vcf --exp "x=CHR,operation=count" --plot_type "bar" --plot_path "variants_num_dist.png"
```



