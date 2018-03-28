# block-email
FROM python:3
EXPOSE 7012
ENV FLASK_DEBUG=1
ENV PORT=7012
RUN pip install flask
RUN pip install yagmail
