FROM python:3
# ARG TIMEZONE
# ENV TIMEZONE=${TIMEZONE}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APPDIR=/app

# RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime \
#   && echo $TZ > /etc/timezone

RUN apt update \
  && apt install -y cifs-utils \
  && rm -rf /var/lib/apt/lists/*

# target directories are created automatically if they don't already exist
COPY *.py *.txt *.sh ${APPDIR}/
RUN pip install --no-cache-dir -r ${APPDIR}/requirements.txt

WORKDIR ${APPDIR}
CMD [ "/bin/bash" ]
