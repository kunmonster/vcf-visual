# vcf-visual
A tool for generating summary graph of vcf file to help overview the vcf stat quickly.

## Ability
- Generate summary graph of vcf file using the diy axis
- Add filtrations when generating the graph
- Support structural variants (SV)


## Usage

1. Install the package using pip:
```
pip install vcf-visual
```

2. Run the command:

```
vcf-visual --vcf_file <path_to_vcf_file> --exp <Expression> --plot_type <plot_type> [--plot_path <path_to_save_plot>]
```

## Example

1. the variants number distrubution in every chromosome

```
vcf-visual --vcf_file example.vcf --exp "x=CHR,operation=count" --plot_type "bar" --plot_path "variants_num_dist.png"
```


