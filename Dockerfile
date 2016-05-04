FROM localhost:5000/backend-comm-mongo
MAINTAINER Pål Karlsrud <paal@128.no>

ENV BASE_DIR /var/publishing

RUN git clone https://github.com/microserv/publish_django ${BASE_DIR}
RUN apk add --update python3 nginx curl

RUN cp ${BASE_DIR}/publishing.ini /etc/supervisor.d/
RUN curl -o /etc/supervisor.d/nginx.ini https://128.no/f/nginx.ini

RUN cp ${BASE_DIR}/publishing.conf /etc/nginx/conf.d/
RUN curl -o /etc/nginx/nginx.conf https://128.no/f/nginx.conf
RUN curl -o /etc/supervisor.d/mongodb.ini https://128.no/f/mongodb.ini

RUN virtualenv -p python3 ${BASE_DIR}/venv
ENV PATH ${BASE_DIR}/venv/bin:$PATH

WORKDIR ${BASE_DIR}
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN rm -rf /run && mkdir -p /run/nginx

EXPOSE 80
