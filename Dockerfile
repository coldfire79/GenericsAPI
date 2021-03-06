FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN echo "start building docker image"

# R related installations
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FCAE2A0E115C3D8A
RUN echo 'deb https://cloud.r-project.org/bin/linux/debian stretch-cran35/' >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y gcc wget r-base r-base-dev

RUN cp /usr/bin/R /kb/deployment/bin/.
RUN cp /usr/bin/Rscript /kb/deployment/bin/.

## Install packages are available for ecologists
# vegan: Community Ecology Package
RUN Rscript -e "install.packages('vegan')"

RUN pip install --upgrade pip \
    && python --version

RUN pip install scikit-bio==0.5.6 \
    && pip uninstall numpy -y \
    && pip install numpy==1.18.0 \
    && pip install networkx==2.1 \
    && pip install pandas==0.23.4 \
    && pip install xlrd==1.2.0\
    && pip install openpyxl==3.0.2 \
    && pip install xlsxwriter==1.2.7 \
    && pip install dotmap==1.3.8 \
    && pip install matplotlib==3.1.2 \
    && pip install scipy==1.4.1 \
    && pip install natsort==6.2.0 \
    && pip install scikit-learn==0.22.1 \
    && pip install plotly==4.4.1 \
    && pip install mock==3.0.5 \
    && pip install biom-format==2.1.7 \
    && pip install rpy2==3.3.3

# -----------------------------------------

RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

# install SigmaJS http://sigmajs.org/
RUN cd /kb/module && \
    wget https://github.com/jacomyal/sigma.js/archive/v1.2.1.zip && \
    unzip v1.2.1.zip && \
    rm -rf v1.2.1.zip && \
    mv sigma.js-1.2.1 sigma_js

# -----------------------------------------

COPY ./ /kb/module
WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
