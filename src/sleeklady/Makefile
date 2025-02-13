PYTHON := python

SCRIPTS := \
    format_change_01.py \
    filtered_02.py \
    dropped_03.py \
    create_brands_04.py \
    categories_05.py \
    storenames_06.py \
    columns_created_07.py \
    product_description_08.py \
    product_code_09.py \
    capitalized_10.py \
    final_excel.py

all: run_scripts

run_scripts:
	@for script in $(SCRIPTS); do \
	    echo "Running $$script"; \
	    $(PYTHON) "$$script" || exit 1; \
	done

.PHONY: all run_scripts
