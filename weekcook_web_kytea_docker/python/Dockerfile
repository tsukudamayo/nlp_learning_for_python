FROM python:3.6
ENV LANG C.UTF-8
ENV TZ Azia/Tokyo
RUN mkdir /home/work
COPY work/ /home/work
WORKDIR /home/work
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "/home/work/uwsgi.ini"]
