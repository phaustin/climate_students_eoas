# https://github.com/jupyterhub/jupyterhub/blob/main/Dockerfile
FROM jupyterhub/jupyterhub:2.3.1
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY user_list.txt /srv/jupyterhub/user_list.txt
RUN touch /srv/jupyterhub/container_version_dec31.txt

