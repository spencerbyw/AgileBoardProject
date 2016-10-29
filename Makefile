all:
	echo No effect.

fill_test_data:
	python tool/fill_test_data.py

drop_tables:
	python tool/drop_tables.py

create_tables:
	python tool/create_tables.py

from_scratch:
	python tool/create_tables.py && \
	python tool/fill_test_data.py

drop_and_fill:
	python tool/drop_tables.py && \
	python tool/create_tables.py && \
	python tool/fill_test_data.py
