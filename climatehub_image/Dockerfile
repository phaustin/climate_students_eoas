# https://github.com/jupyterhub/jupyterhub/blob/main/Dockerfile
FROM jupyterhub/jupyterhub:latest
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache -r /tmp/requirements.txt
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY user_list.txt /srv/jupyterhub/user_list.txt
RUN touch /srv/jupyterhub/container_version_may27.txt

