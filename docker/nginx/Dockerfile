FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="justivan.com"

COPY ./docker/nginx/default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./docker/nginx/uwsgi_params /etc/nginx/uwsgi_params
COPY ./docker/nginx/run.sh /run.sh

ENV LISTEN_PORT=80
ENV APP_HOST=django
ENV APP_PORT=8000

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]