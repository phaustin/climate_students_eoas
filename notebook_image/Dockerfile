FROM phaustin/base-image:jan09
USER ${NB_USER}

RUN mkdir -p ${HOME}/shared_files ${HOME}/content ${HOME}/content ${HOME}/work

USER root
RUN cd ${HOME}
RUN chown -R jovyan shared_files content work
RUN chgrp -R jovyan shared_files content work

USER ${NB_USER}

RUN echo "create work directory owned by jovyan" \
    && mkdir -p ${HOME}/work \
    && mkdir -p ${HOME}/.jupyter

RUN echo "copy contents of .jupyter" 
COPY --chown=${NB_USER}:${NB_USER} ./dotjupyter  ${HOME}/.jupyter/

RUN echo "conda activate ${CONDA_ENV}" >> ${HOME}/.bashrc
COPY jupyter_notebook_config.py /etc/jupyter/

RUN echo "update version tag" \
    && touch ${HOME}/climate_version_jan072023_monitor.txt


WORKDIR ${HOME}/work

CMD ["jupyterhub-singleuser"]
