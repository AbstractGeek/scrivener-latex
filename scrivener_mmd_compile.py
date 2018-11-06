#!/usr/bin/env python3
"""Converts scrivener multimarkdown files to docx, tex and pdf (at once)."""

import argparse
from glob import glob
import os
import sys
import subprocess


def get_file_if_unique(location, ext):
    """Find file if unique for the provided extension."""
    files = glob(os.path.join(location, ext))
    if len(files) == 1:
        return files[0]
    else:
        print(
            'Multiple/No ' + ext[1:] + ' files found in the working directory.'
            'Specify one please.')
        sys.exit()


def find_in_texfile(tex_content, matchstr):
    """Find matchstr in tex_content list."""
    doc_match = [i for i, line in enumerate(tex_content)
                 if matchstr in line]
    print(doc_match)
    if not (len(doc_match) == 1):
        print('Multiple/No ' + matchstr + ' found in generated tex file.')
        sys.exit()
    else:
        doc_match = doc_match[0]

    return doc_match


def main():
    """Parse input and download comic(s)."""
    parser = argparse.ArgumentParser(
        description=(
            'Converts scrivener mmd outputs to docx, tex and pdf. '
            'Integrates it with input and footer tex file, if available.'))

    parser.add_argument('mmd', nargs=1, type=str,
                        help='Multimarkdown file to be converted')
    parser.add_argument(
        "-l", "--location", default=os.getcwd(), help="set working directory")
    parser.add_argument(
        "-b", "--bibfile", default=False,
        help="Bibtex file used to generate bibliography.")
    parser.add_argument(
        "-m", "--maintex", default=False,
        help="Main tex file that controls appearance.")
    parser.add_argument(
        "-o", "--outfile", default=False,
        help="outfile prefix for generated files.")

    args = parser.parse_args()

    # Find bibliography and tex file if not provided
    if not args.bibfile:
        bibfile = get_file_if_unique(args.location, '*.bib')
    else:
        bibfile = args.bibfile

    if not args.maintex:
        maintex = get_file_if_unique(args.location, '*main.tex')
    else:
        maintex = args.maintex

    if not args.outfile:
        outfile = os.path.splitext(args.mmd[0])[0]
    else:
        outfile = args.outfile
    # Change location to the main folder as the working directory
    os.chdir(args.location)

    # Generate docx file from multimarkdown
    subprocess.run(["pandoc", "-s", "-S", "--normalize",
                    "--bibliography", bibfile, "--toc",
                    "-f", "markdown", "-t", "docx",
                    "-o", outfile + ".docx", args.mmd[0]])

    # Generate temp tex file
    subprocess.run(["pandoc", "-s", "-S", "--normalize",
                    "--natbib", "-f", "markdown", "-t", "latex",
                    "-o", "scrivener_mmd_compile_temp.tex", args.mmd[0],
                    "--variable", "documentclass=report"])

    # Read temp, main tex file
    with open('scrivener_mmd_compile_temp.tex', 'r') as tex_file:
        input_tex_content = tex_file.readlines()
    with open(maintex, 'r') as tex_file:
        main_tex_content = tex_file.readlines()

    # find start, input and stop in tex files
    doc_start = find_in_texfile(input_tex_content, "\\begin{document}")
    doc_stop = find_in_texfile(input_tex_content, "\\end{document}")
    input_line = find_in_texfile(
        main_tex_content, "\\input{scrivener-input.tex}")

    # Concatenate to create a complete tex file
    complete_tex_file = main_tex_content[:input_line] + \
        input_tex_content[doc_start + 1:doc_stop] + \
        main_tex_content[input_line + 1:]

    # Write complete tex file
    with open(outfile + '.tex', 'w') as tex_file:
        tex_file.writelines(complete_tex_file)

    # Compile tex and bib files
    subprocess.run(["pdflatex", outfile + '.tex'])
    subprocess.run(["bibtex", outfile + '.aux'])
    subprocess.run(["pdflatex", outfile + '.tex'])
    subprocess.run(["pdflatex", outfile + '.tex'])

    # Print exit message
    print("Scrivener mmd has been exported as docx, tex and pdf")


if __name__ == '__main__':
    main()
