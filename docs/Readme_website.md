# website workflow

0. create the environment if it doesn't exist, for example for intel osx:

        mamba create --name climcourse --file ~/climate_students_eoas/notebook_image/conda-osx-64.lock
        conda activate climcourse
        mamba install ansible jupyter-book

1. build a new version of the book

       cd ~/repos/climate_students_eoas/content
       jb build .
      
2. upload the html to the server

       cd ~/repos/climate_students_eoas/ansible
       ansible-playbook -i hosts.yml -u jovyan -l n7jov -e "course_name=climate_2022" setup_website_noauth.yml

3. visit https://phaustin.org/climate_2022/html/home.html and do a hard refresh to update the browser cache  (shift-reload)
