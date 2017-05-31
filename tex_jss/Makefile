FILE_NAME := report

TEMP_FILES := \
	$(FILE_NAME).aux \
	$(FILE_NAME).bbl \
	$(FILE_NAME).log \
	$(FILE_NAME).blg \
	$(FILE_NAME).brf \
	$(FILE_NAME).out

SECTION_FILES = \
	$(FILE_NAME).tex
#	$(FILE_NAME).tex \
#	preamble.tex \
#	introduction.tex \
#	background.tex \
#	result.tex \
#	setup.tex \
#	threats_to_validity.tex \
#	conclusion.tex

BIBTEX_FILES = \
	reference.bib

GEN_FIGURES = \

STATIC_FIGURES = \

TABLES = \

DEBUG=no
ifneq '$(DEBUG)' 'yes'
LATEX_FLAGS="-interaction=batchmode"
endif

.DELETE_ON_ERROR:

################################################################################
# Main paper building
################################################################################

$(FILE_NAME).pdf: $(SECTION_FILES) $(GEN_FIGURES) $(STATIC_FIGURES) $(TABLES)
	pdflatex $(LATEX_FLAGS) $(FILE_NAME)
	bibtex $(FILE_NAME)
	pdflatex $(LATEX_FLAGS) $(FILE_NAME)
	pdflatex $(LATEX_FLAGS) $(FILE_NAME)
	rm -f $(TEMP_FILES)

.PHONY: clean
clean:
	rm -f $(TEMP_FILES) $(GEN_FIGURES) $(FILE_NAME).pdf