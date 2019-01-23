# Scrivener-latex: A workflow to convert scrivener markdown to latex (and docx).

Writing a PhD thesis is convenient in scrivener (not to mention fun), but it is hard to format it later. Latex is perfect to beautify the thesis, but hard to write a thesis in without getting caught up in formating. I came up with workflow while working on my thesis to get the best of both worlds. Enjoy!


## Setting up scrivener
Here is how you set up scrivener when you begin you thesis (check the thesis-example.scriv for more details).

1. Create chapters as folders and the sections as text inside the folders. Note: names of the folders/text becomes the chapter/section title respectively (see below image).

2. Edit (and create) label names and assign to chapters, sections and appendices. Note: this is used to automatically assign chapter, section and appendix while generating latex code. The spellings should therefore match exactly (including lowercase; see below image).

![](https://raw.githubusercontent.com/AbstractGeek/scrivener-latex/master/scrivener-customization/scrivener-chapter-text-labels.png "Chapter, section, appendix labels")


3. Add `\markedchapter{short title}{<$title>}\label{<$label>-<$position>}` to the start of the folder text (press the scrivenings view to add it to the folder). The first argument of the /markedchapter is a short title for the chapter that will be used for headers in the thesis. Similarly, add this `## <$title>{#<$label>-<$parentposition>.<$position>}` to the start of the text inside the folders (which becomes sections later; see image below). Both these additions is used the latex generation later, and creates easy labels for referencing chapters and sections inside text. For example chapter 1 can be referred by `\ref{chapter-1}` and section 1.1 can be referred by `\ref{section-1.1}`.

![](https://raw.githubusercontent.com/AbstractGeek/scrivener-latex/master/scrivener-customization/scrivener-latex-text.png "scrivener latex reference text")

4. Use the scrivener-latex.scrformat in scrivener-customization to compile. Import it, compile for mmd, and assign section headers as "MAIN text formatting ..." (see figure below). Compile to generate mmds that can be used convert to latex and pdf files.
![](https://raw.githubusercontent.com/AbstractGeek/scrivener-latex/master/scrivener-customization/scrivener-compile-settings.png "scrivener compile settings")


## Generating and referring figures


## Citing articles using zotero



## Modifying latex styling
