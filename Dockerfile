FROM python:3.8.3-slim


WORKDIR /searcher
COPY webpython_hw01/requirements.txt webpython_hw01/requirements.txt
RUN pip install -r webpython_hw01/requirements.txt

COPY webpython_hw01/* webpython_hw01/
COPY README.md .
COPY setup.py .
RUN python setup.py bdist
RUN python setup.py install


CMD ["bash"]
