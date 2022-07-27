docker build -t icesdk .
docker run --name icesdk -d -p 5000:5000 icesdk
sleep 2
docker ps