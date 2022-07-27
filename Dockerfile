# FROM python:3.6-slim
FROM python:3.6-alpine
# FROM public.ecr.aws/sam/emulation-python3.6:latest
# FROM public.ecr.aws/p6i7m9s5/python-3.6-alpine:latest

# RUN apt-get clean \
#     && apt-get -y update

# RUN apt-get -y install \
#     # nginx \
#     python3-dev \
#     build-essential

RUN apk update && \
  apk add --no-cache \
  python3 \
  vim \
  curl
  # build-essential

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY . .

EXPOSE 5000
CMD [ "python", "IceSdkApi.py","-w","/data/plugins" ]