go get -v -d ./...
go build src/*.go


az login
az account set --subscription c830bb7a-83f5-45e3-81fc-3c2053e7d16f
az acr login --name xiaoyanacr

docker build . -f Dockerfile -t xiaoyanacr.azurecr.io/test/aml-gotest:1012-1 
docker run -p 8000:8000 xiaoyanacr.azurecr.io/test/aml-gotest:1012-1 
docker push  xiaoyanacr.azurecr.io/test/aml-gotest:1012-1


az ml online-endpoint create  -f gotest-endpoint.yml --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws
az ml online-deployment create  -f gotest-deployment.yml --all-traffic --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws

