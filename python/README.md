## Azure resource
[pytest-endpoint3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/c830bb7a-83f5-45e3-81fc-3c2053e7d16f/resourceGroups/xiaoyan-group-dev/providers/Microsoft.MachineLearningServices/workspaces/xiaoyan-aml-ws/onlineEndpoints/pytest-endpoint4/overview)


## Commands to build & deploy

az login  
az account set --subscription c830bb7a-83f5-45e3-81fc-3c2053e7d16f  
az acr login --name xiaoyanacr  

docker build . -f Dockerfile -t xiaoyanacr.azurecr.io/test/aml-pytest:1208-1
docker run -p 8000:8000  xiaoyanacr.azurecr.io/test/aml-pytest:1208-1
docker push  xiaoyanacr.azurecr.io/test/aml-pytest:1208-1

az ml online-endpoint create  -f pytest-endpoint.yml --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws  
az ml online-deployment create  -f pytest-deployment.yml --all-traffic --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws  

az ml online-endpoint get-credentials --name pytest-endpoint1  --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws