#! /bin/bash -v
/usr/local/bin/rsync  --progress --stats -a ~/repos/climate_students_eoas/content/_build/html/  -e ssh n7jov:/home/jovyan/repos/climate_students_eoas/book_html_source
