FROM continumio/miniconda3

RUN apt-get update && apt-get upgrade
RUN apt-get install graphviz:w

RUN conda create -n env python=3.6
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

